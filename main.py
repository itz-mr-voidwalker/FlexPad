import customtkinter as ctk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import logging
import os
import tempfile

# Configure logging
log_dir = tempfile.gettempdir()
log_file = os.path.join(log_dir, "customtkinter_editor.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Appearance & theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class CustomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FlexPad - CustomTkinter Editor")
        self.file_path = ''
        self.geometry("900x650")
        self.minsize(650, 450)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.autosave_id = None  # autosave timer id

        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        self._create_header()
        self._create_textbox()
        self._create_footer()
        self._create_appearance_toggle()

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(self, height=50)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(5, weight=1)

        self.file_button = ctk.CTkButton(
            self.header_frame, text="File", width=80,
            fg_color="#152973", hover_color="#3854c3",
            command=self.open_file_menu
        )
        self.file_button.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.format_button = ctk.CTkButton(
            self.header_frame, text="Format", width=80,
            fg_color="#152973", hover_color="#3854c3",
            command=self.open_font_selector
        )
        self.format_button.grid(row=0, column=1, padx=10, pady=8, sticky="w")

    def _create_textbox(self):
        self.textbox = ctk.CTkTextbox(
            self, corner_radius=10,
            font=ctk.CTkFont(size=16),
            border_width=1, border_color="#3a3f54",
            wrap="word"
        )
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 5))
        self.textbox.insert("0.0", "Welcome to FlexPad!\nStart typing your masterpiece here...")
        

    def _create_footer(self):
        self.footer_frame = ctk.CTkFrame(self, height=30)
        self.footer_frame.grid(row=2, column=0, sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.footer_frame, text="Lines: 1  Characters: 0",
            font=ctk.CTkFont(size=12), anchor="w", padx=10
        )
        self.status_label.grid(row=0, column=0, sticky="w")

    def _create_appearance_toggle(self):
        self.appearance_toggle = ctk.CTkSwitch(
            self.header_frame, text="Light Mode", command=self.toggle_appearance
        )
        self.appearance_toggle.grid(row=0, column=4, padx=20)

    def _bind_events(self):
        self.textbox.bind("<<Modified>>", self.update_status)
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-n>", lambda e: self.new_file())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_status(self, event=None):
        try:
            self.textbox.edit_modified(False)
            content = self.textbox.get("0.0", "end-1c")
            lines = content.count('\n') + 1 if content else 0
            chars = len(content)
            self.status_label.configure(text=f"Lines: {lines}  Characters: {chars}")
            # Schedule autosave after 2 sec of inactivity
            if self.autosave_id:
                self.after_cancel(self.autosave_id)
            self.autosave_id = self.after(60000, self.autosave)
        except Exception as e:
            logging.error(f"Error updating status: {e}")

    def autosave(self):
        if not self.file_path:
            # Prompt only once for new file autosave
            if messagebox.askyesno("Save File", "File not saved yet. Do you want to save now?"):
                self.save_file()
            else:
                return
        else:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.textbox.get("0.0", "end-1c"))
                logging.info(f"Autosaved to {self.file_path}")
            except Exception as e:
                logging.error(f"Autosave failed: {e}")

    def open_font_selector(self):
        if hasattr(self, 'font_win') and self.font_win.winfo_exists():
            self.font_win.focus()
            return
        self.font_win = ctk.CTkToplevel(self)
        self.font_win.title("Font Selector")
        self.font_win.geometry("360x220")
        self.font_win.configure(fg_color="#22252a")
        self.font_win.attributes("-topmost", True)
        self.font_win.resizable(False, False)
        self.font_win.geometry(f"+{self.winfo_x() + 100}+{self.winfo_y() + 100}")

        ctk.CTkLabel(self.font_win, text="Font Weight:").pack(anchor="w", padx=20, pady=(20, 4))
        self.font_weight_var = ctk.StringVar(value="normal")
        ctk.CTkOptionMenu(self.font_win, values=["normal", "bold"], variable=self.font_weight_var, width=280).pack(padx=20, pady=(0, 15))

        ctk.CTkLabel(self.font_win, text="Font Size:").pack(anchor="w", padx=20, pady=(0, 4))
        self.font_size_var = ctk.StringVar(value="16")
        font_sizes = [str(size) for size in range(8, 49, 2)]
        ctk.CTkOptionMenu(self.font_win, values=font_sizes, variable=self.font_size_var, width=280).pack(padx=20, pady=(0, 20))

        ctk.CTkButton(self.font_win, text="Apply", width=120, command=lambda: self.apply_font_settings(self.font_win)).pack(pady=(0, 20))

        # On close cleanup attribute
        def on_close():
            self.font_win.destroy()
            delattr(self, 'font_win')

        self.font_win.protocol("WM_DELETE_WINDOW", on_close)

    def apply_font_settings(self, font_win):
        try:
            weight = self.font_weight_var.get()
            size = int(self.font_size_var.get())
            family = "Arial"
            new_font = (family, size, weight)
            self.textbox.configure(font=new_font)
            font_win.destroy()
            self.update_status()
        except Exception as e:
            logging.error(f"Failed to apply font: {e}")

    def open_file_menu(self):
        if hasattr(self, 'menu_win') and self.menu_win.winfo_exists():
            self.menu_win.focus()
            return
        self.menu_win = ctk.CTkToplevel(self)
        self.menu_win.title("File Menu")
        self.menu_win.geometry("250x220")
        self.menu_win.configure(fg_color="#22252a")
        self.menu_win.attributes("-topmost", True)
        self.menu_win.resizable(False, False)
        self.menu_win.geometry(f"+{self.winfo_x() + 50}+{self.winfo_y() + 70}")

        ctk.CTkButton(self.menu_win, text="New", command=self.new_file).pack(pady=(15, 8), padx=30, fill="x")
        ctk.CTkButton(self.menu_win, text="Open", command=self.open_file).pack(pady=8, padx=30, fill="x")
        ctk.CTkButton(self.menu_win, text="Save", command=self.save_file).pack(pady=8, padx=30, fill="x")
        ctk.CTkButton(self.menu_win, text="Exit", fg_color="#d9534f", hover_color="#c9302c", command=self.quit).pack(pady=(8, 15), padx=30, fill="x")

        # On close cleanup attribute
        def on_close():
            self.menu_win.destroy()
            delattr(self, 'menu_win')

        self.menu_win.protocol("WM_DELETE_WINDOW", on_close)

    def new_file(self):
        if messagebox.askyesno("New File", "Are you sure you want to start a new file? Unsaved changes will be lost."):
            self.textbox.delete("0.0", "end")
            self.file_path = ''
            if hasattr(self, 'menu_win'):
                self.menu_win.destroy()
                delattr(self, 'menu_win')
            self.update_status()
            self.title("FlexPad - New")

    def open_file(self):
        try:
            if hasattr(self, 'menu_win'):
                self.menu_win.destroy()
                delattr(self, 'menu_win')
            path = askopenfilename(filetypes=[("Text Files", "*.txt")], title="Open your File")
            if not path:
                return
            with open(path, 'r') as file:
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", file.read())
                self.title(f"FlexPad - {os.path.basename(path)}")
                self.file_path = path
                self.update_status()
        except Exception as e:
            logging.error(f"Error opening file: {e}")

    def save_file(self):
        try:
            if hasattr(self, 'menu_win'):
                self.menu_win.destroy()
                delattr(self, 'menu_win')
            if not self.file_path:
                self.file_path = asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Save your legendary file as..."
                )
            if not self.file_path:
                return
            with open(self.file_path, 'w') as file:
                file.write(self.textbox.get("0.0", "end-1c"))
                self.title(f"FlexPad - {os.path.basename(self.file_path)}")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def toggle_appearance(self):
        mode = "light" if self.appearance_toggle.get() else "dark"
        ctk.set_appearance_mode(mode)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit? Unsaved changes will be lost."):
            self.destroy()

if __name__ == "__main__":
    try:
        app = CustomApp()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Application crashed: {e}")
