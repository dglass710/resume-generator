import tkinter as tk
import json
import platform
import subprocess
from tkinter import ttk, messagebox
import os
import sys
from math import ceil
from generator import generate_resume

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
        self.section_vars = {}  # Main section checkboxes
        self.subsection_vars = {}  # Sub-options checkboxes
        self.selected_objective = tk.StringVar()
        self.output_file_name_var = tk.StringVar(value="Custom_Resume")

        self.create_gui()

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
        self.update_editor_window_dimensions()

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
            "This application lets you customize and generate professional resumes. "
            "Your data is stored in a JSON file, and you can edit it via the built-in editor.\n\n"
            "Features include:\n"
            "• Editing of sections (Objective, Education, etc.) via the GUI with friendly text boxes.\n"
            "• Dynamic controls (checkboxes, radio buttons, plus buttons for adding items).\n"
            "• Generation of a formatted Word document using the selected data.\n\n"
            "For any help or feedback, please contact the developer."
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
            text="Save Changes",
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

    def edit_section_content(self, section):
        """
        Opens an editor for a given section.
        For Professional Experience and Education, a per-field structured editor is used.
        For all other sections (e.g., Objective, Certifications, Core Competencies, Technical Projects),
        a simple structured editor is used where each list item is edited via a child window.
        """
        if section["title"] in ["Professional Experience", "Education"]:
            self.edit_structured_section_content(section)
        else:
            self.edit_simple_section_content(section)

    def edit_structured_section_content(self, section):
        """
        Structured editor for sections that require per-field editing
        (specifically Professional Experience and Education).
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("800x600")

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

        fields = {}
        if section["title"] == "Professional Experience":
            ttk.Label(right_frame, text="Subtitle:", style="Custom.TLabel").pack(anchor="w")
            subtitle_entry = ttk.Entry(right_frame, width=50)
            subtitle_entry.pack(anchor="w", fill="x")
            fields["subtitle"] = subtitle_entry

            ttk.Label(right_frame, text="Date:", style="Custom.TLabel").pack(anchor="w")
            date_entry = ttk.Entry(right_frame, width=50)
            date_entry.pack(anchor="w", fill="x")
            fields["date"] = date_entry

            ttk.Label(right_frame, text="Details (one per line):", style="Custom.TLabel").pack(anchor="w")
            details_text = tk.Text(right_frame, height=10, wrap="word")
            details_text.pack(anchor="w", fill="both", expand=True)
            fields["details"] = details_text

        elif section["title"] == "Education":
            ttk.Label(right_frame, text="Main Entry:", style="Custom.TLabel").pack(anchor="w")
            main_entry = ttk.Entry(right_frame, width=50)
            main_entry.pack(anchor="w", fill="x")
            fields["main_entry"] = main_entry

            ttk.Label(right_frame, text="Details (one per line):", style="Custom.TLabel").pack(anchor="w")
            details_text = tk.Text(right_frame, height=10, wrap="word")
            details_text.pack(anchor="w", fill="both", expand=True)
            fields["details"] = details_text

        def refresh_listbox():
            listbox.delete(0, tk.END)
            for idx, item in enumerate(section["content"]):
                if section["title"] == "Professional Experience":
                    summary = f"{item.get('subtitle', 'No Subtitle')} ({item.get('date', '')})"
                elif section["title"] == "Education":
                    if isinstance(item, list) and len(item) > 0:
                        summary = item[0]
                    else:
                        summary = "No Main Entry"
                listbox.insert(tk.END, summary)

        refresh_listbox()
        current_index = [None]  # mutable container to hold current index

        def on_listbox_select(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                current_index[0] = idx
                item = section["content"][idx]
                if section["title"] == "Professional Experience":
                    subtitle_entry.delete(0, tk.END)
                    subtitle_entry.insert(0, item.get("subtitle", ""))
                    date_entry.delete(0, tk.END)
                    date_entry.insert(0, item.get("date", ""))
                    details_text.delete("1.0", tk.END)
                    details_text.insert("1.0", "\n".join(item.get("details", [])))
                elif section["title"] == "Education":
                    main_entry.delete(0, tk.END)
                    if isinstance(item, list) and len(item) > 0:
                        main_entry.insert(0, item[0])
                    details_text.delete("1.0", tk.END)
                    if isinstance(item, list) and len(item) > 1:
                        details_text.insert("1.0", "\n".join(item[1:]))

        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        # Bottom button frame for actions
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=5)

        def add_item():
            current_index[0] = None
            if section["title"] == "Professional Experience":
                subtitle_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                details_text.delete("1.0", tk.END)
            elif section["title"] == "Education":
                main_entry.delete(0, tk.END)
                details_text.delete("1.0", tk.END)

        def save_edit():
            if section["title"] == "Professional Experience":
                new_item = {
                    "subtitle": subtitle_entry.get().strip(),
                    "date": date_entry.get().strip(),
                    "details": [line.strip() for line in details_text.get("1.0", tk.END).strip().splitlines() if line.strip()]
                }
            elif section["title"] == "Education":
                new_main = main_entry.get().strip()
                details_lines = [line.strip() for line in details_text.get("1.0", tk.END).strip().splitlines() if line.strip()]
                new_item = [new_main] + details_lines if new_main else []
            if current_index[0] is not None:
                section["content"][current_index[0]] = new_item
            else:
                # Only add if the new item is valid (e.g., has a subtitle/main entry)
                if section["title"] == "Professional Experience" and new_item["subtitle"]:
                    section["content"].append(new_item)
                elif section["title"] == "Education" and new_item:
                    section["content"].append(new_item)
            self.write_master_resume()
            refresh_listbox()

        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    self.write_master_resume()
                    refresh_listbox()

        ttk.Button(btn_frame, text="Add New", command=add_item, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save Entry", command=save_edit, style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)

    def edit_simple_section_content(self, section):
        """
        Simple structured editor for sections whose content is a list of strings
        (e.g., Objective, Certifications, Core Competencies, Technical Projects).
        This editor uses a full-window listbox to display items and opens a child window for adding or editing an item.
        """
        win = tk.Toplevel(self.root)
        win.title(f"Edit Content for {section['title']}")
        win.geometry("600x500")

        # Use the full window for the listbox and scrollbar
        listbox = tk.Listbox(win, width=80)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        def refresh_listbox():
            listbox.delete(0, tk.END)
            for item in section["content"]:
                listbox.insert(tk.END, item)

        refresh_listbox()
        current_index = [None]

        def on_listbox_select(event):
            selection = listbox.curselection()
            if selection:
                current_index[0] = selection[0]
            else:
                current_index[0] = None

        listbox.bind("<<ListboxSelect>>", on_listbox_select)

        # Function to open a child window for adding or editing an item
        def open_edit_window(is_new=False):
            if not is_new and current_index[0] is None:
                messagebox.showerror("Error", "No item selected for editing.")
                return
            child_win = tk.Toplevel(win)
            if is_new:
                child_win.title(f"Add New Item for {section['title']}")
            else:
                child_win.title(f"Edit Item for {section['title']}")
            child_win.geometry("400x300")

            ttk.Label(child_win, text="Item Content:", style="Custom.TLabel").pack(anchor="w", padx=10, pady=5)
            text_widget = tk.Text(child_win, height=10, wrap="word")
            text_widget.pack(fill="both", expand=True, padx=10, pady=5)

            if not is_new:
                text_widget.insert("1.0", section["content"][current_index[0]])

            def save_child():
                new_text = text_widget.get("1.0", tk.END).strip()
                if not new_text:
                    messagebox.showerror("Error", "Item content cannot be empty.")
                    return
                if is_new:
                    section["content"].append(new_text)
                else:
                    section["content"][current_index[0]] = new_text
                self.write_master_resume()
                refresh_listbox()
                child_win.destroy()

            ttk.Button(child_win, text="Save", command=save_child, style="Custom.TButton").pack(pady=10)

        # Bottom button frame for actions
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Add New", command=lambda: open_edit_window(is_new=True), style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=lambda: open_edit_window(is_new=False), style="Custom.TButton").pack(side="left", padx=5)
        def remove_item():
            if current_index[0] is not None:
                if messagebox.askyesno("Confirm", "Remove selected item?"):
                    del section["content"][current_index[0]]
                    current_index[0] = None
                    self.write_master_resume()
                    refresh_listbox()
            else:
                messagebox.showerror("Error", "No item selected to remove.")
        ttk.Button(btn_frame, text="Remove Selected", command=remove_item, style="Custom.TButton").pack(side="left", padx=5)

    def create_gui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)
        ttk.Button(top_frame, text="Edit Resume Data", command=self.open_editor_window, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Reset to Default Data", command=self.reset_to_default, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="View Files", command=self.open_app_directory, style="Custom.TButton").pack(side="left", padx=10)
        ttk.Button(top_frame, text="Information", command=self.open_information_window, style="Custom.TButton").pack(side="left", padx=10)

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
        self.custom_objective_text = tk.Text(custom_frame, height=5, width=50, wrap="word")
        self.custom_objective_text.pack(side="left", padx=5)
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
                    initial_state = True
                    var = tk.BooleanVar(value=initial_state)
                    self.subsection_vars[(section_title, subtitle)] = var
                    ttk.Checkbutton(parent, text=subtitle, variable=var, style="Custom.TCheckbutton").pack(anchor="w")
                else:
                    initial_state = True
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
                        custom_text = self.custom_objective_text.get("1.0", tk.END).strip()
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
        if getattr(sys, 'frozen', False):
            output_directory = self.get_app_directory()
        else:
            output_directory = os.path.dirname(os.path.abspath(__file__))
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
