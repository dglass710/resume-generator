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

## Using PyInstaller to Bundle the Application

To distribute the application as a standalone executable, PyInstaller can be used to bundle it. Below are platform-specific instructions for creating the executable, including how to include additional data files.

### PyInstaller Command for Windows

For Windows, the command uses a semicolon (`;`) to separate the source and destination paths for additional data files.

```bash
pyinstaller --onefile --noconsole --add-data "data.py;." --add-data "default_data.py;." --add-data "generator.py;." ResumeBuilder.py
```

#### Explanation:
- `--onefile`: Create a single bundled executable.
- `--noconsole`: Suppress the console window when running the executable.
- `--add-data`: Add additional data files to the bundle. The format is `source_path;destination_path`:
  - Use `;` as the separator on Windows.
  - Example: `"data.py;."` includes `data.py` in the root of the bundle.
- `ResumeBuilder.py`: The name of your main script.

---

### PyInstaller Command for macOS

For macOS, the command uses a colon (`:`) to separate the source and destination paths for additional data files.

```bash
pyinstaller --onefile --noconsole --add-data "data.py:." --add-data "default_data.py:." --add-data "generator.py:." ResumeBuilder.py
```

#### Explanation:
- `--onefile`: Create a single bundled executable.
- `--noconsole`: Suppress the console window when running the executable.
- `--add-data`: Add additional data files to the bundle. The format is `source_path:destination_path`:
  - Use `:` as the separator on macOS.
  - Example: `"data.py:."` includes `data.py` in the root of the bundle.
- `ResumeBuilder.py`: The name of your main script.

---

### Summary
- **Windows**: Use `;` for the `--add-data` separator.
  ```bash
  pyinstaller --onefile --noconsole --add-data "data.py;." --add-data "default_data.py;." --add-data "generator.py;." ResumeBuilder.py
  ```
- **macOS**: Use `:` for the `--add-data` separator.
  ```bash
  pyinstaller --onefile --noconsole --add-data "data.py:." --add-data "default_data.py:." --add-data "generator.py:." ResumeBuilder.py
  ```

This ensures that the PyInstaller command is customized for the platform you are working on, allowing proper inclusion of additional files.

---

## Customizing `data.py`

The `data.py` file contains the default resume data used by the application. You can modify this file to tailor the sections and content to your specific needs. The order of the dictionaries in the `master_resume` list determines the order of sections in both the GUI and the generated resume.

### Objective, Certifications, and Personal Information

These sections use **lists of strings** to define their `content`. Each string must be enclosed in double quotes (`"`) and separated by a comma.

#### Example:
```python
{
    "title": "Objective",
    "content": [
        "Highly motivated IT professional with a strong foundation in mathematics, computer science, and cybersecurity.",
        "Seeking a challenging role in IT operations, leveraging my cybersecurity and troubleshooting skills to ensure seamless system performance."
    ]
}
```

---

### Core Competencies

This section uses a **list of strings** to define skills or attributes. Each string must be enclosed in double quotes and separated by a comma.

#### Example:
```python
{
    "title": "Core Competencies",
    "content": [
        "TCP/IP", "DNS", "DHCP", "Firewalls", "Python", "Bash scripting"
    ]
}
```

---

### Education

This section uses a **list of lists**, where each inner list contains a main string (e.g., degree or institution) followed by additional strings for details.

#### Example:
```python
{
    "title": "Education",
    "content": [
        ["Northwestern University Cybersecurity Program: Graduated June 2024"],
        ["DePaul University: Graduated March 2022", "B.S. in Applied and Computational Mathematics"]
    ]
}
```

---

### Professional Experience

This section uses a **list of dictionaries**, where each dictionary represents a job or project.

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

---

### Guidelines for Customization

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

zing!

## Running PyInstaller

When creating an executable with PyInstaller, the commands vary slightly between Windows and macOS due to differences in path separators. Below are the platform-specific commands:

### PyInstaller Command for Windows

For Windows, use a semicolon (`;`) to separate the source and destination paths for additional data files.

```bash
pyinstaller --onefile --noconsole --add-data "data.py;." --add-data "default_data.py;." --add-data "generator.py;." ResumeBuilder.py
```

**Explanation**:
- `--onefile`: Creates a single bundled executable.
- `--noconsole`: Suppresses the console window when running the executable.
- `--add-data`: Includes additional data files in the bundle. The format is `"source_path;destination_path"`:
  - Use `;` as the separator on Windows.
  - Example: `"data.py;."` includes `data.py` in the root of the bundle.
- `ResumeBuilder.py`: The name of your main script.

### PyInstaller Command for macOS

For macOS, use a colon (`:`) to separate the source and destination paths for additional data files.

```bash
pyinstaller --onefile --noconsole --add-data "data.py:." --add-data "default_data.py:." --add-data "generator.py:." ResumeBuilder.py
```

**Explanation**:
- `--onefile`: Creates a single bundled executable.
- `--noconsole`: Suppresses the console window when running the executable.
- `--add-data`: Includes additional data files in the bundle. The format is `"source_path:destination_path"`:
  - Use `:` as the separator on macOS.
  - Example: `"data.py:."` includes `data.py` in the root of the bundle.
- `ResumeBuilder.py`: The name of your main script.

### Summary

- **Windows**: Use `;` for the `--add-data` separator:
  ```bash
  pyinstaller --onefile --noconsole --add-data "data.py;." --add-data "default_data.py;." --add-data "generator.py;." ResumeBuilder.py
  ```
- **macOS**: Use `:` for the `--add-data` separator:
  ```bash
  pyinstaller --onefile --noconsole --add-data "data.py:." --add-data "default_data.py:." --add-data "generator.py:." ResumeBuilder.py
  ```

By tailoring the PyInstaller command for your operating system, you ensure the correct inclusion of additional data files and a seamless executable build process.
