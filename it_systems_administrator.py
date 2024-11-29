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
            "DAVID GLASS",
            "Chicago, IL 60618 ⋄ 847.764.9200 ⋄ dglass2525@gmail.com ⋄ thedavidglass.com ⋄ github.com/dglass710 ⋄ linkedin.com/in/david-a-glass"
        ],
        # The window title for the resume generator GUI.
        "window_title": "IT Systems Administrator",
        "window_width": "1000", # You should only put digits 0-9 here
        "window_length": "500", # You should only put digits 0-9 here
        "editor_window_width": "900", # You should only put digits 0-9 here
        "editor_window_length": "500", # You should only put digits 0-9 here
        "main_window_font_size": "20", # You should only put digits 0-9 here    
        "editor_text_size": "16" # You should only put digits 0-9 here
    },
    {
        "title": "Objective",
        # List of objectives. You can modify the text and add/remove items as long as they remain in a comma-separated list.
        "content": [
            "To secure a position as an IT Systems Administrator, maintaining and optimizing enterprise systems and infrastructure while ensuring reliable and secure network operations across on-premises and cloud environments.",
            "To contribute as an IT Systems Administrator by implementing automation scripts, managing cloud resources, and ensuring seamless integration of new technologies to drive operational efficiency.",
            "To leverage my expertise in system configuration, user management, and security hardening to support corporate IT environments, ensuring end-users have secure and reliable access to necessary resources."
        ]
    },
    {
        "title": "Certifications",
        # List of certifications. Modify the items to reflect your own certifications.
        "content": [
            "CompTIA Security+ Certified"
        ]
    },
    {
        "title": "Education",
        # List of education experiences. Each entry is a list of strings, where the first string is the institution, 
        # and subsequent strings can include details like degrees, majors, and minors.
        "content": [
            ["Northwestern University Cybersecurity Program: Graduated June 2024"],
            ["DePaul University: Graduated March 2022", 
             "B.S. in Applied and Computational Mathematics; Minors in Computer Science and Physics."]
        ]
    },
    {
        "title": "Core Competencies",
        # List of skills. Add or remove items freely, ensuring they remain comma-separated.
        "content": [
            "Linux Administration", "macOS Administration", "Windows Administration", "Active Directory", "Group Policy",
            "System Hardening", "User and Permissions Management", "Firewalls (UFW, firewalld)", "Process Management", "Backup and Archive Management",
            "Cron Jobs", "Scripting Maintenance Tasks", "Cloud Infrastructure (Azure, AWS)", "Containerization", "Load Balancers",
            "SQL Query Design", "Docker", "Automation Scripting", "Technical Communication", "Problem Solving"
        ]
    },
    {
        "title": "Professional Experience",
        # List of professional experiences. Each entry contains a subtitle (job title and company),
        # a date range, and a list of details about the role.
        "content": [
            {
                "subtitle": "Mathnasium – Mathematics Instructor",
                "date": "April 2023 – Present, Chicago, IL",
                "details": [
                    "Instructed 370 students in mathematical concepts.",
                    "Enhanced security of iPads used in instruction by implementing guided access controls."
                ]
            },
            {
                "subtitle": "DePaul University Math Department – Undergraduate Student Researcher",
                "date": "November 2020 – May 2022, Chicago, IL",
                "details": [
                    "Developed Python tools for research, focusing on preventing rounding errors in fraction representations.",
                    "Advanced the understanding of the Frobenius coin problem and computed symmetry in large data sets."
                ]
            }
        ]
    },
    {
        "title": "Technical Projects",
        # List of projects. Add or remove projects as needed. Each project should be a string.
        "content": [
            "Developed and implemented firewall policies using UFW and firewalld to ensure secure server configurations and restrict unauthorized access.",
            "Automated user account creation and permissions assignment with Bash scripts, improving efficiency for onboarding processes.                ",
            "Built and managed a virtual private cloud (VPC) on Azure, deploying virtual machines and configuring secure remote access via SSH.            ",
            "Deployed and maintained Docker containers for streamlined application development and environment consistency.                              ",
            "Configured cron jobs to automate system maintenance, including backups, log rotation, and system updates.                                   "
        ]
    }
]

# End of file.
# To use this file, replace the placeholders with your own information and save the file as `data.py`.
# Ensure the structure remains consistent for the program to process it correctly.
