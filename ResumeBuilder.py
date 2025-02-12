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
from generator import generate_resume  # Uses python-docx to create the resume document

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
        self.output_file_name_var = tk.StringVar(value="Custom_Resume")

        self.create_gui()

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
        """Opens an editor window to update the main window title, font size, width, and height."""
        ui_window = tk.Toplevel(self.root)
        ui_window.title("Edit UI Settings")
        ui_window.geometry("400x350")  # Set geometry to 400x350

        # --- Field: Main Window Title ---
        ttk.Label(ui_window, text="Main Window Title:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
        title_entry = ttk.Entry(ui_window, width=30)
        title_entry.pack(anchor="w", padx=10)
        # Prepopulate with current title (from the master resume’s first element)
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

            # Validate requirements
            if title == "" or width < 1000 or length < 300 or font_size < 8:
                msg = ("Please ensure that:\n"
                       "- The Title is not empty.\n"
                       "- The Main Window Width is at least 1000.\n"
                       "- The Main Window Height is at least 300.\n"
                       "- The Main Window Font Size is at least 8.\n\n"
                       "These requirements are intended to keep the UI readable and usable.")
                messagebox.showerror("Invalid UI Settings", msg)
                return

            # Update the settings in the master resume data (assumed to be in the first element)
            self.master_resume[0]["window_title"] = title
            self.master_resume[0]["main_window_font_size"] = str(font_size)
            self.master_resume[0]["window_width"] = str(width)
            self.master_resume[0]["window_length"] = str(length)

            # Write data and perform a full refresh (including updating the title and geometry)
            self.write_master_resume()
            self.refresh_main_window()
            ui_window.destroy()

        ttk.Button(ui_window, text="Save", command=save_ui_settings, style="Custom.TButton").pack(pady=10)

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
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)

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
        try:
            with open(self.get_file_path('data.json'), "r") as f:
                self.master_resume = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data.json: {e}")
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
        info_window.title("Information")
        info_window.geometry("600x500")
        info_text = tk.Text(info_window, wrap="word", font=("Arial", 16), state="normal")
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(info_window, command=info_text.yview)
        scrollbar.pack(side="right", fill="y")
        info_text.configure(yscrollcommand=scrollbar.set)
        information_content = (
            "Welcome to the Resume Generator!\n\n"
            "This tool enables you to quickly create a custom, professional resume for each job application. "
            "Instead of using a generic template, you can handpick the specific sections, skills, and details that best match the role you’re applying for.\n\n"
            "Key Features:\n\n"
            "1. Custom Title & Content\n"
            "   - Create a unique resume title and tailor each section exactly how you want it.\n"
            "   - Decide which personal information, skills, education, and professional experience to include.\n\n"
            "2. Intuitive Editing & Reordering\n"
            "   - Each resume section has its own editor. Click \"Edit Section\" to open an interface where you can add, edit, remove, and reorder items.\n"
            "   - To modify an individual entry, select it and click \"Edit\" to open a small Item Editor. Make your changes, press \"Done,\" and see the update in the Section Editor.\n"
            "   - Use the Up and Down buttons within the editor to change the order of items (note that the Core Competencies section is auto-sorted and cannot be manually reordered).\n\n"
            "3. Selective Inclusion via Checkboxes\n"
            "   - For sections like Education and Professional Experience, all items are checked by default—since you typically want to include everything.\n"
            "   - For sections with long lists (such as Technical Projects and Core Competencies), items start unchecked. This encourages you to actively choose only the most relevant skills and projects, helping you build a focused, concise resume.\n"
            "   - In the Core Competencies editor, items appear in alphabetical order for easy selection, while in the main window they’re arranged into columns in a way that most optimally uses horizontal space.\n\n"
            "4. Easy Saving & Refreshing\n"
            "   - After making your changes, simply click \"Save\" in the editor to update your resume. The main window refreshes to reflect your updates, ensuring your resume is always current and tailored to your application.\n\n"
            "By guiding you to select what to include—especially in sections with many options—this tool helps you produce a resume that is both comprehensive and sharply focused on your strengths.\n\n"
            "For any questions or feedback, please contact the developer."
        )
        info_text.insert("1.0", information_content)
        info_text.configure(state="disabled")

    def open_editor_window(self):
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Edit Resume Data (JSON)")
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

    # Helper method to write the current master_resume data to data.json
    def write_master_resume(self):
        try:
            with open(self.get_file_path("data.json"), "w") as f:
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
        if section["title"] in ["Professional Experience", "Education"]:
            self.edit_structured_section_content(section)
        else:
            self.edit_simple_section_content(section)

    # ---------------------------
    # SIMPLE SECTION EDITOR
    # ---------------------------
    def edit_simple_section_content(self, section):
        """
        Editor for sections whose content is a list of strings (e.g., Objective, Certifications, etc.).
        Uses buttons named: Add, Edit, Remove, Save, and Cancel.
        Additionally, for sections other than Core Competencies (which auto-sort), a third row of Up and Down buttons
        is provided to change the order.
        Changes made here are kept in memory until Save is pressed.
        If Cancel is pressed a confirmation popup appears and unsaved changes are discarded.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("600x500")
        # Make a backup of the original content for this section
        original_content = copy.deepcopy(section["content"])

        listbox = tk.Listbox(win, width=80)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def refresh_listbox():
            # For Core Competencies, auto-sort alphabetically.
            if section["title"] == "Core Competencies":
                section["content"] = sorted(section["content"], key=lambda s: s.lower())
            listbox.delete(0, tk.END)
            for item in section["content"]:
                listbox.insert(tk.END, item)
        refresh_listbox()
        current_index = [None]

        def on_listbox_select(event):
            selection = listbox.curselection()
            current_index[0] = selection[0] if selection else None
        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        # --- Item Editor for simple sections ---
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
            entry_widget.bind("<Return>", lambda e: "break")  # Enforce single-line
            if not is_new:
                entry_widget.insert(0, section["content"][selected_index].replace("\\n", " "))

            def done_child():
                new_text = entry_widget.get().strip()
                if not new_text:
                    messagebox.showerror("Error", "Item content cannot be empty.")
                    return
                if is_new:
                    section["content"].append(new_text)
                else:
                    section["content"][selected_index] = new_text
                refresh_listbox()
                child_win.destroy()
            ttk.Button(child_win, text="Done", command=done_child, style="Custom.TButton").pack(pady=10)
        # First row of buttons: Add, Edit, Remove
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Add", command=lambda: open_edit_window(is_new=True), style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=lambda: open_edit_window(is_new=False), style="Custom.TButton").pack(side="left", padx=5)
        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    refresh_listbox()
            else:
                messagebox.showerror("Error", "No item selected to remove.")
        ttk.Button(btn_frame, text="Remove", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)

        # --- For sections other than Core Competencies, add Up/Down buttons to reorder ---
        if section["title"] != "Core Competencies":
            order_frame = ttk.Frame(win)
            order_frame.pack(fill="x", padx=10, pady=5)
            def move_up():
                if current_index[0] is None:
                    messagebox.showerror("Error", "No item selected to move.")
                    return
                idx = current_index[0]
                if idx <= 0:
                    return
                section["content"][idx-1], section["content"][idx] = section["content"][idx], section["content"][idx-1]
                current_index[0] = idx - 1
                refresh_listbox()
                listbox.selection_set(current_index[0])
            def move_down():
                if current_index[0] is None:
                    messagebox.showerror("Error", "No item selected to move.")
                    return
                idx = current_index[0]
                if idx >= len(section["content"]) - 1:
                    return
                section["content"][idx+1], section["content"][idx] = section["content"][idx], section["content"][idx+1]
                current_index[0] = idx + 1
                refresh_listbox()
                listbox.selection_set(current_index[0])
            ttk.Button(order_frame, text="Up", command=move_up, style="Custom.TButton").pack(side="left", padx=5)
            ttk.Button(order_frame, text="Down", command=move_down, style="Custom.TButton").pack(side="left", padx=5)

        # --- Save and Cancel buttons for the content editor ---
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

        bottom_frame = ttk.Frame(win)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(bottom_frame, text="Save", command=save_content_editor, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Cancel", command=cancel_content_editor, style="Custom.TButton").pack(side="left", padx=10)

    # ---------------------------
    # STRUCTURED SECTION EDITOR
    # ---------------------------
    def edit_structured_section_content(self, section):
        """
        Structured editor for Professional Experience and Education.
        Uses per-field editors and uses buttons named:
        Add, Edit, Remove, Save, and Cancel.
        Additionally, a third row of Up and Down buttons is provided to change the order.
        Changes are kept in memory until Save is pressed.
        If Cancel is pressed, a confirmation popup appears and unsaved changes are discarded.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("800x600")
        original_content = copy.deepcopy(section["content"])

        main_frame = ttk.Frame(win)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left frame: Listbox for items
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        listbox = tk.Listbox(left_frame, width=30)
        listbox.pack(side="left", fill="y", expand=True)
        scrollbar = ttk.Scrollbar(left_frame, command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        # Right frame: Form for editing fields
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        if section["title"] == "Professional Experience":
            ttk.Label(right_frame, text="Subtitle:", style="Custom.TLabel").pack(anchor="w")
            subtitle_entry = ttk.Entry(right_frame, width=50)
            subtitle_entry.pack(anchor="w", fill="x")
            subtitle_entry.bind("<Key>", self.restrict_quotes)

            ttk.Label(right_frame, text="Date:", style="Custom.TLabel").pack(anchor="w")
            date_entry = ttk.Entry(right_frame, width=50)
            date_entry.pack(anchor="w", fill="x")
            date_entry.bind("<Key>", self.restrict_quotes)

            ttk.Label(right_frame, text="Details (one per line):", style="Custom.TLabel").pack(anchor="w")
            details_text = tk.Text(right_frame, height=10, wrap="word")
            details_text.pack(anchor="w", fill="both", expand=True)
            details_text.bind("<Return>", self.insert_literal_newline)
            details_text.bind("<Key>", self.restrict_quotes)
        elif section["title"] == "Education":
            ttk.Label(right_frame, text="Main Entry:", style="Custom.TLabel").pack(anchor="w")
            main_entry = ttk.Entry(right_frame, width=50)
            main_entry.pack(anchor="w", fill="x")
            main_entry.bind("<Key>", self.restrict_quotes)

            ttk.Label(right_frame, text="Details (one per line):", style="Custom.TLabel").pack(anchor="w")
            details_text = tk.Text(right_frame, height=10, wrap="word")
            details_text.pack(anchor="w", fill="both", expand=True)
            details_text.bind("<Return>", self.insert_literal_newline)
            details_text.bind("<Key>", self.restrict_quotes)

        def refresh_listbox():
            listbox.delete(0, tk.END)
            for idx, item in enumerate(section["content"]):
                if section["title"] == "Professional Experience":
                    summary = f"{item.get('subtitle', 'No Subtitle')} ({item.get('date', '')})"
                elif section["title"] == "Education":
                    summary = item[0] if isinstance(item, list) and item else "No Main Entry"
                listbox.insert(tk.END, summary)
        refresh_listbox()
        current_index = [None]

        def on_listbox_select(event):
            selection = listbox.curselection()
            if selection:
                current_index[0] = selection[0]
                item = section["content"][current_index[0]]
                if section["title"] == "Professional Experience":
                    subtitle_entry.delete(0, tk.END)
                    subtitle_entry.insert(0, item.get("subtitle", ""))
                    date_entry.delete(0, tk.END)
                    date_entry.insert(0, item.get("date", ""))
                    details_text.delete("1.0", tk.END)
                    details_text.insert("1.0", "\\n".join(item.get("details", [])))
                elif section["title"] == "Education":
                    main_entry.delete(0, tk.END)
                    if isinstance(item, list) and len(item) > 0:
                        main_entry.insert(0, item[0])
                    details_text.delete("1.0", tk.END)
                    if isinstance(item, list) and len(item) > 1:
                        details_text.insert("1.0", "\\n".join(item[1:]))
            else:
                current_index[0] = None

        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        # --- Item Editor for structured sections ---
        def add_item():
            current_index[0] = None
            if section["title"] == "Professional Experience":
                subtitle_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                details_text.delete("1.0", tk.END)
            elif section["title"] == "Education":
                main_entry.delete(0, tk.END)
                details_text.delete("1.0", tk.END)
        def done_edit():
            if section["title"] == "Professional Experience":
                new_item = {
                    "subtitle": subtitle_entry.get().strip(),
                    "date": date_entry.get().strip(),
                    "details": [line.strip() for line in details_text.get("1.0", tk.END).replace("\\n", "").splitlines() if line.strip()]
                }
            elif section["title"] == "Education":
                new_main = main_entry.get().strip()
                details_lines = [line.strip() for line in details_text.get("1.0", tk.END).replace("\\n", "").splitlines() if line.strip()]
                new_item = [new_main] + details_lines if new_main else []
            if current_index[0] is not None:
                section["content"][current_index[0]] = new_item
            else:
                if section["title"] == "Professional Experience" and new_item["subtitle"]:
                    section["content"].append(new_item)
                elif section["title"] == "Education" and new_item:
                    section["content"].append(new_item)
            refresh_listbox()
        # First row of buttons: Add, Edit, Remove
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Add", command=add_item, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit", command=done_edit, style="Custom.TButton").pack(side="left", padx=5)
        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    refresh_listbox()
            else:
                messagebox.showerror("Error", "No item selected to remove.")
        ttk.Button(btn_frame, text="Remove", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)

        # --- Order manipulation buttons (Up and Down) for structured sections ---
        order_frame = ttk.Frame(win)
        order_frame.pack(fill="x", padx=10, pady=5)
        def move_up():
            if current_index[0] is None:
                messagebox.showerror("Error", "No item selected to move.")
                return
            idx = current_index[0]
            if idx <= 0:
                return
            section["content"][idx-1], section["content"][idx] = section["content"][idx], section["content"][idx-1]
            current_index[0] = idx - 1
            refresh_listbox()
            listbox.selection_set(current_index[0])
        def move_down():
            if current_index[0] is None:
                messagebox.showerror("Error", "No item selected to move.")
                return
            idx = current_index[0]
            if idx >= len(section["content"]) - 1:
                return
            section["content"][idx+1], section["content"][idx] = section["content"][idx], section["content"][idx+1]
            current_index[0] = idx + 1
            refresh_listbox()
            listbox.selection_set(current_index[0])
        ttk.Button(order_frame, text="Up", command=move_up, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(order_frame, text="Down", command=move_down, style="Custom.TButton").pack(side="left", padx=5)

        # --- Save and Cancel buttons for the structured content editor ---
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
        bottom_frame = ttk.Frame(win)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(bottom_frame, text="Save", command=save_content_editor, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(bottom_frame, text="Cancel", command=cancel_content_editor, style="Custom.TButton").pack(side="left", padx=10)

    def create_gui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)
        ttk.Button(top_frame, text="Edit Resume Data", command=self.open_editor_window, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Reset to Default Data", command=self.reset_to_default, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="View Files", command=self.open_app_directory, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Information", command=self.open_information_window, style="Custom.TButton").pack(side="left", padx=10)
        # New UI Settings editor button:
        ttk.Button(top_frame, text="Edit UI Settings", command=self.open_ui_settings_editor, style="Custom.TButton").pack(side="left", padx=10)

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
        self.canvas.bind("<Enter>", self.bind_mousewheel)
        self.canvas.bind("<Leave>", self.unbind_mousewheel)

        for section in self.master_resume:
            self.add_section_widgets(self.scrollable_frame, section)

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", pady=10)
        ttk.Label(bottom_frame, text="Output File Name:", style="Custom.TLabel").pack(side="left", padx=5)
        entry = ttk.Entry(bottom_frame, textvariable=self.output_file_name_var, width=30)
        entry.pack(side="left", padx=5)
        entry.configure(font=("Arial", self.get_main_font_size()))
        ttk.Button(bottom_frame, text="Generate Resume", command=self.generate_resume, style="Custom.TButton").pack(side="left", padx=10)

    def bind_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel_mac)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel_mac)

    def unbind_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, event):
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def on_mousewheel_mac(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def add_section_widgets(self, parent, section):
        section_var = tk.BooleanVar(value=True)
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

    def add_objective_options(self, parent, options):
        for option in options:
            label_frame = ttk.Frame(parent)
            label_frame.pack(anchor="w", pady=2)
            ttk.Radiobutton(
                label_frame,
                variable=self.selected_objective,
                value=option,
                style="Custom.TRadiobutton"
            ).pack(side="left")
            ttk.Label(label_frame, text=option, wraplength=self.wrap_length, style="Custom.TLabel").pack(side="left")
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

    def add_education_options(self, parent, education_content, section_title):
        for entry in education_content:
            main_entry = entry[0]
            var = tk.BooleanVar(value=True)
            self.subsection_vars[(section_title, main_entry)] = var
            ttk.Checkbutton(parent, text=main_entry, variable=var, style="Custom.TCheckbutton").pack(anchor="w")

    def add_suboptions(self, parent, options, section_title):
        if section_title == "Core Competencies":
            sorted_options = sorted(options, key=len, reverse=True)
            n = len(sorted_options)
            rearranged_options = [None] * n
            middle_indexes = range(1, n, 3)
            for i, index in enumerate(middle_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[i]
            first_indexes = range(0, n, 3)
            for i, index in enumerate(first_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[len(middle_indexes) + i]
            last_indexes = range(2, n, 3)
            for i, index in enumerate(last_indexes):
                if index < n:
                    rearranged_options[index] = sorted_options[len(middle_indexes) + len(first_indexes) + i]
            num_columns = 3
            columns = [[] for _ in range(num_columns)]
            for idx, option in enumerate(rearranged_options):
                if option:
                    columns[idx % num_columns].append(option)
            core_frame = ttk.Frame(parent)
            core_frame.pack(fill="x", padx=20)
            for col_idx, column in enumerate(columns):
                column_frame = ttk.Frame(core_frame)
                column_frame.pack(side="left", padx=10, anchor="n")
                for option in column:
                    var = tk.BooleanVar(value=False)
                    self.subsection_vars[(section_title, option)] = var
                    ttk.Checkbutton(column_frame, text=option, variable=var, style="Custom.TCheckbutton").pack(anchor="w")
        else:
            for option in options:
                if isinstance(option, dict):
                    subtitle = option["subtitle"]
                    var = tk.BooleanVar(value=True)
                    self.subsection_vars[(section_title, subtitle)] = var
                    ttk.Checkbutton(parent, text=subtitle, variable=var, style="Custom.TCheckbutton").pack(anchor="w")
                else:
                    # For Technical Projects, default to unchecked.
                    initial_state = False if section_title == "Technical Projects" else True
                    var = tk.BooleanVar(value=initial_state)
                    self.subsection_vars[(section_title, option)] = var
                    if section_title == "Technical Projects":
                        frame = ttk.Frame(parent)
                        frame.pack(fill="x", pady=2)
                        ttk.Checkbutton(frame, text="", variable=var, style="Custom.TCheckbutton").pack(side="left", padx=5)
                        ttk.Label(frame, text=option, wraplength=self.wrap_length, style="Custom.TLabel", justify="left").pack(side="left")
                    else:
                        ttk.Checkbutton(parent, text=option, variable=var, style="Custom.TCheckbutton").pack(anchor="w")

    def toggle_suboptions(self, section_title, enabled):
        for key, var in self.subsection_vars.items():
            if isinstance(key, tuple) and key[0] == section_title:
                if not enabled:
                    var.set(False)
                elif section_title not in ["Core Competencies", "Technical Projects"]:
                    var.set(True)

    def generate_resume(self):
        selected_sections = []
        for section in self.master_resume:
            if self.section_vars[section["title"]].get():
                if section["title"] == "Personal Information":
                    section_data = {"title": section["title"], "content": section["content"]}
                elif section["title"] == "Objective":
                    selected_objectives = []
                    if self.selected_objective.get() == "Custom":
                        custom_text = self.custom_objective_text.get().strip()
                        if custom_text:
                            selected_objectives.append(custom_text)
                    else:
                        selected_objectives.append(self.selected_objective.get())
                    section_data = {"title": section["title"], "content": selected_objectives}
                elif section["title"] == "Education":
                    section_content = []
                    for entry in section["content"]:
                        main_entry = entry[0]
                        if self.subsection_vars[(section["title"], main_entry)].get():
                            entry_data = [main_entry] + entry[1:]
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
        output_directory = self.get_app_directory() if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        output_file_name = f"{self.output_file_name_var.get().strip()}.docx"
        output_file_path = os.path.join(output_directory, output_file_name)
        try:
            generate_resume(selected_sections, output_file=output_file_path)
            if os.name == 'posix':
                os.system(f'open "{output_file_path}"')
            elif os.name == 'nt':
                os.startfile(output_file_path)
            else:
                print(f"Resume generated as {output_file_name}. Open it manually.")
        except Exception as e:
            print(f"Error generating resume: {e}")

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
            self.load_master_resume()
            self.create_styles()
            self.set_dimensions()
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    continue
                widget.destroy()
            self.create_gui()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorGUI(root)
    root.mainloop()
