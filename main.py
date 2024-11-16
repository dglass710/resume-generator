from data import master_resume
from generator import generate_resume

def select_sections(master_resume):
    print("Available Sections:")
    for idx, section in enumerate(master_resume):
        print(f"{idx + 1}. {section['title']}")

    selected_indices = input("Enter the numbers of the sections you want to include, separated by commas: ")
    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]

    selected_sections = [master_resume[i] for i in selected_indices]
    return selected_sections

def select_core_competencies(core_competencies):
    print("\nAvailable Core Competencies:")
    for idx, skill in enumerate(core_competencies):
        print(f"{idx + 1}. {skill}")

    selected_indices = input("Enter the numbers of the skills you want to include, separated by commas: ")
    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]

    selected_skills = [core_competencies[i] for i in selected_indices]
    return selected_skills

def main():
    # Step 1: Select Sections
    selected_sections = select_sections(master_resume)

    # Step 2: Handle Core Competencies
    for section in selected_sections:
        if section["title"] == "Core Competencies":
            section["content"] = select_core_competencies(section["content"])

    # Step 3: Generate Resume
    generate_resume(selected_sections)

if __name__ == "__main__":
    main()
