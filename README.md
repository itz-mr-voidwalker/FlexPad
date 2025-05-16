# FlexPad - CustomTkinter Text Editor

> **FlexPad** is a sleek, dark-themed text editor built using CustomTkinter with all the essential features you need for a smooth writing experience. Lightweight, fast, and loaded with cool features like autosave, font customization, and dark/light mode toggle.

---

## Features

- **Modern CustomTkinter UI** with a clean and user-friendly interface.
- **Autosave** functionality that saves your work automatically after 2 seconds of inactivity.
- **File operations:** New, Open, Save, and Exit.
- **Font Selector:** Customize font size and weight on the fly.
- **Dark/Light mode toggle** for your comfort.
- **Status bar** showing current lines and character count.
- **Keyboard shortcuts:**  
  - `Ctrl + S` to Save  
  - `Ctrl + O` to Open
  - `Ctrl + N` to New File

---
## Logging

This app uses logging extensively to help track its internal operations, errors, and critical events. Logging is essential for debugging and maintaining the app efficiently.

  ## How it works
  - All important events like errors, warnings, and info messages are saved to a log file.
  - The log file is located in your system's temporary directory (e.g., C:\Users\<User>\AppData\Local\Temp\customtkinter_editor.log on Windows).
  - Each log entry is timestamped, so you can see exactly when an event happened.
  - If the app crashes or encounters any issues during file operations or UI actions, the relevant error details are logged.
  - This helps developers or users to diagnose and fix issues faster.


## Installation

Make sure you have Python 3.7+ installed. Then, install the required package:

```
pip install customtkinter
```

## Usage
Run the script:
```
python main.py
```

## Contributing
Feel free to fork and send PRs if you want to improve this editor or add new features. All contributions are welcome!

## License
MIT License — Do whatever the hell you want with this code. Just don't blame me if it breaks! 😎

## Author
𝓜я. ᴠᴇɴɢᴇᴀɴᴄᴇ aka Sai Vignesh