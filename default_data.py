# default_data.py
# This file contains default data to be used for generating resumes. 
# Users can modify this file to customize the resume content.
# Ensure that the structure and formatting are preserved while making changes.

master_resume = [
    {
        # The title of this section in the resume (e.g., Personal Information, Objective).
        "title": "Personal Information",
        # Content of the section, provided as a list of strings. 
        # Modify the strings to suit your personal information. Ensure they are comma-separated.
        "content": [
            "Your Name Here",  # Replace with your name.
            "City, State ZIP ⋄ Phone Number ⋄ Email Address ⋄ Personal Website ⋄ GitHub URL ⋄ LinkedIn URL"  # Update with your personal details.
        ],
        # The window title for the resume generator GUI.
        "window_title": "Resume Generator",
        "window_width": "900", # You should only put digits 0-9 here
        "window_length": "500", # You should only put digits 0-9 here
        "editor_window_width": "800", # You should only put digits 0-9 here
        "editor_window_length": "500", # You should only put digits 0-9 here
        "main_window_font_size": "20", # You should only put digits 0-9 here    
        "editor_text_size": "16" # You should only put digits 0-9 here
    },
    {
        "title": "Objective",
        # List of objectives. You can modify the text and add/remove items as long as they remain in a comma-separated list.
        "content": [
            "Your first career objective here.",  # Replace with your career objective.
            "Another career objective.",  # Add as many objectives as you'd like.
            "Example: To leverage my expertise in [specific skills] to contribute to [specific role or organization]."
        ]
    },
    {
        "title": "Certifications",
        # List of certifications. Modify the items to reflect your own certifications.
        "content": [
            "Certification 1",  # Replace with your first certification.
            "Certification 2"  # Add more certifications as needed.
        ]
    },
    {
        "title": "Education",
        # List of education experiences. Each entry is a list of strings, where the first string is the institution, 
        # and subsequent strings can include details like degrees, majors, and minors.
        "content": [
            ["First educational experience", "Details about it (e.g., degree, graduation date)"],
            ["Second educational experience", "Details about it"]
        ]
    },
    {
        "title": "Core Competencies",
        # List of skills. Add or remove items freely, ensuring they remain comma-separated.
        "content": [
            "Skill 1",  # Replace with a skill.
            "Skill 2",  # Add more skills as needed.
            "Skill 3"  # Ensure no trailing comma after the last item.
        ]
    },
    {
        "title": "Professional Experience",
        # List of professional experiences. Each entry contains a subtitle (job title and company),
        # a date range, and a list of details about the role.
        "content": [
            {
                "subtitle": "Job Title – Company Name",  # Replace with your job title and company name.
                "date": "Start Date – End Date, Location",  # Replace with the job's duration and location.
                "details": [
                    "Responsibility 1",  # Replace with your job responsibility.
                    "Responsibility 2"  # Add more responsibilities as needed.
                ]
            },
            {
                "subtitle": "Second Job Title – Company Name", 
                "date": "Start Date – End Date, Location", 
                "details": [
                    "Responsibility 1",
                    "Responsibility 2"
                ]
            }
        ]
    },
    {
        "title": "Technical Projects",
        # List of projects. Add or remove projects as needed. Each project should be a string.
        "content": [
            "Project 1: Brief description of what you did.",  # Replace with your first project.
            "Project 2: Another brief description.",  # Add more projects as needed.
            "Example: Configured a Splunk SIEM environment to analyze security logs."
        ]
    }
]

# End of file.
# To use this file, replace the placeholders with your own information and save the file as `data.py`.
# Ensure the structure remains consistent for the program to process it correctly.