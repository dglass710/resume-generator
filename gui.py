import tkinter as tk
from tkinter import ttk
import os
from math import ceil
from data import master_resume
from generator import generate_resume


class ResumeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Analyst")
        self.root.geometry("800x1000")

        # Variables to track selections
        self.section_vars = {}  # Main section checkboxes
        self.subsection_vars = {}  # Sub-options checkboxes
        self.selected_objective = tk.StringVar()  # For mutually exclusive Objective options
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
            # Special case: Personal Information has no sub-options
            if section["title"] == "Personal Information":
                return  # Skip adding sub-options for this section

            subsection_frame = ttk.Frame(section_frame)
            subsection_frame.pack(fill="x", padx=20)

            if section["title"] == "Objective":
                self.add_objective_options(subsection_frame, section["content"])
            elif section["title"] == "Education":
                self.add_education_options(subsection_frame, section["content"], section["title"])
            else:
                self.add_suboptions(subsection_frame, section["content"], section["title"])

    def add_personal_info(self, parent, content):
        for line in content:
            # Display each line as a wrapped label
            ttk.Label(parent, text=line, wraplength=500).pack(anchor="w", pady=2)

    def add_objective_options(self, parent, options):
        # Create radio buttons for prefab options
        for option in options:
            # Display each objective as a multi-line label
            label_frame = ttk.Frame(parent)
            label_frame.pack(anchor="w", pady=2)
            ttk.Radiobutton(
                label_frame, variable=self.selected_objective, value=option
            ).pack(side="left")
            ttk.Label(label_frame, text=option, wraplength=500).pack(side="left")

        # Custom objective option with a Text widget
        custom_frame = ttk.Frame(parent)
        custom_frame.pack(anchor="w", pady=5)
        ttk.Radiobutton(
            custom_frame, variable=self.selected_objective, value="Custom"
        ).pack(side="left")
        ttk.Label(custom_frame, text="Custom Objective:").pack(side="left")

        # Use a Text widget for multi-line input
        self.custom_objective_text = tk.Text(custom_frame, height=5, width=50, wrap="word")
        self.custom_objective_text.pack(side="left", padx=5)

        # Set default selection to the first prefab option
        if options:
            self.selected_objective.set(options[0])

    def add_education_options(self, parent, education_content, section_title):
        for entry in education_content:
            # Create a single checkbox for the entire entry
            main_entry = entry[0]
            var = tk.BooleanVar(value=True)
            self.subsection_vars[(section_title, main_entry)] = var

            # Display the first item only
            ttk.Checkbutton(parent, text=main_entry, variable=var).pack(anchor="w")

    def add_suboptions(self, parent, options, section_title):
        if section_title == "Core Competencies":
            # Sort options by string length (longest first)
            sorted_options = sorted(options, key=len, reverse=True)
            n = len(sorted_options)  # Total number of options

            # Initialize the rearranged list with placeholders
            rearranged_options = [None] * n

            # Fill middle column indexes: Start at 1, increment by 3
            middle_column_indexes = range(1, n, 3)
            for i, index in enumerate(middle_column_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[i]

            # Fill first column indexes: Start at 0, increment by 3
            first_column_indexes = range(0, n, 3)
            for i, index in enumerate(first_column_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[len(middle_column_indexes) + i]

            # Fill last column indexes: Start at 2, increment by 3
            last_column_indexes = range(2, n, 3)
            for i, index in enumerate(last_column_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[len(middle_column_indexes) + len(first_column_indexes) + i]

            # Split rearranged options into three columns
            num_columns = 3
            columns = [[] for _ in range(num_columns)]

            for idx, option in enumerate(rearranged_options):
                if option:  # Skip None placeholders
                    columns[idx % num_columns].append(option)

            # Create a frame for Core Competencies
            core_frame = ttk.Frame(parent)
            core_frame.pack(fill="x", padx=20)

            # Add columns to the GUI
            for col_idx, column in enumerate(columns):
                column_frame = ttk.Frame(core_frame)
                column_frame.pack(side="left", padx=10, anchor="n")  # Align to the top

                for option in column:
                    var = tk.BooleanVar(value=True)
                    self.subsection_vars[(section_title, option)] = var
                    ttk.Checkbutton(column_frame, text=option, variable=var).pack(anchor="w")
        else:
            # Default behavior for other sections
            for option in options:
                if isinstance(option, dict):  # Handle dictionaries (e.g., Professional Experience)
                    subtitle = option["subtitle"]
                    var = tk.BooleanVar(value=True)
                    self.subsection_vars[(section_title, subtitle)] = var
                    ttk.Checkbutton(parent, text=subtitle, variable=var).pack(anchor="w")
                else:  # Handle regular strings
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
                # Automatically include all fields for Personal Information
                if section["title"] == "Personal Information":
                    section_data = {"title": section["title"], "content": section["content"]}
                elif section["title"] == "Objective":
                    selected_objectives = []
                    if self.selected_objective.get() == "Custom":
                        # Fetch text from the Text widget and strip unnecessary whitespace
                        custom_text = self.custom_objective_text.get("1.0", tk.END).strip()
                        if custom_text:  # Only add if custom text is not empty
                            selected_objectives.append(custom_text)
                    else:
                        selected_objectives.append(self.selected_objective.get())
                    section_data = {"title": section["title"], "content": selected_objectives}
                elif section["title"] == "Education":
                    section_content = []
                    for entry in section["content"]:
                        main_entry = entry[0]
                        if self.subsection_vars[(section["title"], main_entry)].get():
                            # Add the main entry (unindented) and additional elements (indented)
                            entry_data = [main_entry]
                            entry_data.extend(entry[1:])
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

        # Open the generated file using the 'open' command
        try:
            if os.name == 'posix':  # macOS/Linux
                os.system(f'open "{output_file_name}"')
            elif os.name == 'nt':  # Windows
                os.startfile(output_file_name)
            else:
                print(f"Resume generated as {output_file_name}. Please open it manually.")
        except Exception as e:
            print(f"An error occurred while trying to open the file: {e}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()
