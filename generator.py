# generate.py
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

def set_single_spacing(paragraph):
    """Set single spacing and remove extra space before/after the paragraph."""
    p_format = paragraph.paragraph_format
    p_format.line_spacing = 1
    p_format.space_after = Pt(0)
    p_format.space_before = Pt(0)

def add_hyperlink(paragraph, url, text):
    """
    Inserts a hyperlink into a paragraph. Returns the hyperlink element.
    After adding the hyperlink, an empty run is appended to break the hyperlink's scope.
    """
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

# Refined token checks using regular expressions.
_email_re = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
def is_email(token):
    """Return True if token is a valid email."""
    token = token.strip()
    return bool(_email_re.match(token))

_phone_re = re.compile(r'^\D*(\d\D*){10}$')
def is_phone(token):
    """
    Return True if token consists of (or can be reduced to) exactly 10 digits.
    """
    digits = ''.join(ch for ch in token if ch.isdigit())
    return len(digits) == 10

_url_re = re.compile(r'^(https?://|www\.)', re.IGNORECASE)
def is_url(token):
    """
    Return True if token is a URL. It checks if the token starts with http(s):// or www.,
    or if it contains a dot and no spaces.
    """
    token = token.strip()
    if _url_re.match(token):
        return True
    if '.' in token and ' ' not in token:
        return True
    return False

def get_output_path(output_file):
    """
    Determine an output path for the generated resume.
    When running frozen on macOS, save to a persistent folder in ~/Documents/ResumeGeneratorApp.
    Otherwise, return the output_file as-is (which will be in the current working directory).
    """
    if getattr(sys, 'frozen', False) and sys.platform == "darwin":
        persistent_dir = Path.home() / "Documents" / "ResumeGeneratorApp"
        persistent_dir.mkdir(parents=True, exist_ok=True)
        return str(persistent_dir / output_file)
    else:
        return output_file

def generate_resume(selected_sections, output_file="Custom_Resume.docx"):
    """
    Generates a Word document resume based on the selected sections.
    
    Personal Information is rendered with the first item as the name (centered, bold, larger)
    and all remaining items (links, emails, phone numbers) concatenated on one line,
    separated by a diamond (U+22C4). Other sections are preceded by a header with the section title,
    styled in 16pt bold, underlined text.
    
    Additionally, a document header is added with "<Name> - Resume" in blue, bold, underlined, and centered.
    """
    doc = Document()
    
    # Set default style to Arial 11pt.
    style = doc.styles['Normal']
    font = style.font
    font.name = "Arial"
    font.size = Pt(11)
    
    # --- Header: Add applicant name with " - Resume" ---
    applicant_name = ""
    for section in selected_sections:
        if section["title"] == "Personal Information" and section["content"]:
            applicant_name = section["content"][0]
            break
    if applicant_name:
        header = doc.sections[0].header
        if len(header.paragraphs) == 0:
            header_para = header.add_paragraph()
        else:
            header_para = header.paragraphs[0]
        header_para.text = ""
        header_run = header_para.add_run(applicant_name + " - Resume")
        header_run.bold = True
        header_run.font.size = Pt(14)
        header_run.font.color.rgb = RGBColor(0, 0, 255)  # Blue color
        header_run.underline = True
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # --- Process each section ---
    for section in selected_sections:
        if section["title"] == "Personal Information":
            # First item is the name.
            if section["content"]:
                name_para = doc.add_paragraph()
                name_run = name_para.add_run(section["content"][0])
                name_run.bold = True
                name_run.font.size = Pt(14)
                name_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                set_single_spacing(name_para)
            # Process remaining items: each token is handled in its own run.
            if len(section["content"]) > 1:
                links_para = doc.add_paragraph()
                tokens = section["content"][1:]
                for idx, item in enumerate(tokens):
                    if idx > 0:
                        links_para.add_run(" \u22C4 ")
                    token = item.strip()
                    if is_email(token):
                        add_hyperlink(links_para, f"mailto:{token}", token)
                    elif is_phone(token):
                        digits = ''.join(ch for ch in token if ch.isdigit())
                        add_hyperlink(links_para, f"tel:{digits}", token)
                    elif is_url(token):
                        link_url = token if token.lower().startswith("http") else "http://" + token
                        add_hyperlink(links_para, link_url, token)
                    else:
                        links_para.add_run(token)
                set_single_spacing(links_para)
            doc.add_paragraph("")  # Extra space after Personal Information.
            continue
        
        # For all other sections, add a section header.
        title_para = doc.add_heading(section["title"], level=1)
        for run in title_para.runs:
            run.font.size = Pt(16)
            run.bold = True
            run.underline = True
        set_single_spacing(title_para)
        
        # Process section content.
        if section["title"] == "Core Competencies":
            competencies = ", ".join(section["content"]) + "."
            comp_para = doc.add_paragraph(competencies)
            set_single_spacing(comp_para)
        elif section["title"] == "Education":
            for item in section["content"]:
                if not item:
                    continue
                header_para = doc.add_paragraph(item[0])
                set_single_spacing(header_para)
                for detail in item[1:]:
                    detail_para = doc.add_paragraph(detail)
                    detail_para.paragraph_format.left_indent = Pt(36)
                    set_single_spacing(detail_para)
        elif section["title"] == "Professional Experience":
            for item in section["content"]:
                exp_para = doc.add_paragraph()
                title_text = f"{item.get('subtitle', '')} ({item.get('date', '')})"
                exp_run = exp_para.add_run(title_text)
                exp_run.bold = True
                exp_run.font.size = Pt(11)
                set_single_spacing(exp_para)
                for detail in item.get("details", []):
                    detail_para = doc.add_paragraph(detail, style='List Bullet')
                    detail_para.paragraph_format.left_indent = Pt(18)
                    set_single_spacing(detail_para)
        elif section["title"] == "Technical Projects":
            for project in section["content"]:
                proj_para = doc.add_paragraph(project, style='List Bullet')
                proj_para.paragraph_format.left_indent = Pt(18)
                set_single_spacing(proj_para)
        else:
            for item in section["content"]:
                if isinstance(item, dict):
                    other_para = doc.add_paragraph()
                    other_run = other_para.add_run(f"{item.get('subtitle', '')} ({item.get('date', '')})")
                    other_run.bold = True
                    other_run.font.size = Pt(12)
                    set_single_spacing(other_para)
                    for detail in item.get("details", []):
                        detail_para = doc.add_paragraph(detail, style='List Bullet')
                        detail_para.paragraph_format.left_indent = Pt(18)
                        set_single_spacing(detail_para)
                else:
                    simple_para = doc.add_paragraph(item)
                    set_single_spacing(simple_para)
                    
    # Determine output path based on platform and frozen status.
    output_path = get_output_path(output_file)
    doc.save(output_path)
    print(f"Resume saved as {output_path}")
    
    # Attempt to open the document automatically.
    if sys.platform == "darwin":
        os.system(f'open "{output_path}"')
    elif os.name == 'nt':
        os.startfile(output_path)

# Example usage (uncomment the lines below to test the function):
# if __name__ == "__main__":
#     import json
#     with open("data.json", "r") as f:
#         selected_sections = json.load(f)
#     generate_resume(selected_sections)
