import tkinter as tk
import platform
import subprocess
from tkinter import ttk, messagebox
import os
import sys
import importlib
from math import ceil
import data
from data import master_resume
from generator import generate_resume


class ResumeGeneratorGUI:
    def __init__(self, root):
        # Attempt to restore previous session data from users app data directory when running in a bundled executable
        if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
            self.persistent_data_path = os.path.join(self.get_app_directory(), 'data.py')
            if os.path.isfile(self.persistent_data_path):
                content = ''
                with open(self.persistent_data_path) as f:
                    content += f.read()
                with open(os.path.join(sys._MEIPASS, 'data.py'), 'w') as f:
                    f.write(content)

        self.root = root
        self.editor_windows = {} # Dictionary to keep track of open editor windows
        self.load_master_resume()
        if master_resume[0].get("window_title"):
            self.root.title(master_resume[0]["window_title"])
        else:
            self.root.title("Resume Generator")

        # Set window dimensions
        self.set_dimensions()


        # Variables to track selections
        self.section_vars = {}  # Main section checkboxes
        self.subsection_vars = {}  # Sub-options checkboxes
        self.selected_objective = tk.StringVar()  # For mutually exclusive Objective options
        self.custom_objective_var = tk.StringVar()  # Custom objective input
        self.output_file_name_var = tk.StringVar(value="Custom_Resume")  # Default file name

        # Create the GUI
        self.create_gui()

    def set_dimensions(self):
        try:
            width = int(master_resume[0]["window_width"])
            length = int(master_resume[0]["window_length"])
            self.root.geometry(f"{width}x{length}")
        except:
            self.root.geometry("600x700")

    def get_file_path(self, filename):
        if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)

    def load_master_resume(self):
        """Load the current version of master_resume from data.py."""
        global master_resume
        try:
            with open(self.get_file_path('data.py'), "r") as f:
                content = f.read()
                exec(content, globals())  # Execute data.py content to update master_resume
            # Update the dimensions of all open editor windows
            self.update_editor_window_dimensions()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data from data.py: {e}")

    def update_editor_window_dimensions(self):
        try:
            width = int(master_resume[0]["editor_window_width"])
            length = int(master_resume[0]["editor_window_length"])
        except:
            width, length = 600, 700  # Fallback dimensions
        for editor_window in self.editor_windows.keys():
            if editor_window.winfo_exists():
                editor_window.geometry(f"{width}x{length}")
            else:
                self.close_editor_window(editor_window)

    def open_directory(self, path):
        """
        Opens the given directory in the file viewer of the operating system.

        :param path: The directory path to open.
        """
        if not os.path.isdir(path):
            raise ValueError(f"The path '{path}' is not a valid directory.")

        system = platform.system()

        try:
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", path], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", path], check=True)
            else:
                raise NotImplementedError(f"Opening directories is not supported on {system} OS.")
        except Exception as e:
            print(f"An error occurred while trying to open the directory: {e}")

    def open_app_directory(self):
        self.open_directory(self.get_app_directory())


    def get_app_directory(self):
        """
        Get the correct path for storing app-related files in the Documents folder.

        Returns:
            str: The absolute path to the application-specific directory inside Documents.
        """
        # Get the user's Documents folder path in a cross-platform manner
        documents_folder = os.path.expanduser("~/Documents")

        # Define the name of your app-specific subdirectory
        app_folder_name = "ResumeGeneratorApp"

        # Construct the full path to the app directory
        app_directory = os.path.join(documents_folder, app_folder_name)

        # Create the directory if it doesn't exist
        if not os.path.exists(app_directory):
            os.makedirs(app_directory)

        return app_directory


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
            with open(self.get_file_path("default_data.py"), "r") as f:
                default_content = f.read()
    
            # Write the default content to data.py
            with open(self.get_file_path("data.py"), "w") as f:
                f.write(default_content)

            # If running inside a bundled executable
            if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
                with open(self.persistent_data_path, 'w') as f:
                    f.write(default_content)
        
            messagebox.showinfo("Success", "Resume data has been reset to the default successfully!")
    
            # Reload the updated data and refresh the GUI
            self.load_master_resume()
    
            # Clear and Rebuild the GUI Based on Updated Data for the MAIN window only
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):  # Skip clearing the editor window
                    continue
                widget.destroy()
    
            # Recreate the GUI with updated data
            self.create_gui()
    
        except Exception as e:
            messagebox.showerror("Error", f"Could not reset to default data: {e}")

    def open_information_window(self):
        """
        Create an informational window to explain how to use this application
        """
        # Create a new Toplevel window
        information_window = tk.Toplevel(self.root)
        information_window.title("Information")
        information_window.geometry("600x500")
    
        # Create a Text widget to display information
        info_text = tk.Text(information_window, wrap="word", font=("Arial", 12), state="normal")
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
    
        # Add a scrollbar for the Text widget
        scrollbar = ttk.Scrollbar(information_window, command=info_text.yview)
        scrollbar.pack(side="right", fill="y")
        info_text.configure(yscrollcommand=scrollbar.set)
    
        # Information text to display
        information_content = (
            "Welcome to the Resume Generator App!\n\n"
            "This application helps you customize and generate professional resumes "
            "based on a template. Here's how you can use the app:\n\n"
            "1. **Edit Resume Data**: Click the 'Edit Resume Data' button to modify the content "
            "of the resume template. This will open an editor where you can make changes.\n\n"
            "2. **Reset to Default Data**: If you want to start over, use this button to reset "
            "the resume data to its original state. Note: This action will erase all custom changes.\n\n"
            "3. **Objective Selection**: Choose from predefined objective statements or create a "
            "custom one by selecting 'Custom Objective' and entering your own text.\n\n"
            "4. **Selecting Sections**: Use checkboxes to include or exclude specific sections "
            "or subsections from the resume. This allows you to tailor the resume to your needs.\n\n"
            "5. **Generate Resume**: Enter a file name for the generated resume (without extension) "
            "and click 'Generate Resume'. The resume will be created as a .docx file.\n\n"
            "6. **Information Window**: This window provides an overview of how to use the app.\n\n"
            "7. **Navigation**: Scroll through the sections using the scrollbar on the right. "
            "Ensure all desired sections are selected before generating the resume.\n\n"
            "8. **Where Your Files Are Stored**:\n"
            "   - All the files related to this app, including your custom template file (called 'data.py') "
            "and any resumes you create (saved as .docx files), will be in one specific folder.\n\n"
            "   - Here's how to find it:\n"
            "     1. Open your **Documents** folder.\n"
            "     2. Look for a folder named **ResumeGeneratorApp**.\n"
            "     3. Inside this folder, you'll see:\n"
            "        - The 'data.py' file, which stores your resume template.\n"
            "        - Any resumes you've generated, saved as .docx files.\n\n"
            "   Keeping everything in this folder helps you stay organized and ensures all your work is easy to find.\n\n"
            "For additional help or feedback, contact the developer."
        )

        # Insert the information content into the Text widget
        info_text.insert("1.0", information_content)

        # Disable editing for the Text widget
        info_text.configure(state="disabled")

    def open_editor_window(self):
        """
        Create a new editor window for editing the full content of data.py.
        Track the editor window and its associated Text widget for updates.
        """
        # Create a new Toplevel window
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Edit Resume Data")
        
        # Set window dimensions based on master_resume settings
        try:
            width = int(master_resume[0]["editor_window_width"])
            length = int(master_resume[0]["editor_window_length"])
            editor_window.geometry(f"{width}x{length}")
        except:
            editor_window.geometry("600x700")
    
        # Bind the close event to ensure proper cleanup
        editor_window.protocol("WM_DELETE_WINDOW", lambda: self.close_editor_window(editor_window))
    
        # Create a Text widget for editing the content of data.py
        data_text = tk.Text(editor_window, wrap="word", font=("Courier", 10))
        data_text.pack(fill="both", expand=True, padx=10, pady=10)
    
        # Load the content of data.py into the Text widget
        try:
            with open(self.get_file_path("data.py"), "r") as f:
                content = f.read()
                data_text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data.py: {e}")
            editor_window.destroy()
            return
    
        # Store the editor window and its associated Text widget in the tracking dictionary
        self.editor_windows[editor_window] = {"text_widget": data_text}
    
        # Add a Save button to save changes back to data.py
        save_button = ttk.Button(
            editor_window, 
            text="Save Changes", 
            command=lambda: self.save_changes(editor_window)  # Pass the current editor window
        )
        save_button.pack(anchor="center", pady=10)

    def close_editor_window(self, editor_window):
        if editor_window in self.editor_windows:
            del self.editor_windows[editor_window]
        editor_window.destroy()

    def create_gui(self):
        # Top frame for edit and reset buttons
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)

        # Buttons in the top frame
        ttk.Button(top_frame, text="Edit Resume Data", command=self.open_editor_window).pack(side="left", padx=10)
        ttk.Button(top_frame, text="Reset to Default Data", command=self.reset_to_default).pack(side="left", padx=10)
        ttk.Button(top_frame, text="View Files", command=self.open_app_directory).pack(side="left", padx=10)
        ttk.Button(top_frame, text="Information", command=self.open_information_window).pack(side="left", padx=10)

        # Main container for scrollable frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Scrollable frame
        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add scrollable frame to canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the scrollable frame and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel scrolling
        self.canvas.bind("<Enter>", self.bind_mousewheel)  # Enable scrolling when the mouse enters
        self.canvas.bind("<Leave>", self.unbind_mousewheel)  # Disable scrolling when the mouse leaves

        # Add widgets for each section
        for section in master_resume:
            self.add_section_widgets(self.scrollable_frame, section)

        # Bottom container for output file entry and generate button
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", pady=10)

        # Output file name entry and generate button
        ttk.Label(bottom_frame, text="Output File Name:").pack(side="left", padx=5)
        ttk.Entry(bottom_frame, textvariable=self.output_file_name_var, width=30).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Generate Resume", command=self.generate_resume).pack(side="left", padx=10)

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

        if getattr(sys, 'frozen', False):
            # If running as a bundled executable, use the Documents directory
            output_directory = self.get_app_directory()  # NEW LINE: USE DOCUMENTS/APP-SPECIFIC DIRECTORY IF FROZEN
        else:
            # If running as a regular Python script, use the current working directory
            output_directory = os.path.dirname(os.path.abspath(__file__))  # NEW LINE: USE CURRENT FILE DIRECTORY IF NOT FROZEN

        # Get output file name
        output_file_name = f"{self.output_file_name_var.get().strip()}.docx"
        output_file_path = os.path.join(output_directory, output_file_name)  # NEW LINE


        # Open the generated file using the 'open' command
        try:
            generate_resume(selected_sections, output_file=output_file_path) 

            if os.name == 'posix':  # macOS/Linux
                os.system(f'open "{output_file_path}"')
            elif os.name == 'nt':  # Windows
                os.startfile(output_file_path)
            else:
                print(f"Resume generated as {output_file_name}. Please open it manually.")
        except Exception as e:
            print(f"An error occurred while trying to open the file: {e}")

    def save_changes(self, editor_window):
        """
        Save changes made in the editor window to data.py, reload the updated data,
        and refresh all editor windows and the main GUI.
        """
        # Ensure the editor window exists in the tracking dictionary
        if editor_window not in self.editor_windows:
            messagebox.showerror("Error", "Editor window not found.")
            return
    
        # Retrieve the Text widget associated with the editor window
        data_text = self.editor_windows[editor_window]["text_widget"]
    
        # Get the updated content from the Text widget
        updated_content = data_text.get("1.0", tk.END).strip()
    
        # Write the updated content back to data.py
        try:
            with open(self.get_file_path("data.py"), "w") as f:
                f.write(updated_content)

            if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
                with open(self.persistent_data_path, 'w') as f:
                    f.write(updated_content)

            # Reload the updated data.py file and update master_resume
            self.load_master_resume()
    
            # Update main window dimensions
            self.set_dimensions()
    
            # Clear and rebuild the GUI based on updated data for the main window only
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):  # Skip clearing the editor windows
                    continue
                widget.destroy()
    
            # Recreate the main GUI with updated data
            self.create_gui()
    
            # Update the content of all open editor windows
            for editor_win, data in self.editor_windows.items():
                text_widget = data["text_widget"]
                if editor_win.winfo_exists():  # Check if the window still exists
                    try:
                        with open(self.get_file_path("data.py"), "r") as f:
                            new_content = f.read()
                            text_widget.delete("1.0", tk.END)  # Clear current content
                            text_widget.insert("1.0", new_content)  # Insert updated content
                    except Exception as e:
                        print(f"Failed to update content in editor window: {e}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not save changes: {e}")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()




















