# Resume Generator App

This project is a Python-based resume generator application that allows users to create and customize professional resumes through an intuitive graphical interface. Resume data is stored in JSON files, and a formatted Microsoft Word document (.docx) is generated using the `python-docx` library.

## Project Structure

- **ResumeBuilder.py**  
  The main script that launches the GUI. It enables users to modify resume content via dedicated section editors, reset data to default settings, and generate the resume document.
  
- **data.json**  
  The JSON file containing the current resume data used by the application.
  
- **default_data.json**  
  The JSON file with the default resume data, used to restore `data.json` when necessary.
  
- **generator.py**  
  A module responsible for generating the formatted Word document based on the selected resume sections.

## Features

- **Editable Resume Data**  
  Modify your resume without worrying about JSON syntax. Although advanced users can click "Edit Resume Data" to directly modify the JSON file, most users are encouraged to use the section editors.

- **Section & Item Editors**  
  - **Section Editors:**  
    Click "Edit Section" next to each resume section to open a dedicated editor. Here you can add, edit, remove, and reorder items using intuitive controls (including Up/Down buttons).
  - **Item Editors:**  
    Within a section editor, select an individual item and click "Edit" to open a small item editor. Make your changes, click "Done" to apply them, and then confirm your updates by saving the section editor.

- **Selective Inclusion via Checkboxes**  
  When you update your resume, the main window refreshes with all sections and most subsections checked by default—except for the "Core Competencies" and "Technical Projects" sections. This encourages you to selectively choose the most relevant skills and projects, ensuring a focused, concise resume.

- **Optimized Display of Core Competencies**  
  In the Core Competencies editor, skills are displayed in alphabetical order for easy selection, while in the main window they are arranged into columns in a way that most optimally uses horizontal space.

- **Professional Document Generation**  
  Generate a professionally formatted `.docx` resume with headers, bullet points, and indented details for education and professional experience.

- **Reset to Default Data**  
  Easily restore the resume data to its default state with a single click using the "Reset to Default Data" option.

- **Cross-Platform Compatibility**  
  Designed to work on Windows, macOS, and Linux, with platform-specific handling for opening files and directories.

## Getting Started

1. **Install Dependencies**

   Ensure you have Python installed, then install the required package:

   ```bash
   pip install python-docx
   ```

2. **Run the Application**

   Launch the application by running:

   ```bash
   python ResumeBuilder.py
   ```

3. **Using the Application**

   - **Edit Resume Data (Advanced Users):**  
     The "Edit Resume Data" button opens a raw JSON editor, allowing advanced users to directly modify the JSON file. For most users, however, it’s best to work with the section editors.

   - **Section Editors (Recommended):**  
     For each resume section, click the "Edit Section" button. This opens an editor where you can:
       - Add, edit, and remove items.
       - Reorder items using Up/Down buttons (except for Core Competencies, which are auto-sorted).
       - Save your changes or cancel to discard unsaved modifications.
     Within a section editor, you can also use the item editor (accessed via the "Edit" button) to modify individual entries.

   - **Reset Data:**  
     Use the "Reset to Default Data" button to restore the resume data from `default_data.json`.

   - **Generate Resume:**  
     Enter a file name and click "Generate Resume" to create a `.docx` file. The generated resume will open automatically (if supported by your operating system).

## Building the Application

To build the application as a standalone executable, use the provided build script:

```bash
./build.sh
```

This script will:
1. Detect your operating system (Windows or macOS)
2. Build the appropriate executable using PyInstaller
3. Package it correctly (exe for Windows, app for macOS)
4. Optionally install it locally
5. Commit the changes and optionally push to the remote repository

To update your local repository with the latest changes:

```bash
./update.sh
```

## Data Format

The resume data is structured in JSON format:

- **Personal Information:**  
  An array of strings containing your contact details.
  
- **Objective:**  
  An array of strings for different career objectives, with support for a custom objective option.
  
- **Certifications:**  
  An array of strings listing your certifications.
  
- **Education:**  
  An array of arrays. The first element of each sub-array is the header (e.g., institution and graduation info), and any additional elements provide further details (displayed as indented text in the generated resume).
  
- **Core Competencies:**  
  An array of strings representing your skills. In the section editor, these are displayed in alphabetical order, while in the main window they are arranged into columns that most optimally use horizontal space.
  
- **Professional Experience:**  
  An array of objects. Each object includes:
  - `subtitle`: Job title and company name.
  - `date`: Date range and location.
  - `details`: An array of strings describing responsibilities and achievements.
  
- **Technical Projects:**  
  An array of strings describing various projects. These can be reordered, and by default, their checkboxes start unchecked so you can select only the most relevant projects.

## Customization

To update your resume content, modify `data.json` either manually or (preferably) through the built-in section editors. Using the section editors allows you to focus on what to include without worrying about JSON syntax.

## License

This project is licensed under the MIT License.

## Contact

For questions, feedback, or support, please contact the developer.

Happy resume generating!
