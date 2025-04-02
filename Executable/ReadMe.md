# Resume Generator Guide

Welcome to the Resume Generator!

This tool empowers you to quickly create a custom, professional resume tailored for each job application. Rather than using a one-size-fits-all template, you can handpick exactly which sections, skills, and details to include—ensuring that your resume best fits the role you’re applying for.

---

## What's New

- **Improved Structured Section Editing:**  
  In the structured section editors for **Education** and **Professional Experience**, editing an entry now replaces the existing item rather than appending a new one. This change ensures that your modifications update the correct entry.

- **Drag and Drop Reordering:**  
  You can now drag and drop items within structured sections (Education and Professional Experience) to reorder them. Simply click on an item in the list and drag it to your desired position.

---

## **Using the GUI**

When you launch the application (for example, by running the executable on your system), you’ll see a toolbar at the top with the following buttons (from left to right):

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
   - **Advanced Feature:** This option allows you to directly edit the raw JSON data that defines your resume.
   - A confirmation prompt appears before launching this editor to ensure that only experienced users proceed.

### **Saving and Refreshing**

- Any changes made in an editor are automatically saved, and the main window is fully refreshed. This update includes the window title, size, and font—ensuring that all modifications are applied immediately.

---

## **Editing Resume Data (Advanced)**

*Note: Editing the resume data directly is an advanced feature intended for experienced users. The resume data is stored in JSON files, with `data.json` containing the active configuration and `default_data.json` providing a default version.*

### **Structure of the JSON Data**

- **JSON Array:**  
  The file contains a list of objects. Each object represents a section of your resume.
  
- **Objects (Sections):**  
  Each object includes keys such as:
  - `"title"`: The name of the section (e.g., "Personal Information").
  - `"content"`: An array of items that represent the content for that section.
  - Additional keys (like `"subtitle"`, `"date"`, or `"details"`) may be present for more complex sections.

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

> **Important:** Always maintain the JSON structure as shown to ensure the application functions correctly. Validate your JSON for proper syntax and structure before saving your changes.

---

## **Final Notes**

- **GUI Refresh:**  
  Any changes made through the GUI (such as customizing the UI, editing sections, or reordering items via drag and drop) trigger a full refresh of the main window. This ensures that updates—such as changes to the window title, size, and font—are applied immediately.

- **Support:**  
  If you encounter any issues or have questions, please contact the developer.

Happy resume building!
