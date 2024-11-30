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
        "window_title": "Security Engineer",
        "window_width": "1600", # You should only put digits 0-9 here
        "window_length": "1000", # You should only put digits 0-9 here
        "editor_window_width": "900", # You should only put digits 0-9 here
        "editor_window_length": "500", # You should only put digits 0-9 here
        "main_window_font_size": "20", # You should only put digits 0-9 here    
        "editor_text_size": "16" # You should only put digits 0-9 here
    },
    {
        "title": "Objective",
        # List of objectives. You can modify the text and add/remove items as long as they remain in a comma-separated list.
        "content": [
            "To leverage my expertise in cryptography, penetration testing, and secure system design to build robust security frameworks that protect organizational assets. I aim to contribute to proactive threat mitigation and ensure the integrity of critical infrastructure.",
            "To utilize my knowledge of encryption protocols, secure software development, and penetration testing to design, implement, and maintain applications and systems with a focus on minimizing vulnerabilities and maximizing resilience.",
            "To apply my skills in penetration testing, vulnerability assessment, and cryptographic methods to anticipate and mitigate threats, ensuring enterprise systems are prepared for emerging cybersecurity challenges."
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
            "Cryptography", "Penetration Testing", "Vulnerability Assessment", "SSL/TLS Certificate Management", "Application Security",
            "Python", "Bash", "Encryption Protocols (AES", "RSA", "GPG)", "Secure Software Development", "Firewall Configuration",
            "Docker Security", "System Hardening", "Network Security", "Incident Response", "Log Analysis",
            "Threat Mitigation", "Secure System Design", "Automation Scripting", "Splunk", "SIEM Analysis",
            "Firewall Policy Development", "Cloud Infrastructure Security (OCI, Linode)", "Vulnerability Remediation", "Load Balancer Configuration",
            "SSL Certificates", "Data Integrity Validation", "Exploit Development", "Secure Communication Protocols", "Automation of Security Tasks"
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
                    "Instructed 370 students K-12 in mathematical concepts.",
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
            "Developed a secure file-sharing application using encryption protocols like AES and RSA to ensure confidentiality and integrity during data transfer.",
            "Performed application penetration tests to identify vulnerabilities, providing detailed reports and remediation strategies to developers for secure software improvements.",
            "Implemented SSL/TLS encryption for a web application and managed secure certificate handling, ensuring encrypted communication between users and servers.",
            "Designed and executed custom Python scripts to automate vulnerability scanning and mitigate risks across an organization’s network infrastructure.",
            "Created secure Docker container deployments, configuring firewalls and access controls to minimize attack surfaces in production environments."
        ]
    }
]

# End of file.
# To use this file, replace the placeholders with your own information and save the file as `data.py`.
# Ensure the structure remains consistent for the program to process it correctly.
