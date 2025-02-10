# Resume Generator App

This project is a Python-based resume generator application that allows users to create and customize professional resumes via a graphical interface. Resume data is stored in JSON files and the resume document is generated as a formatted Microsoft Word document (.docx) using the `python-docx` library.

## Project Structure

- **ResumeBuilder.py**  
  The main script that launches the GUI. It enables users to edit resume data, reset to default settings, and generate the resume document.
  
- **data.json**  
  The JSON file that contains the current resume data used by the application.
  
- **default_data.json**  
  The JSON file with the default resume data. This file is used to reset `data.json` if necessary.
  
- **generator.py**  
  A module responsible for generating the formatted Word document based on the selected resume sections.

## Features

- **Editable Resume Data**:  
  Modify resume sections (e.g., Personal Information, Objective, Education, Professional Experience, etc.) directly through the GUI without manually editing code.

- **Dynamic Section Controls**:  
  Enable or disable specific sections using checkboxes, and choose preset or custom objectives via radio buttons and text fields.

- **Professional Document Generation**:  
  Generate a `.docx` resume with appropriate formatting—headers, bullet points, and indented details for education and professional experience.

- **Reset to Default Data**:  
  Easily restore the resume data to its default state using the "Reset to Default Data" option.

- **Cross-Platform Compatibility**:  
  Designed to work on Windows, macOS, and Linux with platform-specific handling for opening files and directories.

## Getting Started

1. **Install Dependencies**

   Ensure you have Python installed and then install the required package:

   ```bash
   pip install python-docx
   ```

2. **Run the Application**

   Launch the application by running:

   ```bash
   python ResumeBuilder.py
   ```

3. **Using the Application**

   - **Edit Resume Data**:  
     Click the "Edit Resume Data" button to open an editor where you can modify the JSON data.
     
   - **Reset Data**:  
     Use the "Reset to Default Data" button to restore the resume data from `default_data.json`.
     
   - **Generate Resume**:  
     Enter a file name and click "Generate Resume" to create a `.docx` file. The generated resume will open automatically (if supported by your operating system).

## Packaging with PyInstaller

To bundle the application as a standalone executable, use the following commands:

- **For Windows**:

   ```bash
   pyinstaller --onefile --noconsole --add-data "data.json;." --add-data "default_data.json;." --add-data "generator.py;." ResumeBuilder.py
   ```

- **For macOS**:

   ```bash
   pyinstaller --onefile --noconsole --add-data "data.json:." --add-data "default_data.json:." --add-data "generator.py:." ResumeBuilder.py
   ```

## Data Format

The resume data is structured in JSON format:

- **Personal Information**:  
  An array of strings containing your contact details.
  
- **Objective**:  
  An array of strings for different career objectives; supports a custom objective option.
  
- **Certifications**:  
  An array of strings listing your certifications.
  
- **Education**:  
  An array of arrays. The first element of each sub-array is the header (e.g., institution and graduation info), and any additional elements provide further details (formatted as indented text in the generated resume).
  
- **Core Competencies**:  
  An array of strings representing your skills.
  
- **Professional Experience**:  
  An array of objects. Each object should include:
  - `subtitle`: Job title and company name.
  - `date`: Date range and location.
  - `details`: An array of strings describing responsibilities and achievements.
  
- **Technical Projects**:  
  An array of strings describing various projects.

## Customization

To update your resume content, modify `data.json` either manually or using the built-in editor available through the application. Make sure the JSON structure is preserved to ensure proper processing by the resume generator.

## License

This project is licensed under the MIT License.

## Contact

For questions, feedback, or support, please contact the developer.

Happy resume generating!
