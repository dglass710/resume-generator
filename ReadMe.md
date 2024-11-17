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

## Customizing `data.py`

The `data.py` file contains the default resume data used by the application. You can modify this file to tailor the sections and content to your specific needs. The order of the dictionaries in the `master_resume` list determines the order of sections in both the GUI and the generated resume.

Below, we explain how each section is structured and how to modify it while maintaining the correct syntax.

---

### Objective, Certifications, and Personal Information

These sections are **basic text sections**. Each section contains a `title` (e.g., "Objective") and a `content` list, where each item in the list is a string.

#### Example:
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

#### How to Customize:
- **Add a new statement**: Add a new string to the `content` list:
  ```python
  "content": [
      "Previous statements...",
      "New statement here."
  ]
  ```
- **Remove a statement**: Delete the string from the `content` list:
  ```python
  "content": [
      "Keep this statement."
  ]
  ```

For **Personal Information**, ensure every detail (e.g., name, email) is on a separate line as a string in the `content` list.

---

### Core Competencies

This section contains a **list of skills** or attributes as its `content`.

#### Example:
```python
{
    "title": "Core Competencies",
    "content": [
        "TCP/IP", "DNS", "DHCP", "Firewalls", "Network Troubleshooting",
        "Packet Analysis", "Windows", "Linux", "Python", "Bash scripting"
    ]
}
```

#### How to Customize:
- **Add a new skill**: Add a new string to the `content` list:
  ```python
  "content": [
      "TCP/IP", "New Skill"
  ]
  ```
- **Remove a skill**: Delete the corresponding string from the list:
  ```python
  "content": [
      "TCP/IP", "Linux"
  ]
  ```
- **Reorder skills**: Move the strings around in the list to adjust their order in the generated resume.

---

### Education

This section is a **nested list**, where each entry is a list that begins with a main string (e.g., degree or institution) followed by additional strings for details (e.g., major, graduation year).

#### Example:
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

#### How to Customize:
- **Add a new institution**: Add a new list to the `content` list:
  ```python
  "content": [
      ["Existing entries..."],
      ["New University: Graduated May 2023", "Degree in Computer Science"]
  ]
  ```
- **Remove an institution**: Delete the entire list entry:
  ```python
  "content": [
      ["Keep this university."]
  ]
  ```
- **Edit details**: Update strings within the nested list:
  ```python
  ["DePaul University: Graduated March 2022",
   "Updated major or detail here."]
  ```

---

### Professional Experience

This section is a **dictionary-based section**, where each job is represented as a dictionary. Each dictionary includes:
- `subtitle`: Job title and company.
- `date`: The date range and location.
- `details`: A list of bullet points describing responsibilities and accomplishments.

#### Example:
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
        }
    ]
}
```

#### How to Customize:
- **Add a new job**: Add a new dictionary to the `content` list:
  ```python
  {
      "subtitle": "New Job Title – New Company",
      "date": "Start Date – End Date, City, State",
      "details": [
          "New responsibility 1.",
          "New accomplishment 2."
      ]
  }
  ```
- **Remove a job**: Delete the dictionary entry:
  ```python
  "content": [
      {"subtitle": "Keep this job."}
  ]
  ```
- **Edit job details**: Update any field (e.g., `subtitle`, `date`, or `details`):
  ```python
  "details": [
      "Updated responsibility or accomplishment."
  ]
  ```

---

### Guidelines for Customization
- **Consistency**: Ensure you follow the structure for each section to avoid syntax errors.
- **String Formatting**: Use double quotes (`"`) for all strings.
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
