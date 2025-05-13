# generator.py
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
import os
import sys
from pathlib import Path
import re

# Refined token checks using regular expressions.
_email_re = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
_phone_re = re.compile(r'^\D*(\d\D*){10}$')
_url_re = re.compile(r'^(https?://|www\.)', re.IGNORECASE)

def set_single_spacing(paragraph):
    """Set single spacing and remove extra space before/after the paragraph."""
    p_format = paragraph.paragraph_format
    p_format.line_spacing = 1
    p_format.space_after = Pt(0)
    p_format.space_before = Pt(0)

def add_hyperlink(paragraph, url, text):
    """Inserts a hyperlink into a paragraph. Returns the hyperlink element."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    
    # Create the w:hyperlink element and set its relationship id.
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    # Create a run inside the hyperlink.
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    # Set hyperlink styling (blue, underlined).
    color = OxmlElement('w:color')
    color.set(qn('w:val'), "0000FF")
    rPr.append(color)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), "single")
    rPr.append(u)
    new_run.append(rPr)
    
    new_run_text = OxmlElement('w:t')
    new_run_text.text = text
    new_run.append(new_run_text)
    hyperlink.append(new_run)
    
    # Append the hyperlink element to the paragraph.
    paragraph._p.append(hyperlink)
    # Append an empty run to ensure the hyperlink formatting does not continue.
    paragraph.add_run("")
    return hyperlink

def is_email(token):
    """Return True if token is a valid email."""
    token = token.strip()
    return bool(_email_re.match(token))

def is_phone(token):
    """Return True if token consists of (or can be reduced to) exactly 10 digits."""
    digits = ''.join(ch for ch in token if ch.isdigit())
    return len(digits) == 10

def is_url(token):
    """Return True if token is a URL."""
    token = token.strip()
    if _url_re.match(token):
        return True
    if '.' in token and ' ' not in token:
        return True
    return False

class Generator:
    def __init__(self, selected_sections):
        self.selected_sections = selected_sections

    def generate(self, output_file):
        """Generate a Word document resume based on the selected sections."""
        # Create a new document
        doc = Document()
        
        # Set default style to Arial 11pt
        style = doc.styles['Normal']
        font = style.font
        font.name = "Arial"
        font.size = Pt(11)
        
        # Set document margins (0.5 inches on all sides)
        sections = doc.sections
        for section in sections:
            section.top_margin = Pt(36)    # 0.5 inches = 36 points
            section.bottom_margin = Pt(36)
            section.left_margin = Pt(36)
            section.right_margin = Pt(36)

        # Process each section
        for section in self.selected_sections:
            title = section["title"]
            content = section["content"]

            # Special handling for Personal Information section
            if title == "Personal Information":
                # First item is the name - make it large, bold, and centered
                name_paragraph = doc.add_paragraph()
                name_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                name_run = name_paragraph.add_run(content[0])
                name_run.bold = True
                name_run.font.size = Pt(24)
                set_single_spacing(name_paragraph)

                # Remaining items go on one line, separated by diamonds
                if len(content) > 1:
                    info_paragraph = doc.add_paragraph()
                    info_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                    set_single_spacing(info_paragraph)

                    for i, item in enumerate(content[1:], 1):
                        if i > 1:  # Add separator between items (not before first item)
                            separator = info_paragraph.add_run(" ")
                            separator.font.size = Pt(12)

                        # Check if the item is a special token (email, phone, URL)
                        if is_email(item):
                            add_hyperlink(info_paragraph, f"mailto:{item}", item)
                        elif is_phone(item):
                            # Format phone number consistently
                            digits = ''.join(filter(str.isdigit, item))
                            formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                            add_hyperlink(info_paragraph, f"tel:{digits}", formatted)
                        elif is_url(item):
                            url = item if item.startswith('http') else f'http://{item}'
                            add_hyperlink(info_paragraph, url, item)
                        else:
                            run = info_paragraph.add_run(item)
                            run.font.size = Pt(12)

                doc.add_paragraph()  # Add space after personal info

            # Special handling for Objective section
            elif title == "Objective":
                # Add section header
                header = doc.add_paragraph()
                header_run = header.add_run(title)
                header_run.bold = True
                header_run.font.size = Pt(16)
                header_run.underline = True
                set_single_spacing(header)

                # Add the selected objective
                obj_para = doc.add_paragraph()
                obj_para.add_run(content)
                set_single_spacing(obj_para)
                doc.add_paragraph()  # Add space after objective

            # Special handling for Education and Professional Experience sections
            elif title in ["Education", "Professional Experience"]:
                # Add section header
                header = doc.add_paragraph()
                header_run = header.add_run(title)
                header_run.bold = True
                header_run.font.size = Pt(16)
                header_run.underline = True
                set_single_spacing(header)

                # Process each item
                for item in content:
                    # Handle Education items (which are lists) differently
                    if title == "Education" and isinstance(item, list):
                        # First item is the title
                        title_para = doc.add_paragraph()
                        title_run = title_para.add_run(item[0])
                        title_run.bold = True
                        set_single_spacing(title_para)

                        # Remaining items are details
                        for detail in item[1:]:
                            detail_para = doc.add_paragraph()
                            detail_para.paragraph_format.left_indent = Pt(18)  # 0.25 inches
                            detail_run = detail_para.add_run("• " + detail)
                            set_single_spacing(detail_para)
                    else:
                        # Professional Experience items are dictionaries
                        # Add the title/institution
                        title_para = doc.add_paragraph()
                        title_run = title_para.add_run(item["subtitle"])
                        title_run.bold = True
                        set_single_spacing(title_para)

                        # Add dates if present (Professional Experience)
                        if "date" in item:
                            dates_para = doc.add_paragraph()
                            dates_run = dates_para.add_run(item["date"])
                            dates_run.italic = True
                            set_single_spacing(dates_para)

                        # Add details
                        for detail in item["details"]:
                            detail_para = doc.add_paragraph()
                            detail_para.paragraph_format.left_indent = Pt(18)  # 0.25 inches
                            detail_run = detail_para.add_run("• " + detail)
                            set_single_spacing(detail_para)

                doc.add_paragraph()  # Add space after section

            # Default handling for other sections
            else:
                # Add section header
                header = doc.add_paragraph()
                header_run = header.add_run(title)
                header_run.bold = True
                header_run.font.size = Pt(16)
                header_run.underline = True
                set_single_spacing(header)

                # Add content items as bullet points
                for item in content:
                    item_para = doc.add_paragraph()
                    item_para.paragraph_format.left_indent = Pt(18)  # 0.25 inches
                    item_para.add_run("• " + item)
                    set_single_spacing(item_para)

                doc.add_paragraph()  # Add space after section

        # Ensure output directory exists
        output_path = get_output_path(output_file)
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the document to the provided absolute path
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the document
        doc.save(output_file)
# Example usage (uncomment the lines below to test the function):
# if __name__ == "__main__":
#     import json
#     with open("data.json", "r") as f:
#         selected_sections = json.load(f)
#     generate_resume(selected_sections)
