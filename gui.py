import tkinter as tk
from tkinter import ttk, messagebox
import os
import importlib
from math import ceil
import data
from data import master_resume
from generator import generate_resume


class ResumeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.load_master_resume()
        if master_resume[0].get("window_title"):
            self.root.title(master_resume[0]["window_title"])
        else:
            self.root.title("Resume Generator")
        self.root.geometry("800x1000")

        # Button to open the Editor Window
        ttk.Button(self.root, text="Edit Resume Data", command=self.open_editor_window).pack(anchor="center", pady=10)

        # Button to reset resume data to default
        ttk.Button(self.root, text="Reset to Default Data", command=self.reset_to_default).pack(anchor="center", pady=10)

        # Variables to track selections
        self.section_vars = {}  # Main section checkboxes
        self.subsection_vars = {}  # Sub-options checkboxes
        self.selected_objective = tk.StringVar()  # For mutually exclusive Objective options
        self.custom_objective_var = tk.StringVar()  # Custom objective input
        self.output_file_name_var = tk.StringVar(value="Custom_Resume")  # Default file name

        # Create GUI
        self.create_gui()

    def load_master_resume(self):
        """Load the current version of master_resume from data.py."""
        global master_resume
        try:
            with open("data.py", "r") as f:
                content = f.read()
                exec(content, globals())  # Execute data.py content to update master_resume
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data from data.py: {e}")

    def reset_to_default(self):
        """Reset the resume data to default using default_data.py."""
        # Show a confirmation dialog to warn the user about resetting data
        confirm_reset = messagebox.askyesno(
                "Confirm Reset to Default",
                "This will reset the resume data to the default version, wiping all personal information.\n\n"
                "Please make sure you have saved your data elsewhere if needed.\n\n"
                "Are you sure you want to proceed?"
                )
    
        if not confirm_reset:
            return  # If the user selects "No", just exit the function
    
        try:
            # Read from default_data.py
            with open("default_data.py", "r") as f:
                default_content = f.read()
    
            # Write the default content to data.py
            with open("data.py", "w") as f:
                f.write(default_content)
    
            messagebox.showinfo("Success", "Resume data has been reset to the default successfully!")
    
            # Reload the updated data and refresh the GUI
            self.load_master_resume()
    
            # Clear and Rebuild the GUI Based on Updated Data for the MAIN window only
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):  # Skip clearing the editor window
                    continue
                widget.destroy()
    
            # Add buttons to open the editor and reset data to default
            self.add_top_buttons()
    
            # Recreate the GUI with updated data
            self.create_gui()
    
        except Exception as e:
            messagebox.showerror("Error", f"Could not reset to default data: {e}")

    def open_editor_window(self):
        # Create a new window for editing the full content of data.py
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Edit Resume Data")
        editor_window.geometry("800x600")

        # Create a Text widget to display and edit the full content of data.py
        self.data_text = tk.Text(editor_window, wrap="word", font=("Courier", 10))
        self.data_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Load the content of data.py
        try:
            with open("data.py", "r") as f:
                content = f.read()
                self.data_text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data.py: {e}")
            editor_window.destroy()
            return

        # Add a Save button to save changes to data.py
        save_button = ttk.Button(editor_window, text="Save Changes", command=self.save_changes)
        save_button.pack(anchor="center", pady=10)

    def create_gui(self):
        # Scrollable frame
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
                "<Configure>",
                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Add mouse wheel scrolling
        self.canvas.bind("<Enter>", self.bind_mousewheel)  # Bind mousewheel on hover
        self.canvas.bind("<Leave>", self.unbind_mousewheel)  # Unbind when leaving

        # Add widgets for each section
        for section in master_resume:
            self.add_section_widgets(self.scrollable_frame, section)

        # Output file name entry
        ttk.Label(self.scrollable_frame, text="Output File Name:").pack(anchor="w", pady=5)
        ttk.Entry(self.scrollable_frame, textvariable=self.output_file_name_var, width=30).pack(anchor="w", pady=5)

        # Generate button
        ttk.Button(self.scrollable_frame, text="Generate Resume", command=self.generate_resume).pack(anchor="center", pady=10)

        # Add scrollable frame and scrollbar to the main window
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def bind_mousewheel(self, event=None):
        """Bind mouse wheel scrolling to the canvas."""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # Windows/Linux
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_mac)  # macOS scroll up
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_mac)  # macOS scroll down

    def unbind_mousewheel(self, event=None):
        """Unbind mouse wheel scrolling from the canvas."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling (Windows/Linux)."""
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            self.canvas.yview_scroll(1, "units")  # Scroll down

    def on_mousewheel_mac(self, event):
        """Handle mouse wheel scrolling (macOS)."""
        if event.num == 4:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            self.canvas.yview_scroll(1, "units")

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

    def save_changes(self):
        # Get the updated content from the text widget
        updated_content = self.data_text.get("1.0", tk.END).strip()
    
        # Write the updated content back to data.py
        try:
            with open("data.py", "w") as f:
                f.write(updated_content)
    
            # Reload the updated data.py file and update master_resume
            self.load_master_resume()
    
            # Clear and Rebuild the GUI Based on Updated Data for the MAIN window only
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):  # Skip clearing the editor window
                    continue
                widget.destroy()
    
            # Add buttons to open the editor and reset data to default
            self.add_top_buttons()
    
            # Recreate the GUI with updated data
            self.create_gui()
    
        except Exception as e:
            messagebox.showerror("Error", f"Could not save changes: {e}")


    def add_top_buttons(self):
        """Add buttons to open the editor and reset resume data to default."""
        # Button to open the Editor Window
        ttk.Button(self.root, text="Edit Resume Data", command=self.open_editor_window).pack(anchor="center", pady=10)
    
        # Button to reset resume data to default
        ttk.Button(self.root, text="Reset to Default Data", command=self.reset_to_default).pack(anchor="center", pady=10)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()












