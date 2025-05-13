#!/usr/bin/env python3
"""
ResumeGenerator.py

This is the main GUI file for the Resume Generator application. 
It lets users edit their resume data (stored in JSON),
customize which sections and items to include, and generate a
formatted Word document resume.
"""

import tkinter as tk
import json
import platform
import subprocess
from tkinter import ttk, messagebox
import os
import sys
import copy
from datetime import datetime
from generator import Generator  # Uses python-docx to create the resume document

class ResumeGeneratorGUI:
    def __init__(self, root):
        # When running as a bundled executable, restore persistent data from the app directory.
        if getattr(sys, 'frozen', False):
            self.persistent_data_path = os.path.join(self.get_app_directory(), 'data.json')
            if os.path.isfile(self.persistent_data_path):
                with open(self.persistent_data_path, 'r') as f:
                    content = f.read()
                # Overwrite the bundled data.json (if possible)
                bundled_path = os.path.join(sys._MEIPASS, 'data.json')
                try:
                    with open(bundled_path, 'w') as f:
                        f.write(content)
                except Exception:
                    pass  # Ignore if not writable

        self.root = root
        self.editor_windows = {}  # Track open editor windows
        self.load_master_resume()
        # Use the window title from the first section if available
        if self.master_resume and self.master_resume[0].get("window_title"):
            self.root.title(self.master_resume[0]["window_title"])
        else:
            self.root.title("Resume Generator")

        self.set_dimensions()
        self.create_styles()
        # Variables for selections and file name
        self.section_vars = {}      # Main section checkboxes
        self.subsection_vars = {}   # Sub-options checkboxes
        self.selected_objective = tk.StringVar()
        self.output_file_name_var = tk.StringVar(value="Custom Resume")

        self.canvas = None  # Will be set in create_gui
        self.create_gui()
        self.setup_scrolling()

    def restrict_quotes(self, event):
        """Block typing of double quotes and backslashes."""
        if event.char in ['"', '\\']:
            return "break"

    def insert_literal_newline(self, event):
        """Instead of a newline, insert the literal string '\\n' and cancel the event."""
        event.widget.insert(tk.INSERT, "\\n")
        return "break"

    def restrict_to_digits(self, event):
        """Allow only digit characters (plus control keys) in certain entry fields."""
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Tab"):
            return
        if event.char and not event.char.isdigit():
            return "break"

    def open_ui_settings_editor(self):
        """Opens an editor window to update the UI settings and allow reordering of sections."""
        ui_window = tk.Toplevel(self.root)
        ui_window.title("Customize UI")
        ui_window.geometry("400x600")  # Increased height for the drag and drop list

        # --- Field: Main Window Title ---
        ttk.Label(ui_window, text="Main Window Title:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        title_entry = ttk.Entry(ui_window, width=30)
        title_entry.pack(anchor="w", padx=10)
        title_entry.insert(0, self.master_resume[0].get("window_title", "Master"))

        # --- Field: Main Window Font Size ---
        ttk.Label(ui_window, text="Main Window Font Size:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        font_entry = ttk.Entry(ui_window, width=30)
        font_entry.pack(anchor="w", padx=10)
        font_entry.insert(0, self.master_resume[0].get("main_window_font_size", "20"))
        font_entry.bind("<Key>", self.restrict_to_digits)

        # --- Field: Main Window Width ---
        ttk.Label(ui_window, text="Main Window Width:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        width_entry = ttk.Entry(ui_window, width=30)
        width_entry.pack(anchor="w", padx=10)
        width_entry.insert(0, self.master_resume[0].get("window_width", "1000"))
        width_entry.bind("<Key>", self.restrict_to_digits)

        # --- Field: Main Window Height ---
        ttk.Label(ui_window, text="Main Window Height:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        length_entry = ttk.Entry(ui_window, width=30)
        length_entry.pack(anchor="w", padx=10)
        length_entry.insert(0, self.master_resume[0].get("window_length", "500"))
        length_entry.bind("<Key>", self.restrict_to_digits)

        # --- New: Drag and Drop Listbox for Reordering Sections ---
        ttk.Label(ui_window, text="Reorder Sections (Drag and Drop):", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        drag_listbox = tk.Listbox(ui_window, width=50, height=10)
        drag_listbox.pack(padx=10, pady=5)

        # Populate the listbox with section titles from master_resume.
        for section in self.master_resume:
            drag_listbox.insert(tk.END, section.get("title", "No Title"))

        # Bind drag and drop events.
        drag_listbox.bind("<ButtonPress-1>", self.on_start_drag)
        drag_listbox.bind("<B1-Motion>", self.on_drag_motion)
        drag_listbox.bind("<ButtonRelease-1>", self.on_drop)

        # --- Save Button ---
        def save_ui_settings():
            title = title_entry.get().strip()
            font_size_str = font_entry.get().strip()
            width_str = width_entry.get().strip()
            length_str = length_entry.get().strip()

            try:
                font_size = int(font_size_str)
                width = int(width_str)
                length = int(length_str)
            except ValueError:
                messagebox.showerror("Error", "Font size, width, and height must be integers.")
                return

            # Validate requirements.
            if title == "" or width < 1000 or length < 300 or font_size < 8:
                msg = ("Please ensure that:\n"
                       "- The Title is not empty.\n"
                       "- The Main Window Font Size is at least 8.\n"
                       "- The Main Window Width is at least 1000.\n"
                       "- The Main Window Height is at least 300.\n\n"
                       "These requirements are intended to keep the UI readable and usable.")
                messagebox.showerror("Invalid UI Settings", msg)
                return

            # Update the settings in the master resume data (first element).
            self.master_resume[0]["window_title"] = title
            self.master_resume[0]["main_window_font_size"] = str(font_size)
            self.master_resume[0]["window_width"] = str(width)
            self.master_resume[0]["window_length"] = str(length)

            # Reorder the sections based on the new order in the drag_listbox.
            new_order = []
            listbox_items = drag_listbox.get(0, tk.END)
            for item in listbox_items:
                for section in self.master_resume:
                    if section.get("title") == item:
                        new_order.append(section)
                        break
            self.master_resume = new_order

            # Write updated JSON and refresh the main UI.
            self.write_master_resume()
            self.refresh_main_window()
            ui_window.destroy()

        ttk.Button(ui_window, text="Save", command=save_ui_settings, style="Custom.TButton").pack(pady=10)

    def on_start_drag(self, event):
        """Record the index where the drag starts."""
        widget = event.widget
        self._drag_start_index = widget.nearest(event.y)

    def on_drag_motion(self, event):
        """Swap items in the listbox as the user drags."""
        widget = event.widget
        new_index = widget.nearest(event.y)
        if new_index != self._drag_start_index:
            # Get the item, delete it, and insert it at the new index.
            item = widget.get(self._drag_start_index)
            widget.delete(self._drag_start_index)
            widget.insert(new_index, item)
            self._drag_start_index = new_index

    def on_drop(self, event):
        """Called when the drag is released. No additional action needed here."""
        pass
    
    def open_advanced_editor(self):
        """Prompt the user before opening the advanced JSON editor."""
        if messagebox.askyesno("Advanced Feature",
                               "This option is intended for advanced users only. Are you sure you want to open the advanced JSON editor?"):
            self.open_editor_window()

    def set_dimensions(self):
        try:
            width = int(self.master_resume[0]["window_width"])
            height = int(self.master_resume[0]["window_length"])
            self.root.geometry(f"{width}x{height}")
            self.wrap_length = max(0, width - 100)
        except Exception:
            self.root.geometry("600x700")
            self.wrap_length = 500

    def get_file_path(self, filename):
        """
        Returns the full path for the given filename.
        When running frozen, it first checks if the persistent file exists in the user's
        Documents/ResumeGeneratorApp folder. If it does, that path is returned.
        Otherwise, it falls back to the bundled version (if available) or the persistent path.
        In non-frozen mode, returns the local file path.
        """
        if getattr(sys, 'frozen', False):
            # Get persistent file path
            persistent_path = os.path.join(self.get_app_directory(), filename)
            if os.path.exists(persistent_path):
                return persistent_path
            else:
                # Fallback: use bundled file if available
                try:
                    bundled_path = os.path.join(sys._MEIPASS, filename)
                    if os.path.exists(bundled_path):
                        return bundled_path
                except AttributeError:
                    pass
                # If no persistent file exists yet, return the persistent path
                return persistent_path
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    def create_styles(self):
        main_font_size = self.get_main_font_size()
        main_font = f"Arial {main_font_size}"
        style = ttk.Style(self.root)
        style.configure("Custom.TCheckbutton", font=main_font)
        style.configure("Custom.TRadiobutton", font=main_font)
        style.configure("Custom.TLabel", font=main_font)
        style.configure("Custom.TButton", font=main_font)

    def get_main_font_size(self):
        try:
            return int(self.master_resume[0].get("main_window_font_size", 14))
        except Exception:
            return 14

    def load_master_resume(self):
        """
        Loads resume data.
        - When running frozen: first check for a persistent data.json in the user's Documents/ResumeGeneratorApp folder.
          If it exists, load it. If not, load default_data.json from the bundled environment.
        - When not frozen: first check for data.json in the local directory.
          If not found, load default_data.json from the same local directory.
        If neither file is found, initializes an empty resume.
        """
        file_path = None

        if getattr(sys, 'frozen', False):
            # Frozen mode: look for persistent file first
            persistent_file = os.path.join(self.get_app_directory(), 'data.json')
            if os.path.exists(persistent_file):
                file_path = persistent_file
            else:
                # Fall back to default_data.json from the bundled environment
                try:
                    bundled_default = os.path.join(sys._MEIPASS, 'default_data.json')
                    if os.path.exists(bundled_default):
                        file_path = bundled_default
                except Exception:
                    file_path = None
        else:
            # Non-frozen mode: look for data.json in the same directory as the script
            local_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
            if os.path.exists(local_data):
                file_path = local_data
            else:
                # Fall back to default_data.json in the same directory
                local_default = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_data.json')
                if os.path.exists(local_default):
                    file_path = local_default

        # Attempt to load the file if found; otherwise, initialize an empty resume.
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    self.master_resume = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load resume data: {e}")
                self.master_resume = []
        else:
            self.master_resume = []

    def update_editor_window_dimensions(self):
        try:
            width = int(self.master_resume[0]["editor_window_width"])
            height = int(self.master_resume[0]["editor_window_length"])
        except Exception:
            width, height = 600, 700
        try:
            text_size = int(self.master_resume[0].get("editor_text_size", 16))
        except Exception:
            text_size = 16
        for editor_window, data in list(self.editor_windows.items()):
            if editor_window.winfo_exists():
                editor_window.geometry(f"{width}x{height}")
                data["text_widget"].configure(font=("Courier", text_size))
            else:
                self.close_editor_window(editor_window)

    def open_directory(self, path):
        if not os.path.isdir(path):
            raise ValueError(f"The path '{path}' is not a valid directory.")
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":
                subprocess.run(["open", path], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", path], check=True)
            else:
                raise NotImplementedError(f"Opening directories is not supported on {system} OS.")
        except Exception as e:
            print(f"Error opening directory: {e}")

    def open_app_directory(self):
        self.open_directory(self.get_app_directory())

    def get_app_directory(self):
        """
        Returns the path to the persistent application folder in the user's Documents directory.
        If the folder does not exist, it is created.
        """
        documents_folder = os.path.expanduser("~/Documents")
        app_folder_name = "ResumeGeneratorApp"
        app_directory = os.path.join(documents_folder, app_folder_name)
        if not os.path.exists(app_directory):
            os.makedirs(app_directory)
        return app_directory

    def reset_to_default(self):
        confirm_reset = messagebox.askyesno(
            "Confirm Reset to Default",
            "This will reset the resume data to the default version, wiping all personal information.\n\n"
            "Make sure to backup your data if needed.\n\nProceed?"
        )
        if not confirm_reset:
            return
        try:
            with open(self.get_file_path("default_data.json"), "r") as f:
                default_content = f.read()
            with open(self.get_file_path("data.json"), "w") as f:
                f.write(default_content)
            if getattr(sys, 'frozen', False):
                with open(self.persistent_data_path, 'w') as f:
                    f.write(default_content)
            messagebox.showinfo("Success", "Resume data has been reset to default!")
            self.load_master_resume()
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    continue
                widget.destroy()
            self.create_gui()
        except Exception as e:
            messagebox.showerror("Error", f"Could not reset to default data: {e}")

    def open_information_window(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("Help")
        info_window.geometry("600x500")
        info_text = tk.Text(info_window, wrap="word", font=("Arial", 16), state="normal")
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(info_window, command=info_text.yview)
        scrollbar.pack(side="right", fill="y")
        info_text.configure(yscrollcommand=scrollbar.set)
        information_content = (
            "Welcome to the Resume Generator!\n\n"
            "This tool empowers you to quickly create a custom, professional resume tailored for each job application. "
            "Rather than relying on a generic template, you can choose exactly which sections, skills, and details to include so that your resume best fits the position you're applying for.\n\n"
            "Key Features:\n\n"
            "1. Customize UI\n"
            "   - Personalize the main window by changing its title, size, and font. Adjust these settings to match your preferences and ensure the app remains readable and user-friendly.\n\n"
            "2. Browse Files\n"
            "   - Quickly access the folder where your resume files and JSON data are stored. This makes it easy to manage, back up, or share your files.\n\n"
            "3. Reset Data\n"
            "   - Restore the default resume data with a single click. This is useful if you wish to start over or remove customizations (note: this will wipe all personalized information).\n\n"
            "4. Advanced JSON Editor\n"
            "   - (Advanced) Directly edit the underlying JSON data. This option is intended for power users. Please use it with caution, as incorrect modifications may lead to errors.\n\n"
            "Additional Functionalities:\n\n"
            " - Intuitive Editing & Reordering:\n"
            "   Each resume section has its own editor where you can add, edit, remove, and reorder items easily. For sections such as Education and Professional Experience, items are pre-selected by default to ensure all relevant information is included.\n\n"
            " - Selective Inclusion:\n"
            "   Use checkboxes and radio buttons to choose which sections and individual items appear on your resume. This helps you build a focused, concise document tailored to each job application.\n\n"
            " - Easy Saving & Refreshing:\n"
            "   Simply click 'Save' in any editor to update your resume data. The main window refreshes automatically, ensuring that your resume is always current.\n\n"
            "For any questions, feedback, or issues, please contact the developer."
        )
        info_text.insert("1.0", information_content)
        info_text.configure(state="disabled")

    def open_editor_window(self):
        """Opens the advanced JSON editor (raw data editor)."""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Advanced JSON Editor")
        try:
            width = int(self.master_resume[0]["editor_window_width"])
            height = int(self.master_resume[0]["editor_window_length"])
            editor_window.geometry(f"{width}x{height}")
        except Exception:
            editor_window.geometry("600x700")
        try:
            text_size = int(self.master_resume[0].get("editor_text_size", 16))
        except Exception:
            text_size = 16
        editor_window.protocol("WM_DELETE_WINDOW", lambda: self.close_editor_window(editor_window))
        data_text = tk.Text(editor_window, wrap="word", font=("Courier", text_size))
        data_text.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            with open(self.get_file_path("data.json"), "r") as f:
                content = f.read()
                data_text.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data.json: {e}")
            editor_window.destroy()
            return
        self.editor_windows[editor_window] = {"text_widget": data_text}
        save_button = ttk.Button(
            editor_window,
            text="Save",
            command=lambda: self.save_changes(editor_window),
            style="Custom.TButton"
        )
        save_button.pack(anchor="center", pady=10)

    def close_editor_window(self, editor_window):
        if editor_window in self.editor_windows:
            del self.editor_windows[editor_window]
        editor_window.destroy()

    def write_master_resume(self):
        """
        Writes the current master resume data to data.json.
        When running as frozen, this writes to the persistent folder.
        """
        try:
            # In frozen mode, always write to the persistent folder.
            if getattr(sys, 'frozen', False):
                file_path = os.path.join(self.get_app_directory(), 'data.json')
            else:
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
            
            # Ensure the directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, "w") as f:
                json.dump(self.master_resume, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not write data.json: {e}")

    def refresh_main_window(self):
        """Reload data.json and completely redraw the main window (except Toplevel windows)."""
        self.load_master_resume()
        self.create_styles()
        self.set_dimensions()
        # Update the main window title if defined
        if self.master_resume and self.master_resume[0].get("window_title"):
            self.root.title(self.master_resume[0]["window_title"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                continue
            widget.destroy()
        self.create_gui()

    def edit_section_content(self, section):
        """
        Opens an editor for a given section.
        For Professional Experience and Education, a structured editor is used.
        For all other sections, a simple editor (with single-line input) is used.
        """
        if section["title"] == "Personal Information":
            self.edit_personal_info_section(section)
        elif section["title"] in ["Professional Experience", "Education"]:
            self.edit_structured_section_content(section)
        else:
            self.edit_simple_section_content(section)

    def edit_personal_info_section(self, section):
        # Create a new Toplevel window with a wider geometry.
        win = tk.Toplevel(self.root)
        win.title("Edit Personal Information")
        win.geometry("900x500")  # Wider window for ample space

        # --- Name Field ---
        ttk.Label(win, text="Name:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        name_entry = ttk.Entry(win, width=50)
        name_entry.pack(anchor="w", padx=10)
        if section["content"]:
            name_entry.insert(0, section["content"][0])

        # --- Details Listbox with Drag-and-Drop ---
        ttk.Label(win, text="Details:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        
        details_frame = ttk.Frame(win)
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        listbox = tk.Listbox(details_frame, width=80)
        listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate listbox with details from section (skipping the first item which is the name)
        for detail in section["content"][1:]:
            listbox.insert(tk.END, detail)
        
        # --- Drag and Drop Functions ---
        def on_start_drag(event):
            widget = event.widget
            widget._drag_start_index = widget.nearest(event.y)
        
        def on_drag_motion(event):
            widget = event.widget
            new_index = widget.nearest(event.y)
            if new_index != widget._drag_start_index:
                # Get all items, reorder in the list, then update the Listbox.
                items = list(widget.get(0, tk.END))
                item = items.pop(widget._drag_start_index)
                items.insert(new_index, item)
                widget.delete(0, tk.END)
                for i in items:
                    widget.insert(tk.END, i)
                widget._drag_start_index = new_index
        
        def on_drop(event):
            # No extra action is needed on drop.
            pass

        listbox.bind("<ButtonPress-1>", on_start_drag)
        listbox.bind("<B1-Motion>", on_drag_motion)
        listbox.bind("<ButtonRelease-1>", on_drop)
        
        # --- Combined Button Frame for Managing Details and Save/Cancel ---
        combined_frame = ttk.Frame(win)
        combined_frame.pack(fill="x", padx=10, pady=10)
        
        def add_detail():
            detail_win = tk.Toplevel(win)
            detail_win.title("Add Detail")
            detail_win.geometry("400x150")
            ttk.Label(detail_win, text="New Detail:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            detail_entry = ttk.Entry(detail_win, width=50)
            detail_entry.pack(anchor="w", padx=10, pady=5)
            def save_new_detail():
                text = detail_entry.get().strip()
                if text:
                    listbox.insert(tk.END, text)
                    detail_win.destroy()
                else:
                    messagebox.showerror("Error", "Detail cannot be empty.")
            ttk.Button(detail_win, text="Save", command=save_new_detail, style="Custom.TButton").pack(pady=10)
        
        def edit_detail():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "No detail selected.")
                return
            index = selection[0]
            current_text = listbox.get(index)
            detail_win = tk.Toplevel(win)
            detail_win.title("Edit Detail")
            detail_win.geometry("400x150")
            ttk.Label(detail_win, text="Edit Detail:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            detail_entry = ttk.Entry(detail_win, width=50)
            detail_entry.pack(anchor="w", padx=10, pady=5)
            detail_entry.insert(0, current_text)
            def save_edited_detail():
                new_text = detail_entry.get().strip()
                if new_text:
                    listbox.delete(index)
                    listbox.insert(index, new_text)
                    detail_win.destroy()
                else:
                    messagebox.showerror("Error", "Detail cannot be empty.")
            ttk.Button(detail_win, text="Save", command=save_edited_detail, style="Custom.TButton").pack(pady=10)
        
        def remove_detail():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "No detail selected.")
                return
            index = selection[0]
            if messagebox.askyesno("Confirm", "Remove selected detail?"):
                listbox.delete(index)
        
        def save_changes():
            # Update section["content"]: first item is name, rest are details from the listbox.
            new_content = [name_entry.get().strip()]
            for i in range(listbox.size()):
                new_content.append(listbox.get(i))
            section["content"] = new_content
            self.write_master_resume()  # Save to JSON
            self.refresh_main_window()  # Refresh the GUI
            win.destroy()
        
        def cancel_changes():
            if messagebox.askyesno("Cancel", "Discard changes?"):
                win.destroy()
        
        ttk.Button(combined_frame, text="Add", command=add_detail, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Edit", command=edit_detail, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Remove", command=remove_detail, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Save", command=save_changes, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Cancel", command=cancel_changes, style="Custom.TButton").pack(side="left", padx=5)

    def edit_simple_section_content(self, section):
        """
        Editor for sections whose content is a list of strings (e.g., Objective, Certifications, etc.).
        Features:
        - Drag and drop reordering
        - Duplicate entry prevention
        - Selection state preservation
        - Improved error handling
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("900x500")
        win.transient(self.root)  # Make it modal
        
        # Backup original content and current selection
        original_content = copy.deepcopy(section["content"])
        current_selection = None

        # NOTE: Inform users they can drag and drop to reorder items.
        ttk.Label(win, text="Drag and drop items to reorder them.", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)

        # Create Listbox for items.
        listbox = tk.Listbox(win, width=80)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def refresh_listbox():
            try:
                # Store current selection
                selection = listbox.curselection()
                selected_index = selection[0] if selection else None
                
                # For Core Competencies, sort alphabetically
                if section["title"] == "Core Competencies":
                    section["content"] = sorted(section["content"], key=lambda s: s.lower())
                
                listbox.delete(0, tk.END)
                for item in section["content"]:
                    listbox.insert(tk.END, item)
                
                # Restore selection if possible
                if selected_index is not None and selected_index < listbox.size():
                    listbox.selection_set(selected_index)
                    listbox.see(selected_index)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh list: {str(e)}")
        refresh_listbox()
        current_index = [None]

        def on_listbox_select(event):
            selection = listbox.curselection()
            current_index[0] = selection[0] if selection else None
        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        # Child popup for adding/editing an item.
        def open_edit_window(is_new=False):
            selected_index = current_index[0]
            if not is_new and selected_index is None:
                messagebox.showerror("Error", "No item selected for editing.")
                return
            child_win = tk.Toplevel(win)
            child_win.title(f"{'Add' if is_new else 'Edit'} Item for {section['title']}")
            child_win.geometry("400x150")

            ttk.Label(child_win, text="Item Content:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            entry_widget = ttk.Entry(child_win, width=50)
            entry_widget.pack(fill="x", padx=10, pady=5)
            entry_widget.bind("<Key>", self.restrict_quotes)
            entry_widget.bind("<Return>", lambda e: "break")
            if not is_new:
                entry_widget.insert(0, section["content"][selected_index].replace("\\n", " "))

            def done_child():
                try:
                    new_text = entry_widget.get().strip()
                    if not new_text:
                        messagebox.showerror("Error", "Item content cannot be empty.")
                        return
                    
                    # Check for duplicates
                    if new_text in section["content"] and (is_new or new_text != section["content"][selected_index]):
                        messagebox.showerror("Error", "This item already exists in the list.")
                        return
                    
                    if is_new:
                        section["content"].append(new_text)
                    else:
                        section["content"][selected_index] = new_text
                    
                    refresh_listbox()
                    child_win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save item: {str(e)}")
            ttk.Button(child_win, text="Done", command=done_child, style="Custom.TButton").pack(pady=10)

        ttk.Button(win, text="Add", command=lambda: open_edit_window(is_new=True), style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(win, text="Edit", command=lambda: open_edit_window(is_new=False), style="Custom.TButton").pack(side="left", padx=5)
        
        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    refresh_listbox()
            else:
                messagebox.showerror("Error", "No item selected to remove.")
        ttk.Button(win, text="Remove", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)

        # --- DRAG AND DROP EVENT HANDLERS ---
        def on_start_drag(event):
            widget = event.widget
            widget._drag_start_index = widget.nearest(event.y)

        def on_drag_motion(event):
            try:
                widget = event.widget
                new_index = widget.nearest(event.y)
                if new_index != widget._drag_start_index:
                    # Update the underlying list: move the item
                    section["content"].insert(new_index, section["content"].pop(widget._drag_start_index))
                    # Refresh the Listbox
                    widget.delete(0, tk.END)
                    for i in section["content"]:
                        widget.insert(tk.END, i)
                    widget._drag_start_index = new_index
                    widget.selection_clear(0, tk.END)
                    widget.selection_set(new_index)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reorder items: {str(e)}")

        def on_drop(event):
            # No extra processing required on drop.
            pass

        listbox.bind("<ButtonPress-1>", on_start_drag)
        listbox.bind("<B1-Motion>", on_drag_motion)
        listbox.bind("<ButtonRelease-1>", on_drop)
        # --- END DRAG AND DROP ---

        # Save and Cancel buttons.
        bottom_frame = ttk.Frame(win)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        def save_content_editor():
            self.write_master_resume()
            messagebox.showinfo("Saved", "Changes saved successfully.")
            self.refresh_main_window()
            win.destroy()

        def cancel_content_editor():
            if messagebox.askyesno("Cancel", "Are you sure you want to cancel? All unsaved changes will be discarded."):
                section["content"] = original_content
                messagebox.showinfo("Canceled", "Changes discarded.")
                win.destroy()

        ttk.Button(bottom_frame, text="Save", command=save_content_editor, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Cancel", command=cancel_content_editor, style="Custom.TButton").pack(side="left", padx=10)

    # ---------------------------
    # NEW STRUCTURED SECTION EDITOR
    # ---------------------------
    def edit_structured_section_content(self, section):
        """
        Implementation for structured sections (Professional Experience and Education).
        Displays the section items in a single Listbox with drag-and-drop support.
        When adding or editing an item, a popup is opened with fields:
          - For Professional Experience: "Title", "Dates", and "Details" (edited as a list)
          - For Education: "Title" and "Details" (edited as a list)
        Includes validation for required fields and proper error handling.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("900x500")
        
        # Backup original content
        original_content = copy.deepcopy(section["content"])
        original_content = copy.deepcopy(section["content"])

        # NOTE: Inform users they can drag and drop to reorder items.
        ttk.Label(win, text="Drag and drop items to reorder them.", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)

        # Listbox for structured items
        listbox = tk.Listbox(win, width=80)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def refresh_listbox():
            try:
                # Store current selection
                current_selection = listbox.curselection()
                selected_index = current_selection[0] if current_selection else None

                listbox.delete(0, tk.END)
                for item in section["content"]:
                    if isinstance(item, list):  # Education
                        listbox.insert(tk.END, item[0])
                    else:  # Professional Experience
                        listbox.insert(tk.END, f"{item['subtitle']} ({item['date']})")

                # Restore selection if possible
                if selected_index is not None and selected_index < listbox.size():
                    listbox.selection_set(selected_index)
                    listbox.see(selected_index)  # Ensure the selected item is visible
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh list: {str(e)}")
                return

        refresh_listbox()

        current_index = [None]

        def on_start_drag(event):
            widget = event.widget
            widget._drag_start_index = widget.nearest(event.y)

        def on_drag_motion(event):
            widget = event.widget
            new_index = widget.nearest(event.y)
            if new_index != widget._drag_start_index:
                # Move the item in the underlying JSON data.
                section["content"].insert(new_index, section["content"].pop(widget._drag_start_index))
                # Refresh the listbox display.
                refresh_listbox()
                widget._drag_start_index = new_index

        def on_drop(event):
            # No additional processing required on drop.
            pass

        listbox.bind("<ButtonPress-1>", on_start_drag)
        listbox.bind("<B1-Motion>", on_drag_motion)
        listbox.bind("<ButtonRelease-1>", on_drop)

        def on_listbox_select(event):
            selection = listbox.curselection()
            current_index[0] = selection[0] if selection else None
        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        def open_structured_item_editor(selected_index, is_new=False):
            item_editor = tk.Toplevel(win)
            item_editor.transient(win)  # Make it modal
            if is_new:
                item_editor.title(f"Add Item for {section['title']}")
            else:
                item_editor.title(f"Edit Item for {section['title']}")
            item_editor.geometry("500x500")

            # Field: Title
            ttk.Label(item_editor, text="Title:*", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            title_entry = ttk.Entry(item_editor, width=50)
            title_entry.pack(anchor="w", padx=10)
            title_entry.bind("<Key>", self.restrict_quotes)

            # Field: Dates (only for Professional Experience)
            if section["title"] == "Professional Experience":
                ttk.Label(item_editor, text="Dates:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
                dates_entry = ttk.Entry(item_editor, width=50)
                dates_entry.pack(anchor="w", padx=10)
                dates_entry.bind("<Key>", self.restrict_quotes)
            else:
                dates_entry = None

            # Details sublist editor
            ttk.Label(item_editor, text="Details:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            details_listbox = tk.Listbox(item_editor, width=50, height=8)
            details_listbox.pack(anchor="w", padx=10, pady=5)
            details_scrollbar = ttk.Scrollbar(item_editor, orient="vertical", command=details_listbox.yview)
            details_scrollbar.pack(side="right", fill="y")
            details_listbox.config(yscrollcommand=details_scrollbar.set)
            details = []  # Local list for details

            def on_start_drag_detail(event):
                details_listbox._drag_start_index = details_listbox.nearest(event.y)

            def on_drag_motion_detail(event):
                new_index = details_listbox.nearest(event.y)
                if new_index != details_listbox._drag_start_index:
                    # Reorder the underlying details list.
                    details.insert(new_index, details.pop(details_listbox._drag_start_index))
                    refresh_details_listbox()
                    details_listbox._drag_start_index = new_index

            def on_drop_detail(event):
                try:
                    # Get the current index where the mouse was released
                    index = details_listbox.nearest(event.y)
                    refresh_details_listbox()
                    # Restore selection after refresh
                    details_listbox.selection_set(index)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update after drag: {str(e)}")
                return

            # Bind the drag-and-drop events to the details_listbox.
            details_listbox.bind("<ButtonPress-1>", on_start_drag_detail)
            details_listbox.bind("<B1-Motion>", on_drag_motion_detail)
            details_listbox.bind("<ButtonRelease-1>", on_drop_detail)

            def refresh_details_listbox():
                # Save current selection if any
                selected_indices = details_listbox.curselection()
                selected_index = selected_indices[0] if selected_indices else None
                
                details_listbox.delete(0, tk.END)
                for d in details:
                    details_listbox.insert(tk.END, d)
                    
                # Restore selection if there was one
                if selected_index is not None and selected_index < len(details):
                    details_listbox.selection_set(selected_index)

            # Sub-functions for managing details
            def add_detail():
                detail_win = tk.Toplevel(item_editor)
                detail_win.title("Add Detail")
                detail_win.geometry("400x150")
                ttk.Label(detail_win, text="Detail:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
                detail_entry = ttk.Entry(detail_win, width=50)
                detail_entry.pack(anchor="w", padx=10, pady=5)
                detail_entry.bind("<Key>", self.restrict_quotes)
                def done_detail():
                    text = detail_entry.get().strip()
                    if not text:
                        messagebox.showerror("Error", "Detail cannot be empty.")
                        return
                    details.append(text)
                    refresh_details_listbox()
                    detail_win.destroy()
                ttk.Button(detail_win, text="Done", command=done_detail, style="Custom.TButton").pack(pady=10)

            def edit_detail():
                selection = details_listbox.curselection()
                if not selection:
                    messagebox.showerror("Error", "No detail selected.")
                    return
                index = selection[0]
                detail_win = tk.Toplevel(item_editor)
                detail_win.title("Edit Detail")
                detail_win.geometry("400x150")
                ttk.Label(detail_win, text="Detail:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
                detail_entry = ttk.Entry(detail_win, width=50)
                detail_entry.pack(anchor="w", padx=10, pady=5)
                detail_entry.bind("<Key>", self.restrict_quotes)
                detail_entry.insert(0, details[index])
                def done_detail():
                    text = detail_entry.get().strip()
                    if not text:
                        messagebox.showerror("Error", "Detail cannot be empty.")
                        return
                    details[index] = text
                    refresh_details_listbox()
                    detail_win.destroy()
                ttk.Button(detail_win, text="Done", command=done_detail, style="Custom.TButton").pack(pady=10)

            def remove_detail():
                selection = details_listbox.curselection()
                if not selection:
                    messagebox.showerror("Error", "No detail selected.")
                    return
                index = selection[0]
                if messagebox.askyesno("Confirm", "Remove selected detail?"):
                    del details[index]
                    refresh_details_listbox()

            detail_btn_frame = ttk.Frame(item_editor)
            detail_btn_frame.pack(anchor="w", padx=10, pady=5)
            ttk.Button(detail_btn_frame, text="Add Detail", command=add_detail, style="Custom.TButton").pack(side="left", padx=5)
            ttk.Button(detail_btn_frame, text="Edit Detail", command=edit_detail, style="Custom.TButton").pack(side="left", padx=5)
            ttk.Button(detail_btn_frame, text="Remove Detail", command=remove_detail, style="Custom.TButton").pack(side="left", padx=5)

            # Prepopulate fields if editing an existing item.
            if not is_new and selected_index is not None:
                item = section["content"][selected_index]
                if section["title"] == "Professional Experience":
                    title_entry.insert(0, item.get("subtitle", ""))
                    dates_entry.insert(0, item.get("date", ""))
                    details.extend(item.get("details", []))
                elif section["title"] == "Education":
                    if isinstance(item, list) and item:
                        title_entry.insert(0, item[0])
                        details.extend(item[1:])
                refresh_details_listbox()

            def validate_dates(date_str):
                """Basic date format validation"""
                if not date_str.strip():
                    return False
                # Could add more specific validation here if needed
                return True

            def done_item():
                try:
                    new_title = title_entry.get().strip()
                    if not new_title:
                        messagebox.showerror("Error", "Title cannot be empty.")
                        return

                    if section["title"] == "Professional Experience":
                        new_dates = dates_entry.get().strip()
                        if not validate_dates(new_dates):
                            messagebox.showerror("Error", "Please enter a valid date.")
                            return
                        new_item = {"subtitle": new_title, "date": new_dates, "details": details.copy()}
                    elif section["title"] == "Education":
                        new_item = [new_title] + details.copy()

                    if not details:  # Ensure there's at least one detail
                        messagebox.showerror("Error", "Please add at least one detail.")
                        return

                    if is_new or selected_index is None:
                        section["content"].append(new_item)
                    else:
                        section["content"][selected_index] = new_item

                    refresh_listbox()
                    item_editor.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save item: {str(e)}")

            ttk.Button(item_editor, text="Done", command=done_item, style="Custom.TButton").pack(pady=10)

        def add_item():
            current_index[0] = None
            open_structured_item_editor(is_new=True)

        def edit_item():
            selection = listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "No item selected for editing.")
                return
            # Capture the selected index immediately.
            selected_index = selection[0]
            # Open the structured item editor with the captured index.
            open_structured_item_editor(selected_index=selected_index, is_new=False)

        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    refresh_listbox()
            else:
                messagebox.showerror("Error", "No item selected to remove.")

        # Combined button frame for item management and saving/canceling changes.
        combined_frame = ttk.Frame(win)
        combined_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(combined_frame, text="Add", command=add_item, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Edit", command=edit_item, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Remove", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Save", command=lambda: (self.write_master_resume(), messagebox.showinfo("Saved", "Changes saved successfully."), self.refresh_main_window(), win.destroy()), style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(combined_frame, text="Cancel", command=lambda: (section.update({"content": original_content}), messagebox.showinfo("Canceled", "Changes discarded."), win.destroy()) if messagebox.askyesno("Cancel", "Are you sure you want to cancel? All unsaved changes will be discarded.") else None, style="Custom.TButton").pack(side="left", padx=5)

    def create_gui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)
        # New order and renamed buttons:
        ttk.Button(top_frame, text="Customize UI", command=self.open_ui_settings_editor, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Browse Files", command=self.open_app_directory, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Help", command=self.open_information_window, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Reset Data", command=self.reset_to_default, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Advanced JSON Editor", command=self.open_advanced_editor, style="Custom.TButton").pack(side="left", padx=10)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(main_frame)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel events
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)
        
        # Add sections
        for section in self.master_resume:
            self.add_section_widgets(self.scrollable_frame, section)
            
        # Bottom frame
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", pady=10)
        ttk.Label(bottom_frame, text="Output File Name:", style="Custom.TLabel").pack(side="left", padx=5)
        entry = ttk.Entry(bottom_frame, textvariable=self.output_file_name_var, width=30)
        entry.pack(side="left", padx=5)
        entry.configure(font=("Arial", self.get_main_font_size()))
        ttk.Button(bottom_frame, text="Generate Resume", command=self.generate_resume, style="Custom.TButton").pack(side="left", padx=10)

    def _on_mousewheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def _on_mousewheel_mac(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
            
    def _on_enter(self, event):
        if platform.system() == 'Darwin':  # macOS
            self.canvas.bind_all('<Button-4>', self._on_mousewheel_mac)
            self.canvas.bind_all('<Button-5>', self._on_mousewheel_mac)
        else:  # Windows
            self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
            
    def _on_leave(self, event):
        if platform.system() == 'Darwin':  # macOS
            self.canvas.unbind_all('<Button-4>')
            self.canvas.unbind_all('<Button-5>')
        else:  # Windows
            self.canvas.unbind_all('<MouseWheel>')

    def add_section_widgets(self, parent, section):
        if section["title"] == "Personal Information":
            section_var = tk.BooleanVar(value=True)
        else:
            # Check if the section has any subsections.
            section_var = tk.BooleanVar(value=bool(section.get("content")))
        # section_var = tk.BooleanVar(value=True) Old lazy version checks all sections (even empty ones)
        self.section_vars[section["title"]] = section_var
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill="x", pady=5)
        # Checkbox at the top
        section_checkbox = ttk.Checkbutton(
            section_frame,
            text=section["title"],
            variable=section_var,
            command=lambda: self.toggle_suboptions(section["title"], section_var.get()),
            style="Custom.TCheckbutton"
        )
        section_checkbox.pack(anchor="w")
        # Edit Section button positioned below the checkbox
        ttk.Button(
            section_frame,
            text="Edit Section",
            command=lambda: self.edit_section_content(section),
            style="Custom.TButton"
        ).pack(anchor="w", padx=20, pady=2)
        if "content" in section and isinstance(section["content"], list):
            if section["title"] == "Personal Information":
                return
            subsection_frame = ttk.Frame(section_frame)
            subsection_frame.pack(fill="x", padx=20)
            if section["title"] == "Objective":
                self.add_objective_options(subsection_frame, section["content"])
            elif section["title"] == "Education":
                self.add_education_options(subsection_frame, section["content"], section["title"])
            else:
                self.add_suboptions(subsection_frame, section["content"], section["title"])

    def on_label_click_radio(self, event):
        widget = event.widget
        if hasattr(widget, "custom_value"):
            self.selected_objective.set(widget.custom_value)

    def add_education_options(self, parent, education_content, section_title):
        for entry in education_content:
            if isinstance(entry, list) and entry:  # Check if entry is a non-empty list
                main_entry = entry[0]  # Get the title (first element)
                var = tk.BooleanVar(value=True)
                # Use the title string as the key
                self.subsection_vars[(section_title, str(main_entry))] = var
                ttk.Checkbutton(parent, text=main_entry, variable=var, style="Custom.TCheckbutton").pack(anchor="w")

    def on_label_click_toggle(self, event):
        widget = event.widget
        if hasattr(widget, "custom_var"):
            current = widget.custom_var.get()
            widget.custom_var.set(not current)

    def add_objective_options(self, parent, options):
        # Create a radio button + label for each objective option.
        for option in options:
            label_frame = ttk.Frame(parent)
            label_frame.pack(anchor="w", pady=2)

            rb = ttk.Radiobutton(
                label_frame,
                variable=self.selected_objective,
                value=option,
                style="Custom.TRadiobutton"
            )
            rb.pack(side="left")

            label = ttk.Label(
                label_frame,
                text=option,
                wraplength=self.wrap_length,
                style="Custom.TLabel"
            )
            # Attach the option value to the label so the click can set it.
            label.custom_value = option
            label.pack(side="left")
            label.bind("<Button-1>", lambda e, val=option: self.selected_objective.set(val))

        # Add the custom objective field.
        custom_frame = ttk.Frame(parent)
        custom_frame.pack(anchor="w", pady=5)
        ttk.Radiobutton(
            custom_frame,
            variable=self.selected_objective,
            value="Custom",
            style="Custom.TRadiobutton"
        ).pack(side="left")
        ttk.Label(custom_frame, text="Custom Objective:", style="Custom.TLabel").pack(side="left")
        self.custom_objective_text = ttk.Entry(custom_frame, width=50)
        self.custom_objective_text.pack(side="left", padx=5)
        self.custom_objective_text.bind("<Key>", self.restrict_quotes)

        if options:
            self.selected_objective.set(options[0])

    def add_suboptions(self, parent, options, section_title):
        if section_title == "Technical Projects":
            for option in options:
                var = tk.BooleanVar(value=False)
                self.subsection_vars[(section_title, option)] = var
                frame = ttk.Frame(parent)
                frame.pack(fill="x", pady=2)
                cb = ttk.Checkbutton(frame, text="", variable=var, style="Custom.TCheckbutton")
                cb.pack(side="left", padx=5)
                label = ttk.Label(frame, text=option, wraplength=self.wrap_length, style="Custom.TLabel", justify="left")
                label.custom_var = var
                label.pack(side="left")
                label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
        elif section_title == "Core Competencies":
            sorted_options = sorted(options, key=lambda s: s.lower())
            for option in sorted_options:
                var = tk.BooleanVar(value=False)
                self.subsection_vars[(section_title, option)] = var
                frame = ttk.Frame(parent)
                frame.pack(fill="x", pady=2)
                cb = ttk.Checkbutton(frame, text="", variable=var, style="Custom.TCheckbutton")
                cb.pack(side="left", padx=5)
                label = ttk.Label(frame, text=option, wraplength=self.wrap_length, style="Custom.TLabel", justify="left")
                label.custom_var = var
                label.pack(side="left")
                label.bind("<Button-1>", lambda e, v=var: v.set(not v.get()))
        elif section_title == "Professional Experience":
            # Options are expected to be dictionaries.
            for option in options:
                key = option.get("subtitle", "No Title")
                var = tk.BooleanVar(value=True)
                self.subsection_vars[(section_title, key)] = var
                ttk.Checkbutton(parent, text=key, variable=var, style="Custom.TCheckbutton").pack(anchor="w")
        else:
            # For any other section, check if the option is a dict.
            for option in options:
                if isinstance(option, dict):
                    key = option.get("subtitle", "No Title")
                    var = tk.BooleanVar(value=True)
                    self.subsection_vars[(section_title, key)] = var
                    ttk.Checkbutton(parent, text=key, variable=var, style="Custom.TCheckbutton").pack(anchor="w")
                else:
                    var = tk.BooleanVar(value=True)
                    self.subsection_vars[(section_title, option)] = var
                    ttk.Checkbutton(parent, text=option, variable=var, style="Custom.TCheckbutton").pack(anchor="w")

    def toggle_suboptions(self, section_title, enabled):
        for key, var in self.subsection_vars.items():
            if isinstance(key, tuple) and key[0] == section_title:
                if not enabled:
                    var.set(False)
                elif section_title not in ["Core Competencies", "Technical Projects"]:
                    var.set(True)

    def generate_resume(self):
        """
        Generate the resume document and save it to the user's Documents folder.
        For macOS, saves to ~/Documents/ResumeGeneratorApp/
        For Windows, saves to Documents\ResumeGeneratorApp\
        """
        try:
            # Ensure output directory exists
            output_dir = self.get_app_directory()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Collect selected sections
            selected_sections = []
            for section in self.master_resume:
                if self.section_vars[section["title"]].get():
                    if section["title"] == "Personal Information":
                        selected_sections.append({"title": section["title"], "content": section["content"]})
                    elif section["title"] == "Objective":
                        if self.selected_objective.get() == "Custom":
                            custom_text = self.custom_objective_text.get().strip()
                            if custom_text:
                                selected_sections.append({
                                    "title": section["title"],
                                    "content": [custom_text]
                                })
                        else:
                            selected_objective = self.selected_objective.get()
                            if selected_objective in section["content"]:
                                selected_sections.append({
                                    "title": section["title"],
                                    "content": [selected_objective]
                                })
                    else:
                        # For other sections, filter by selected subsections
                        selected_content = []
                        for item in section["content"]:
                            # Special handling for Education section
                            if section["title"] == "Education" and isinstance(item, list) and item:
                                key = str(item[0])  # Convert title to string for dictionary key
                            elif isinstance(item, dict):
                                key = item.get("subtitle", "No Title")
                            else:
                                key = str(item)
                            if (section["title"], key) in self.subsection_vars:
                                if self.subsection_vars[(section["title"], key)].get():
                                    selected_content.append(item)
                        if selected_content:
                            selected_sections.append({
                                "title": section["title"],
                                "content": selected_content
                            })

            if not selected_sections:
                messagebox.showerror("Error", "No sections selected. Please select at least one section.")
                return

            # Generate output filename with timestamp to avoid overwrites
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_path = os.path.abspath(os.path.join(output_dir, f"resume_{timestamp}.docx"))

            try:
                # Generate the resume with absolute path
                generator = Generator(selected_sections)
                generator.generate(output_file_path)

                # Open the generated file
                try:
                    if os.name == 'posix':  # macOS
                        subprocess.run(['open', output_file_path], check=True)
                    else:  # Windows
                        os.startfile(output_file_path)
                except Exception as e:
                    messagebox.showwarning("Warning", 
                        f"Resume was generated but could not be opened automatically.\n" 
                        f"File is saved at: {output_file_path}\n\n"
                        f"Error: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate resume: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare resume data: {str(e)}")

    def save_changes(self, editor_window):
        if editor_window not in self.editor_windows:
            messagebox.showerror("Error", "Editor window not found.")
            return
        data_text = self.editor_windows[editor_window]["text_widget"]
        updated_content = data_text.get("1.0", tk.END).strip()
        try:
            parsed = json.loads(updated_content)
            with open(self.get_file_path("data.json"), "w") as f:
                json.dump(parsed, f, indent=4)
            if getattr(sys, 'frozen', False):
                with open(self.persistent_data_path, 'w') as f:
                    json.dump(parsed, f, indent=4)
            # Use full refresh to update main window title, geometry, and all elements
            self.refresh_main_window()
            for editor_win, data in self.editor_windows.items():
                text_widget = data["text_widget"]
                if editor_win.winfo_exists():
                    try:
                        with open(self.get_file_path("data.json"), "r") as f:
                            new_content = f.read()
                        text_widget.delete("1.0", tk.END)
                        text_widget.insert("1.0", new_content)
                    except Exception as e:
                        print(f"Failed to update editor window: {e}")
        except json.JSONDecodeError as je:
            messagebox.showerror("JSON Error", f"Invalid JSON format:\n{je}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save changes: {e}")

    def setup_scrolling(self):
        """Set up scrolling for the main canvas and its children"""
        if not self.canvas:
            return
            
        def _on_mousewheel(event):
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")

        def _on_mousewheel_mac(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

        def _on_enter(event):
            # Bind scrolling when mouse enters any widget in the canvas
            widget = event.widget
            while widget and widget != self.root:
                if widget == self.canvas:
                    self.root.bind_all("<MouseWheel>", _on_mousewheel)
                    self.root.bind_all("<Button-4>", _on_mousewheel_mac)
                    self.root.bind_all("<Button-5>", _on_mousewheel_mac)
                    break
                widget = widget.master

        def _on_leave(event):
            # Unbind scrolling when mouse leaves the canvas area
            widget = event.widget
            while widget and widget != self.root:
                if widget == self.canvas:
                    self.root.unbind_all("<MouseWheel>")
                    self.root.unbind_all("<Button-4>")
                    self.root.unbind_all("<Button-5>")
                    break
                widget = widget.master

        # Bind enter/leave events to the canvas and all its children
        self.canvas.bind("<Enter>", _on_enter)
        self.canvas.bind("<Leave>", _on_leave)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()
