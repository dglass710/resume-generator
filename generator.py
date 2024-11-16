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
                para = doc.add_paragraph(line, style='Title' if index == 0 else None)
                set_single_spacing(para)
            continue

        # Add section title as a heading
        title_para = doc.add_heading(section["title"], level=1)
        set_single_spacing(title_para)

        # Handle Core Competencies (comma-separated skills on a single line)
        if section["title"] == "Core Competencies":
            core_competencies = ", ".join(section["content"]) + "."
            para = doc.add_paragraph(core_competencies)
            set_single_spacing(para)

        # Handle Education section
        elif section["title"] == "Education":
            for item in section["content"]:
                # First line (non-indented)
                para = doc.add_paragraph(item[0])
                set_single_spacing(para)
                # Subsequent lines (indented)
                for detail in item[1:]:
                    indented_para = doc.add_paragraph(f"    {detail}")
                    set_single_spacing(indented_para)

        # Handle other sections
        else:
            for item in section["content"]:
                if isinstance(item, dict):  # For sections with subtitles, dates, and details
                    subtitle_para = doc.add_paragraph(f"{item['subtitle']} ({item['date']})", style='Heading 2')
                    set_single_spacing(subtitle_para)
                    for detail in item["details"]:
                        detail_para = doc.add_paragraph(f"    - {detail}", style='List Bullet')  # Indented details
                        set_single_spacing(detail_para)
                else:
                    para = doc.add_paragraph(item)
                    set_single_spacing(para)

    # Save the document
    doc.save(output_file)
    print(f"Resume saved as {output_file}")
