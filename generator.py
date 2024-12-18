from docx import Document
from docx.shared import Pt


def set_single_spacing(paragraph):
    """Set single spacing and remove extra space after a paragraph."""
    paragraph_format = paragraph.paragraph_format
    paragraph_format.line_spacing = 1  # Single spacing
    paragraph_format.space_after = Pt(0)  # Remove extra space after the paragraph
    paragraph_format.space_before = Pt(0)  # Remove extra space before the paragraph


def generate_resume(selected_sections, output_file="Custom_Resume.docx"):
    """
    Generates a Word document resume based on selected sections.

    Args:
        selected_sections (list): List of selected sections with titles and content.
        output_file (str): The name of the output Word document file.
    """
    doc = Document()

    for section in selected_sections:
        # Handle Personal Information as a special case
        if section["title"] == "Personal Information":
            for index, line in enumerate(section["content"]):
                # Remove "Title" style to avoid the horizontal line
                para = doc.add_paragraph(line)
                if index == 0:  # First line (name): bold and larger font
                    run = para.runs[0]
                    run.bold = True
                    run.font.size = Pt(14)
                set_single_spacing(para)
            continue  # Skip adding a blank line here

        # Add section title as a heading
        title_para = doc.add_heading(section["title"], level=1)
        set_single_spacing(title_para)

        # Handle Core Competencies (comma-separated skills on a single line)
        if section["title"] == "Core Competencies":
            core_competencies = ", ".join(section["content"]) + "."
            para = doc.add_paragraph(core_competencies)
            set_single_spacing(para)

        elif section["title"] == "Education":
            for item in section["content"]:
                if not item:  # Skip empty items
                    continue

                # Add the first item (main entry) as unindented
                para = doc.add_paragraph(item[0])
                set_single_spacing(para)

                # Add any additional details (indented)
                for detail in item[1:]:
                    indented_para = doc.add_paragraph(f"    {detail}")
                    set_single_spacing(indented_para)

        elif section["title"] == "Professional Experience":
            for item in section["content"]:
                # Add the title and date as a bold paragraph
                title_para = doc.add_paragraph()
                title_run = title_para.add_run(f"{item['subtitle']} ({item['date']})")
                title_run.bold = True
                title_run.font.size = Pt(11)  # Same size as regular text
                set_single_spacing(title_para)

                # Add the bullet points (details)
                for detail in item["details"]:
                    detail_para = doc.add_paragraph(detail, style='List Bullet')  # Standard bullet
                    set_single_spacing(detail_para)

        else:
            for item in section["content"]:
                if isinstance(item, dict):  # For sections with subtitles, dates, and details
                    subtitle_para = doc.add_paragraph(f"{item['subtitle']} ({item['date']})", style='Heading 2')
                    set_single_spacing(subtitle_para)
                    for detail in item["details"]:
                        detail_para = doc.add_paragraph(detail, style='List Bullet')  # Standard bullet
                        set_single_spacing(detail_para)
                else:
                    para = doc.add_paragraph(item)
                    set_single_spacing(para)

    # Save the document
    doc.save(output_file)
    print(f"Resume saved as {output_file}")
