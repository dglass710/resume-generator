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

These sections use **lists of strings** to define their `content`. Each string must be enclosed in double quotes (`"`) and separated by a comma. While putting each item on a new line promotes readability, the critical part of the syntax is ensuring the strings are properly quoted and comma-separated.

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
- **Add a new statement**:
  ```python
  "content": [
      "Existing statement 1.",
      "New statement here."
  ]
  ```
- **Remove a statement**:
  ```python
  "content": [
      "Keep this statement."
  ]
  ```
- **Ensure proper syntax**:
  - All strings must be enclosed in double quotes.
  - Each string must end with a comma unless it’s the last item in the list.

---

### Core Competencies

This section uses a **list of strings** to define skills or attributes. Each string must be enclosed in double quotes and separated by a comma.

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
- **Add a new skill**:
  ```python
  "content": [
      "TCP/IP", "New Skill"
  ]
  ```
- **Remove a skill**:
  ```python
  "content": [
      "TCP/IP", "Linux"
  ]
  ```
- **Ensure proper syntax**:
  - Each skill must be enclosed in double quotes.
  - Use commas to separate the skills.

---

### Education

This section uses a **list of lists**, where each inner list contains a main string (e.g., degree or institution) followed by additional strings for details. Each list must be separated by a comma, and the strings inside each list must be enclosed in double quotes and separated by commas.

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
- **Add a new institution**:
  ```python
  "content": [
      ["Existing institution..."],
      ["New University: Graduated May 2023", "Degree in Computer Science"]
  ]
  ```
- **Remove an institution**:
  ```python
  "content": [
      ["Keep this university."]
  ]
  ```
- **Edit details**:
  ```python
  ["DePaul University: Graduated March 2022",
   "Updated major or detail here."]
  ```
- **Formatting in the resume**:
  - The first string in each list appears unindented.
  - Additional strings appear indented on the following lines.

---

### Professional Experience

This section uses a **list of dictionaries**, where each dictionary represents a job or project. Each dictionary must have three keys:
1. **`subtitle`**: A string representing the job title and company.
2. **`date`**: A string representing the employment dates and location.
3. **`details`**: A list of strings describing the responsibilities and accomplishments.

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
- **Add a new job**:
  ```python
  "content": [
      {
          "subtitle": "New Job Title – New Company",
          "date": "Start Date – End Date, City, State",
          "details": [
              "New responsibility 1.",
              "New accomplishment 2."
          ]
      }
  ]
  ```
- **Remove a job**:
  ```python
  "content": [
      {"subtitle": "Keep this job."}
  ]
  ```
- **Edit job details**:
  - Ensure the `subtitle` and `date` fields are strings enclosed in double quotes.
  - Ensure `details` is a list of strings, with each string enclosed in double quotes and separated by commas:
    ```python
    "details": [
        "Updated responsibility or accomplishment."
    ]
    ```
- **Ensure proper syntax**:
  - The dictionary keys (`subtitle`, `date`, `details`) must be enclosed in double quotes.
  - The `details` key must contain a list of strings.

---

## Guidelines for Customization
- **Consistency**: Follow the defined structure for each section to avoid syntax errors.
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
