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
            "DAVID GLASS",  # Replace with your name.
            "Chicago, IL 60618 ⋄ 847.764.9200 ⋄ dglass2525@gmail.com ⋄ thedavidglass.com ⋄ github.com/dglass710 ⋄ linkedin.com/in/david-a-glass"  # Update with your personal details.
        ],
        # The window title for the resume generator GUI.
        "window_title": "Cybersecurity Analyst",
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
            "To join a dynamic Security Operations Center (SOC) as an analyst, where I can leverage my skills in real-time threat monitoring, vulnerability scanning, and incident response to detect and mitigate potential security risks, ensuring the organization's infrastructure remains secure.",
            "To utilize my expertise in penetration testing, ethical hacking, and security assessments to identify and remediate vulnerabilities, ensuring comprehensive protection for enterprise systems against cyber threats.",
            "To apply my technical skills and hands-on experience with cybersecurity tools and methodologies in a challenging analyst role, contributing to organizational security through proactive risk mitigation and incident handling."
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
            "Risk Assessment", "Threat Mitigation", "Incident Response", "Vulnerability Scanning", "Penetration Testing",
            "Network Security", "Splunk", "Security Onion", "Snort rules", "Log Analysis",
            "Ethical Hacking", "Privilege Escalation", "Exploit Development", "Packet Analysis", "SIEM Analysis",
            "Incident Reporting", "Firewall Policy Development", "Log Correlation and Alerts", "OSINT Techniques", "Recon-ng",
            "Google Dorking", "Shodan", "Advanced Nmap Scans", "Digital Evidence Preservation", "Password Cracking (Hashcat)"

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
            "Conducted penetration tests and network traffic analysis using Metasploit, Nmap, and Wireshark to identify and exploit vulnerabilities in simulated environments.",
            "Developed and implemented firewall policies using UFW and firewalld to ensure secure network configurations.",
            "Configured and monitored a Splunk SIEM environment to analyze security logs, correlate events, and respond to potential threats.",
            "Designed and executed vulnerability scans on virtualized networks, identifying and prioritizing remediation for high-risk exposures.",
            "Created an offline version of the \"Have I Been Pwned\" database using Docker, enabling secure local queries of compromised credentials."
        ]
    }
]

# End of file.
# To use this file, replace the placeholders with your own information and save the file as `data.py`.
# Ensure the structure remains consistent for the program to process it correctly.
