# Resume Generator

This project is a Python-based GUI application that allows users to create customizable resumes in Word document format. The application uses the `python-docx` library for document generation and `Tkinter` for the graphical user interface.

## Features
- Select from predefined resume sections to include in your final document.
- Customize sections, such as Objectives, with pre-set or custom inputs.
- Flexible layout options for presenting skills, experiences, and education.
- Save the resume as a Word document (`.docx`) with consistent, professional formatting.

---

## Getting Started with Dependencies

### Ensure `python-docx` is Installed

The `python-docx` library is required to generate Word documents. Follow these steps to ensure it is installed and ready to use:

1. **Check if `python-docx` is Installed**:
   Run the following command in your terminal to see if the library is already installed:
   ```bash
   python -m pip show python-docx
   ```
   - If it returns details about the package (e.g., version, location), you're good to go.
   - If it shows `WARNING: Package(s) not found: python-docx`, proceed to the next step.

2. **Install `python-docx`**:
   Use the following command to install the library:
   ```bash
   python -m pip install python-docx
   ```
   - If your system uses `python3` instead of `python`, run:
     ```bash
     python3 -m pip install python-docx
     ```
   - For systems where `python` or `python3` may be ambiguous, explicitly specify `pip` for your Python environment:
     ```bash
     pip install python-docx
     ```

3. **Verify Installation**:
   After installation, confirm that `python-docx` is installed by running:
   ```bash
   python -m pip show python-docx
   ```
   You should see package details confirming the installation.

---

## How to Customize `data.py`

The `data.py` file contains the default resume data used by the application. Users can modify this file to tailor the sections and content to their specific needs. Below is a guide to customizing `data.py`.

### `master_resume` Structure

The `master_resume` variable is a list of dictionaries, where each dictionary represents a resume section. Each section has two main keys:
- `title`: The section title (e.g., "Personal Information").
- `content`: The content of the section, which can be strings, lists, or nested dictionaries.

---

### Order Matters

The order of dictionaries in the `master_resume` structure determines the order in which sections appear:
1. **In the GUI**: Sections appear in the same order as they are listed in `data.py`.
2. **In the Resume**: The same order is reflected in the generated Word document.

To rearrange the order of sections in both the GUI and the resume:
- Simply rearrange the dictionaries in the `master_resume` list.

For example:
```python
master_resume = [
    { "title": "Certifications", "content": ["CompTIA Security+ Certified"] },
    { "title": "Objective", "content": ["Highly motivated IT professional..."] }
]
```
In this case:
1. "Certifications" will appear before "Objective" in both the GUI and the generated resume.

---

### Section Types

#### 1. **Basic Text Sections**
These sections contain simple text content, such as "Objective" or "Certifications".

```python
{
    "title": "Objective",
    "content": [
        "Highly motivated IT professional with a strong foundation in mathematics, computer science, and cybersecurity.",
        "Seeking a challenging role in IT operations, leveraging my cybersecurity and troubleshooting skills to ensure seamless system performance.",
        "Dedicated to providing innovative solutions and streamlining IT processes to meet dynamic business needs."
    ]
}
```

**How to Customize**:
- Add, edit, or remove items in the `content` list to reflect your career goals.

---

#### 2. **List-Based Sections**
For sections like "Core Competencies," the `content` is a list of skills or attributes.

```python
{
    "title": "Core Competencies",
    "content": [
        "TCP/IP", "DNS", "DHCP", "Firewalls", "Network Troubleshooting",
        "Packet Analysis", "Windows", "Linux", "Python", "Bash scripting"
    ]
}
```

**How to Customize**:
- Add or remove skills from the list.
- Ensure each skill is enclosed in double quotes and separated by a comma.

---

#### 3. **Nested List Sections**
Sections like "Education" use nested lists to organize main entries and additional details.

```python
{
    "title": "Education",
    "content": [
        ["Northwestern University Cybersecurity Program: Graduated June 2024"],
        ["DePaul University: Graduated March 2022",
         "B.S. in Applied and Computational Mathematics; Minors in Computer Science and Physics."]
    ]
}
```

**How to Customize**:
- Add new educational institutions as lists.
- Each entry should have the main information as the first string, followed by any additional details in subsequent strings.

---

#### 4. **Dictionary-Based Sections**
Sections like "Professional Experience" contain a list of dictionaries for each job or project.

```python
{
    "title": "Professional Experience",
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
}
```

**How to Customize**:
- Add new job entries as dictionaries.
  - `subtitle`: Job title and company.
  - `date`: The employment dates and location.
  - `details`: A list of bullet points describing your responsibilities and accomplishments.

---

### Example Customization

Here’s an example of a custom addition:

**Add a Certification Section:**

```python
{
    "title": "Certifications",
    "content": [
        "AWS Certified Solutions Architect – Associate",
        "Google Professional Cloud Architect"
    ]
}
```

**Add a New Job to Professional Experience:**

```python
{
    "subtitle": "Tech Startup – Software Engineer Intern",
    "date": "June 2021 – August 2021, Chicago, IL",
    "details": [
        "Collaborated with a team to develop a web-based project management tool using Python and Flask.",
        "Optimized database queries to improve performance by 25%."
    ]
}
```

---

## Guidelines for Customization
- **Consistency**: Follow the existing structure to avoid breaking the program.
- **String Formatting**: Ensure all text values are enclosed in double quotes (`"`).
- **Validation**: Test the GUI after making changes to ensure the resume generates correctly.

---

## Running the Application
1. Update the `master_resume` variable in `data.py` to include your personalized information.
2. Run the `gui.py` script to launch the GUI:
   ```bash
   python gui.py
   ```
3. Select the sections and subsections you want to include in your resume.
4. Enter a custom objective (if needed) in the GUI’s text box.
5. Generate your resume and enjoy a professional Word document tailored to your needs!

For questions or further assistance, feel free to reach out. Happy customizing!
