تمام ✅
إليك النسخة المعدّلة من الملف (بالإنجليزية كما هو، لكن بدون سطر **`pip install -r requirements.txt`**)
ومع تعديل فقرة التثبيت لتوضيح أن البرنامج لا يحتاج أي مكتبات إضافية:

---

# 📂 File Organizer

A simple, flexible, and now **multi-interface tool** written in Python to automatically **organize files** inside a folder.
You can use it either from the **command-line (CLI)** or with a **graphical interface (GUI)**.

It provides two organization modes:

1. **Type-based organization** → Group files into folders by file type (Videos, Images, Documents, Audio, etc.)
2. **Name-based organization** → Create individual folders for each file using its filename (without extension)

---

## 🚀 Features

* Organize files **by type** or **by name**
* **Move** or **Copy** files
* **Dry-run mode** → simulate actions without making changes
* **Conflict resolution**:

  * `skip` → ignore existing files
  * `overwrite` → replace existing files
  * `rename` → auto-rename to avoid conflicts
* **Recursive processing** → include subdirectories if needed
* **Custom categorization** → JSON config for file extension mappings
* **Logging system** → display actions in console and optionally save to a log file
* **Graphical User Interface (GUI)** with:

  * Folder selection
  * Mode, Action, and Conflict Policy options
  * **Progress Bar** to show operation progress
  * **i18n support (multi-language)** → currently English / Arabic
* **Windows Batch File (.bat)** included for quick launch with double-click

---

## 🛠 Installation

1. Clone or download this repository.
2. Make sure you have **Python 3.13.7** (or later) installed.
3. No external libraries are required — everything works with Python’s built-in modules.

*(Optional)* You may install extra utilities like `tqdm`, `colorama`, or `rich` if you want prettier terminal output.

---

## 📌 Usage (CLI)

Run the script from terminal:

```bash
python File-Organizer.py "C:\path\to\folder" --mode type --action move
```

### Examples

* **Organize by type** and move files:

```bash
python File-Organizer.py "C:\Users\You\Downloads" --mode type --action move
```

* **Organize by name** and copy files:

```bash
python File-Organizer.py "C:\Users\You\Documents" --mode name --action copy
```

* **Dry-run mode** (no changes applied):

```bash
python File-Organizer.py "C:\Users\You\Desktop" --mode type --dry-run
```

* **Using a custom JSON mapping**:

```bash
python File-Organizer.py "C:\Data" --mode type --config custom_mapping.json
```

---

## 🖥 Usage (GUI)

To run the graphical version:

```bash
python File-Organizer-GUI.py
```

Or simply double-click the **`Run-Organizer.bat`** file (on Windows).

GUI Features:

* Select source folder via file picker
* Choose mode, action, and conflict resolution policy
* Enable recursive or dry-run options
* Progress bar to show number of processed files
* Log area to display actions
* Language selector (English / Arabic)

---

## ⚙️ JSON Configuration Example

Example `custom_mapping.json` file:

```json
{
  "Design": [".psd", ".ai", ".xd"],
  "Data": [".csv", ".sql"]
}
```

---

## 📒 Notes

* Default destination folder will be created as **Organized_Files** inside the source folder.
* Works on **Windows, macOS, and Linux**.
* GUI supports multilingual text (currently **English** and **Arabic**).
* On Windows, you can just double-click `Run-Organizer.bat` to start the GUI without opening the terminal.
