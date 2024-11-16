from docx import Document
from docx.shared import Pt, RGBColor

def set_single_spacing(paragraph):
    """Set single spacing and remove extra space after a paragraph."""
    paragraph_format = paragraph.paragraph_format
    paragraph_format.line_spacing = 1  # Single spacing
    paragraph_format.space_after = Pt(0)  # Remove extra space after the paragraph
    paragraph_format.space_before = Pt(0)  # Remove extra space before the paragraph

def format_subtitle(paragraph):
    """Format subtitles (like job titles) to make them smaller and less prominent."""
    run = paragraph.runs[0]
    run.font.size = Pt(11)  # Slightly smaller font size
    run.font.color.rgb = RGBColor(64, 64, 64)  # Neutral dark gray color
    run.bold = False  # Remove bold styling

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

        # Handle Professional Experience
        elif section["title"] == "Professional Experience":
            for item in section["content"]:
                # Format job title and date
                subtitle_text = f"{item['subtitle']} ({item['date']})"
                subtitle_para = doc.add_paragraph(subtitle_text)
                set_single_spacing(subtitle_para)
                format_subtitle(subtitle_para)  # Apply new formatting for job titles

                # Add bullet points for details (no extra spacing or hyphen)
                for detail in item["details"]:
                    detail_para = doc.add_paragraph(detail, style='List Bullet')  # Standard bullet
                    set_single_spacing(detail_para)

        # Handle other sections
        else:
            for item in section["content"]:
                para = doc.add_paragraph(item)
                set_single_spacing(para)

    # Save the document
    doc.save(output_file)
    print(f"Resume saved as {output_file}")
