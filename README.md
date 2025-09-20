# 📂 File Organizer

A simple and flexible command-line tool written in Python to automatically **organize files** inside a folder.

It provides two organization modes:
1. **Type-based organization** → Group files into folders by file type (Videos, Images, Documents, Audio, etc.)
2. **Name-based organization** → Create individual folders for each file using its filename (without extension)

---

## 🚀 Features

- Organize files **by type** or **by name**
- **Move** or **Copy** files
- **Dry-run mode** → simulate actions without making changes
- **Conflict resolution**:
  - `skip` → ignore existing files
  - `overwrite` → replace existing files
  - `rename` → auto-rename to avoid conflicts
- **Recursive processing** → include subdirectories if needed
- **Custom categorization** → JSON config for file extension mappings
- **Logging system** → display actions in console and optionally save to a log file

---

## 🛠 Installation

1. Clone or download this repository.
2. Make sure you have **Python 3.13.7** (or later).
3. Install dependencies (none required here, but just in case):

```bash
pip install -r requirements.txt


---

📌 Usage

Run the script from terminal:
```bash
python file_organizer.py "C:\path\to\folder" --mode type --action move
