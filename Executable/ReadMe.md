# Resume Generator Guide

Welcome to the Resume Generator!

This tool empowers you to quickly create a custom, professional resume tailored for each job application. Rather than using a one-size-fits-all template, you can handpick exactly which sections, skills, and details to include—ensuring that your resume best fits the role you’re applying for.

---

## **Using the GUI**

When you launch the application (for example, by running `resume_generator.exe` on Windows), you’ll see a toolbar at the top with the following buttons (from left to right):

1. **Customize UI**
   - Opens an interface where you can change the main window title, size, and font.
   - Personalize the appearance and behavior of the application.

2. **Browse Files**
   - Opens the folder containing your resume files and JSON data.
   - Quickly access, back up, or review your data files.

3. **Help**
   - Provides detailed guidance on how to use the application (see full details below).

4. **Reset Data**
   - Restores the resume data to its default state.
   - *Warning:* This will remove all customizations you’ve made.

5. **Advanced JSON Editor**
   - (Advanced) Directly edit the raw JSON data that defines your resume.
   - **Note:** This option is intended for power users only. A confirmation prompt will appear before launching the editor to discourage casual use.

### **Saving and Refreshing**

- Any changes made in an editor are automatically saved, and the main window is fully refreshed. This update includes the window title, size, and font—ensuring that all modifications are applied immediately.

---

## **Editing Resume Data**

The resume data is now stored in JSON files rather than a Python dictionary. The primary file is `data.json` (with `default_data.json` providing the defaults). These files define a variable called `master_resume`, which is a JSON array containing your resume sections.

### **Structure of the JSON Data**

- **JSON Array:**  
  The file contains a list of objects. Each object represents a section of your resume.
  
- **Objects (Sections):**  
  Each object includes keys such as:
  - `"title"`: The name of the section (e.g., "Personal Information").
  - `"content"`: An array of items that represent the content for that section.
  - Optional fields for more complex sections (like `"subtitle"`, `"date"`, or `"details"`) are also supported.

### **Examples**

#### Personal Information Section
```json
{
    "title": "Personal Information",
    "content": [
        "Your Name",
        "City, State ZIP ⋄ Phone ⋄ Email ⋄ Website ⋄ GitHub ⋄ LinkedIn"
    ]
}
```
- Replace `"Your Name"` with your actual name.
- Modify other details (location, phone, LinkedIn URL) accordingly.

#### Core Competencies Section
```json
{
    "title": "Core Competencies",
    "content": [
        "Skill 1",
        "Skill 2",
        "Skill 3"
    ]
}
```
- Update the skills as needed.
- Add or remove items to best reflect your expertise.

#### Professional Experience Section
```json
{
    "title": "Professional Experience",
    "content": [
        {
            "subtitle": "Job Title – Company",
            "date": "Start Date – End Date, Location",
            "details": [
                "Responsibility 1",
                "Responsibility 2"
            ]
        }
    ]
}
```
- Fill in the appropriate job details and responsibilities.

> **Note:** Always maintain the JSON structure as shown to ensure the application functions correctly. Validate your JSON for correct syntax, proper commas, and accurate nesting.

---

## **Advanced Editing**

### **Advanced JSON Editor**

- **Purpose:**  
  For power users, the Advanced JSON Editor allows you to directly modify the raw JSON data in `data.json`.
  
- **Safety:**  
  A confirmation dialog appears before the editor launches, making it clear that this feature is intended only for advanced users.

---

## **Packing with PyInstaller**

To create a standalone executable:

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Generate the Executable**:
   ```bash
   pyinstaller --onefile --name resume_generator resume_generator.py
   ```
   - The `--onefile` flag packages the application into a single executable.
   - Replace `resume_generator.py` with your main script’s filename.

3. **Distribution:**
   - Distribute the resulting executable along with `default_data.json` so users have a default configuration to start with.

---

## **Final Notes**

- **GUI Refresh:**  
  Any changes made through the UI (for example, customizing the UI or editing sections) trigger a full refresh of the main window. This ensures that updates—such as the window title, size, and font—are applied immediately.

- **Support:**  
  If you encounter any issues or have questions, please contact the developer.

Happy resume building!
