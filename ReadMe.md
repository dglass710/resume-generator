# Resume Generator

This project is a Python-based GUI application that allows users to create customizable resumes in Word document format. The application uses the `python-docx` library for document generation and `Tkinter` for the graphical user interface.

---

## Features
- Select from predefined resume sections to include in your final document.
- Customize sections, such as Objectives, with pre-set or custom inputs.
- Flexible layout options for presenting skills, experiences, and education.
- Save the resume as a Word document (`.docx`) with consistent, professional formatting.

---

## How to Customize `data.py`

The `data.py` file contains the default resume data used by the application. Users can modify this file to tailor the sections and content to their specific needs. See the [Customization Guide](#how-to-customize-data.py) for detailed instructions.

---

## Installation Instructions

### 1. Verify Python is Installed
Ensure that Python is installed on your system:
```bash
python --version
```
or
```bash
python3 --version
```

If Python is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).

---

### 2. Check if `python-docx` is Installed

The `python-docx` library is required for this project. To check if it’s installed, open a terminal or command prompt and run:

```bash
python -m pip show python-docx
```
or, depending on your environment:
```bash
python3 -m pip show python-docx
```

- **If `python-docx` is installed**, you will see details like version and location.
- **If it’s not installed**, the command will return nothing.

---

### 3. Install `python-docx`

To install `python-docx`, use the following command:
```bash
python -m pip install python-docx
```
or, for environments where `python3` is used:
```bash
python3 -m pip install python-docx
```

If you are using an environment with a custom Python installation or virtual environment, make sure you use the appropriate Python executable.

---

### 4. Verify the Installation

After installation, verify that `python-docx` is installed by running:
```bash
python -m pip show python-docx
```
or
```bash
python3 -m pip show python-docx
```

You should see details confirming the library is installed, such as:
```
Name: python-docx
Version: 0.8.11
Summary: Create and update Microsoft Word .docx files.
```

---

## Getting Started
1. Ensure `python-docx` is installed as described above.
2. Update the `master_resume` variable in `data.py` to include your personalized information (see the [Customization Guide](#how-to-customize-data.py)).
3. Run the `gui.py` script to launch the GUI:
   ```bash
   python gui.py
   ```
   or
   ```bash
   python3 gui.py
   ```
4. Select the sections and subsections you want to include in your resume.
5. Enter a custom objective (if needed) in the GUI’s text box.
6. Generate your resume and enjoy a professional Word document tailored to your needs!

---

For questions or further assistance, feel free to reach out. Happy customizing!
ustomizing!
