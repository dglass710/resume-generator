from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE

def set_single_spacing(paragraph):
    """Set single spacing and remove extra space before/after the paragraph."""
    p_format = paragraph.paragraph_format
    p_format.line_spacing = 1
    p_format.space_after = Pt(0)
    p_format.space_before = Pt(0)

def add_hyperlink(paragraph, url, text):
    """
    A function that places a hyperlink within a paragraph.
    This code is based on known workarounds for python-docx.
    """
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    
    # Create the w:hyperlink tag and set its relationship id.
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    # Create a w:r element and a w:rPr element.
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    # Optionally, you can set the font color and underline for hyperlinks.
    color = OxmlElement('w:color')
    color.set(qn('w:val'), "0000FF")
    rPr.append(color)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), "single")
    rPr.append(u)
    
    new_run.append(rPr)
    
    # Set the text for the run.
    new_run_text = OxmlElement('w:t')
    new_run_text.text = text
    new_run.append(new_run_text)
    hyperlink.append(new_run)
    
    # Append the hyperlink element to the paragraph.
    paragraph._p.append(hyperlink)
    return hyperlink

def is_email(token):
    """Determine if the token should be treated as an email address."""
    token = token.strip()
    return "@" in token and "." in token

def is_phone(token):
    """
    Determine if the token looks like a phone number.
    This function strips non-digit characters and checks for exactly 10 digits.
    """
    digits = ''.join(ch for ch in token if ch.isdigit())
    return len(digits) == 10

def is_url(token):
    """
    Determine if the token should be treated as a URL.
    Returns True if the token starts with http(s)://, www.,
    or if it contains a dot and no spaces.
    """
    token = token.strip()
    if token.startswith("http://") or token.startswith("https://") or token.startswith("www."):
        return True
    if "." in token and " " not in token:
        return True
    return False

def generate_resume(selected_sections, output_file="Custom_Resume.docx"):
    """
    Generates a Word document resume based on the selected sections.
    
    Applies enhancements to improve visual appeal while keeping the layout
    clear and ATS-friendly.
    
    Args:
        selected_sections (list): List of sections with titles and content.
        output_file (str): The output file name.
    """
    doc = Document()

    # Set default style (Arial, 11pt) for consistency.
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    # Optionally, add a header with the applicant's name (from Personal Information)
    applicant_name = ""
    for section in selected_sections:
        if section["title"] == "Personal Information" and section["content"]:
            applicant_name = section["content"][0]
            break
    if applicant_name:
        header = doc.sections[0].header
        header_para = header.paragraphs[0]
        header_para.text = applicant_name + " - Resume"
        header_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    for section in selected_sections:
        if section["title"] == "Personal Information":
            for index, line in enumerate(section["content"]):
                if index == 0:
                    # For the first line (name), center and bold it.
                    para = doc.add_paragraph()
                    run = para.add_run(line)
                    run.bold = True
                    run.font.size = Pt(14)
                    para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                else:
                    # Split the line by the delimiter (diamond character).
                    tokens = line.split(" \u22c4 ")
                    para = doc.add_paragraph()
                    for i, token in enumerate(tokens):
                        if i > 0:
                            para.add_run(" \u22c4 ")
                        token = token.strip()
                        if is_email(token):
                            add_hyperlink(para, f"mailto:{token}", token)
                        elif is_phone(token):
                            digits = ''.join(ch for ch in token if ch.isdigit())
                            add_hyperlink(para, f"tel:{digits}", token)
                        elif is_url(token):
                            # Prepend http:// if missing for proper linking.
                            link = token if token.startswith("http") else "http://" + token
                            add_hyperlink(para, link, token)
                        else:
                            para.add_run(token)
                set_single_spacing(para)
            doc.add_paragraph("")  # Extra space after Personal Information.
            continue

        # Refine section headings: increase size, bold, and underline.
        title_para = doc.add_heading(section["title"], level=1)
        for run in title_para.runs:
            run.font.size = Pt(16)
            run.bold = True
            run.underline = True
        set_single_spacing(title_para)

        if section["title"] == "Core Competencies":
            competencies = ", ".join(section["content"]) + "."
            para = doc.add_paragraph(competencies)
            set_single_spacing(para)

        elif section["title"] == "Education":
            for item in section["content"]:
                if not item:
                    continue
                # The first element is the institution/program (header).
                para = doc.add_paragraph(item[0])
                set_single_spacing(para)
                # Subsequent details are indented using proper left indent.
                for detail in item[1:]:
                    indented_para = doc.add_paragraph(detail)
                    indented_para.paragraph_format.left_indent = Pt(36)
                    set_single_spacing(indented_para)

        elif section["title"] == "Professional Experience":
            for item in section["content"]:
                # Change label from "subtitle" to "Title/Company" for clarity.
                title_para = doc.add_paragraph()
                title_run = title_para.add_run(f"Title/Company: {item['subtitle']} ({item['date']})")
                title_run.bold = True
                title_run.font.size = Pt(11)
                set_single_spacing(title_para)
                for detail in item["details"]:
                    detail_para = doc.add_paragraph(detail, style='List Bullet')
                    detail_para.paragraph_format.left_indent = Pt(18)
                    set_single_spacing(detail_para)

        elif section["title"] == "Technical Projects":
            for project in section["content"]:
                para = doc.add_paragraph(project, style='List Bullet')
                para.paragraph_format.left_indent = Pt(18)
                set_single_spacing(para)

        else:
            for item in section["content"]:
                if isinstance(item, dict):
                    subheading = doc.add_paragraph()
                    subheading_run = subheading.add_run(f"{item.get('subtitle', 'No Title')} ({item.get('date', '')})")
                    subheading_run.bold = True
                    subheading_run.font.size = Pt(12)
                    set_single_spacing(subheading)
                    for detail in item.get("details", []):
                        detail_para = doc.add_paragraph(detail, style='List Bullet')
                        detail_para.paragraph_format.left_indent = Pt(18)
                        set_single_spacing(detail_para)
                else:
                    para = doc.add_paragraph(item)
                    set_single_spacing(para)

    doc.save(output_file)
    print(f"Resume saved as {output_file}")
