from docx import Document

def generate_resume(selected_sections, output_file="Custom_Resume.docx"):
    """
    Generates a Word document resume based on selected sections.
    
    Args:
        selected_sections (list): List of selected sections with titles and content.
        output_file (str): The name of the output Word document file.
    """
    doc = Document()

    for section in selected_sections:
        # Add section title as a heading
        doc.add_heading(section["title"], level=1)
        
        # Handle Core Competencies (comma-separated skills on a single line)
        if section["title"] == "Core Competencies":
            core_competencies = ", ".join(section["content"]) + "."
            doc.add_paragraph(core_competencies)
        else:
            for item in section["content"]:
                if isinstance(item, dict):  # For sections with subtitles, dates, and details
                    doc.add_paragraph(f"{item['subtitle']} ({item['date']})", style='Heading 2')
                    for detail in item["details"]:
                        doc.add_paragraph(f" - {detail}", style='List Bullet')
                else:
                    doc.add_paragraph(item)

    # Save the document
    doc.save(output_file)
    print(f"Resume saved as {output_file}")
