from docx import Document
from docx.shared import Pt

def set_single_spacing(paragraph):
    """Set single spacing and remove extra space before/after the paragraph."""
    paragraph_format = paragraph.paragraph_format
    paragraph_format.line_spacing = 1
    paragraph_format.space_after = Pt(0)
    paragraph_format.space_before = Pt(0)

def generate_resume(selected_sections, output_file="Custom_Resume.docx"):
    """
    Generates a Word document resume based on the selected sections.

    Args:
        selected_sections (list): List of sections with titles and content.
        output_file (str): The output file name.
    """
    doc = Document()

    for section in selected_sections:
        if section["title"] == "Personal Information":
            for index, line in enumerate(section["content"]):
                para = doc.add_paragraph(line)
                if index == 0:
                    run = para.runs[0]
                    run.bold = True
                    run.font.size = Pt(14)
                set_single_spacing(para)
            doc.add_paragraph("")
            continue

        title_para = doc.add_heading(section["title"], level=1)
        set_single_spacing(title_para)

        if section["title"] == "Core Competencies":
            competencies = ", ".join(section["content"]) + "."
            para = doc.add_paragraph(competencies)
            set_single_spacing(para)
        elif section["title"] == "Education":
            for item in section["content"]:
                if not item:
                    continue
                para = doc.add_paragraph(item[0])
                set_single_spacing(para)
                for detail in item[1:]:
                    indented_para = doc.add_paragraph("    " + detail)
                    set_single_spacing(indented_para)
        elif section["title"] == "Professional Experience":
            for item in section["content"]:
                title_para = doc.add_paragraph()
                title_run = title_para.add_run(f"{item['subtitle']} ({item['date']})")
                title_run.bold = True
                title_run.font.size = Pt(11)
                set_single_spacing(title_para)
                for detail in item["details"]:
                    detail_para = doc.add_paragraph(detail, style='List Bullet')
                    set_single_spacing(detail_para)
        elif section["title"] == "Technical Projects":
            for project in section["content"]:
                para = doc.add_paragraph(project, style='List Bullet')
                set_single_spacing(para)
        else:
            for item in section["content"]:
                if isinstance(item, dict):
                    subtitle_para = doc.add_paragraph(f"{item['subtitle']} ({item['date']})", style='Heading 2')
                    set_single_spacing(subtitle_para)
                    for detail in item["details"]:
                        detail_para = doc.add_paragraph(detail, style='List Bullet')
                        set_single_spacing(detail_para)
                else:
                    para = doc.add_paragraph(item)
                    set_single_spacing(para)

    doc.save(output_file)
    print(f"Resume saved as {output_file}")
