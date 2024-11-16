import tkinter as tk
from tkinter import ttk, messagebox
from data import master_resume
from generator import generate_resume


class ResumeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Generator")
        self.root.geometry("800x600")

        # Variables to track selections
        self.section_vars = {}  # Main section checkboxes
        self.subsection_vars = {}  # Sub-options checkboxes
        self.custom_objective_var = tk.StringVar()  # Custom objective input
        self.output_file_name_var = tk.StringVar(value="Custom_Resume")  # Default file name

        # Create GUI
        self.create_gui()

    def create_gui(self):
        # Scrollable frame
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add widgets for each section
        for section in master_resume:
            self.add_section_widgets(scrollable_frame, section)

        # Output file name entry
        ttk.Label(scrollable_frame, text="Output File Name:").pack(anchor="w", pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.output_file_name_var, width=30).pack(anchor="w", pady=5)

        # Generate button
        ttk.Button(scrollable_frame, text="Generate Resume", command=self.generate_resume).pack(anchor="center", pady=10)

        # Add scrollable frame and scrollbar to the main window
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_section_widgets(self, parent, section):
        # Add the main section checkbox
        section_var = tk.BooleanVar(value=True)
        self.section_vars[section["title"]] = section_var
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill="x", pady=5)

        section_checkbox = ttk.Checkbutton(
            section_frame, text=section["title"], variable=section_var,
            command=lambda: self.toggle_suboptions(section["title"], section_var.get())
        )
        section_checkbox.pack(anchor="w")

        # Add sub-options (if applicable)
        if "content" in section and isinstance(section["content"], list):
            subsection_frame = ttk.Frame(section_frame)
            subsection_frame.pack(fill="x", padx=20)

            # Handle Objective (special case for prefab and custom input)
            if section["title"] == "Objective":
                self.add_objective_options(subsection_frame, section["content"])
            elif section["title"] == "Education":
                self.add_education_options(subsection_frame, section["content"], section["title"])
            else:
                self.add_suboptions(subsection_frame, section["content"], section["title"])

    def add_objective_options(self, parent, options):
        for option in options:
            var = tk.BooleanVar(value=True)
            self.subsection_vars[option] = var
            ttk.Checkbutton(parent, text=option, variable=var).pack(anchor="w")

        # Custom objective option
        custom_frame = ttk.Frame(parent)
        custom_frame.pack(anchor="w", pady=5)
        custom_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="Custom Objective:", variable=custom_var).pack(side="left")
        ttk.Entry(custom_frame, textvariable=self.custom_objective_var, width=40).pack(side="left")

        self.subsection_vars["Custom Objective"] = custom_var

    def add_education_options(self, parent, education_content, section_title):
        for entry in education_content:
            # Main entry (first item in the list)
            main_entry = entry[0]
            main_var = tk.BooleanVar(value=True)
            self.subsection_vars[(section_title, main_entry)] = main_var
            main_checkbox = ttk.Checkbutton(parent, text=main_entry, variable=main_var)
            main_checkbox.pack(anchor="w")

            # Sub-details (remaining items in the list)
            for detail in entry[1:]:
                detail_var = tk.BooleanVar(value=True)
                self.subsection_vars[(section_title, detail)] = detail_var
                detail_checkbox = ttk.Checkbutton(parent, text=f"    {detail}", variable=detail_var)
                detail_checkbox.pack(anchor="w")

    def add_suboptions(self, parent, options, section_title):
        for option in options:
            if isinstance(option, dict):  # Handle dictionary entries (e.g., Professional Experience)
                subtitle = option["subtitle"]
                var = tk.BooleanVar(value=True)
                self.subsection_vars[(section_title, subtitle)] = var
                ttk.Checkbutton(parent, text=subtitle, variable=var).pack(anchor="w")
            else:  # Handle regular entries
                var = tk.BooleanVar(value=True)
                self.subsection_vars[(section_title, option)] = var
                ttk.Checkbutton(parent, text=option, variable=var).pack(anchor="w")

    def toggle_suboptions(self, section_title, enabled):
        # Enable or disable sub-options when the main section is toggled
        for key, var in self.subsection_vars.items():
            if isinstance(key, tuple) and key[0] == section_title:
                var.set(enabled)

    def generate_resume(self):
        selected_sections = []

        for section in master_resume:
            if self.section_vars[section["title"]].get():
                if section["title"] == "Objective":
                    selected_objectives = [
                        obj for obj, var in self.subsection_vars.items() if var.get() and obj != "Custom Objective"
                    ]
                    if self.subsection_vars["Custom Objective"].get() and self.custom_objective_var.get():
                        selected_objectives.append(self.custom_objective_var.get())
                    section_data = {"title": section["title"], "content": selected_objectives}
                elif section["title"] == "Education":
                    section_content = []
                    for entry in section["content"]:
                        main_entry = entry[0]
                        if self.subsection_vars[(section["title"], main_entry)].get():
                            entry_data = [main_entry]
                            entry_data.extend(
                                detail for detail in entry[1:]
                                if self.subsection_vars[(section["title"], detail)].get()
                            )
                            section_content.append(entry_data)
                    section_data = {"title": section["title"], "content": section_content}
                elif section["title"] == "Professional Experience":
                    section_content = [
                        item for item in section["content"]
                        if self.subsection_vars.get((section["title"], item["subtitle"]), tk.BooleanVar()).get()
                    ]
                    section_data = {"title": section["title"], "content": section_content}
                else:
                    section_data = {
                        "title": section["title"],
                        "content": [
                            option for option in section["content"]
                            if self.subsection_vars.get((section["title"], option), tk.BooleanVar()).get()
                        ]
                    }
                selected_sections.append(section_data)

        # Get output file name
        output_file_name = f"{self.output_file_name_var.get().strip()}.docx"
        generate_resume(selected_sections, output_file=output_file_name)
        messagebox.showinfo("Success", f"Resume generated as {output_file_name}")


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()
