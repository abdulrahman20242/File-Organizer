import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import importlib.util
import sys
import json

# تحميل ملف File-Organizer.py كـ Module
file_path = Path(__file__).parent / "File-Organizer.py"
spec = importlib.util.spec_from_file_location("file_organizer", file_path)
file_organizer = importlib.util.module_from_spec(spec)
sys.modules["file_organizer"] = file_organizer
spec.loader.exec_module(file_organizer)


class Translator:
    def __init__(self, lang="en"):
        with open("translations.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.lang = lang

    def set_lang(self, lang):
        if lang in self.data:
            self.lang = lang

    def t(self, key):
        return self.data.get(self.lang, {}).get(key, key)


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.tr = Translator("en")  # الافتراضي: إنجليزي
        self.root.geometry("600x500")

        # Variables
        self.source_dir = tk.StringVar()
        self.mode = tk.StringVar(value="type")
        self.action = tk.StringVar(value="move")
        self.recursive = tk.BooleanVar()
        self.dry_run = tk.BooleanVar()
        self.conflict = tk.StringVar(value="rename")
        self.lang = tk.StringVar(value="en")

        # UI Layout
        self.build_ui()
        self.refresh_ui()

    def build_ui(self):
        # اختيار اللغة
        frm_lang = tk.Frame(self.root, pady=5)
        frm_lang.pack(fill="x")
        self.lbl_lang = tk.Label(frm_lang, text="Language:")
        self.lbl_lang.pack(side="left")
        ttk.Combobox(frm_lang, textvariable=self.lang, values=["en", "ar"], width=5).pack(side="left")
        tk.Button(frm_lang, text="Apply", command=self.change_lang).pack(side="left", padx=5)

        # Source folder selection
        frm_source = tk.Frame(self.root, pady=5)
        frm_source.pack(fill="x")
        self.lbl_source = tk.Label(frm_source, text="Source Folder:")
        self.lbl_source.pack(side="left")
        tk.Entry(frm_source, textvariable=self.source_dir, width=40).pack(side="left", padx=5)
        self.btn_browse = tk.Button(frm_source, text="Browse", command=self.browse_folder)
        self.btn_browse.pack(side="left")

        # Mode selection
        frm_mode = tk.Frame(self.root, pady=5)
        frm_mode.pack(fill="x")
        self.lbl_mode = tk.Label(frm_mode, text="Mode:")
        self.lbl_mode.pack(side="left")
        ttk.Combobox(frm_mode, textvariable=self.mode, values=["type", "name"], width=10).pack(side="left")

        # Action selection
        frm_action = tk.Frame(self.root, pady=5)
        frm_action.pack(fill="x")
        self.lbl_action = tk.Label(frm_action, text="Action:")
        self.lbl_action.pack(side="left")
        ttk.Combobox(frm_action, textvariable=self.action, values=["move", "copy"], width=10).pack(side="left")

        # Conflict policy
        frm_conflict = tk.Frame(self.root, pady=5)
        frm_conflict.pack(fill="x")
        self.lbl_conflict = tk.Label(frm_conflict, text="Conflict Policy:")
        self.lbl_conflict.pack(side="left")
        ttk.Combobox(frm_conflict, textvariable=self.conflict,
                     values=["skip", "overwrite", "rename"], width=12).pack(side="left")

        # Checkboxes
        frm_opts = tk.Frame(self.root, pady=5)
        frm_opts.pack(fill="x")
        self.chk_recursive = tk.Checkbutton(frm_opts, text="Recursive", variable=self.recursive)
        self.chk_recursive.pack(side="left", padx=5)
        self.chk_dryrun = tk.Checkbutton(frm_opts, text="Dry-run", variable=self.dry_run)
        self.chk_dryrun.pack(side="left", padx=5)

        # Run button
        self.btn_run = tk.Button(self.root, text="Run Organizer", command=self.run_organizer, bg="green", fg="white")
        self.btn_run.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)

        # Log area
        self.lbl_log = tk.Label(self.root, text="Log Output:")
        self.lbl_log.pack()
        self.txt_log = tk.Text(self.root, height=12, wrap="word")
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_ui(self):
        self.root.title(self.tr.t("title"))
        self.lbl_lang.config(text=self.tr.t("language"))
        self.lbl_source.config(text=self.tr.t("source"))
        self.btn_browse.config(text=self.tr.t("browse"))
        self.lbl_mode.config(text=self.tr.t("mode"))
        self.lbl_action.config(text=self.tr.t("action"))
        self.lbl_conflict.config(text=self.tr.t("conflict"))
        self.chk_recursive.config(text=self.tr.t("recursive"))
        self.chk_dryrun.config(text=self.tr.t("dry_run"))
        self.btn_run.config(text=self.tr.t("run"))
        self.lbl_log.config(text=self.tr.t("log"))

    def change_lang(self):
        self.tr.set_lang(self.lang.get())
        self.refresh_ui()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_dir.set(folder)

    def run_organizer(self):
        src = self.source_dir.get().strip()
        if not src:
            messagebox.showerror(self.tr.t("error"), self.tr.t("source"))
            return
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):
        self.txt_log.insert("end", self.tr.t("starting") + "\n")
        self.txt_log.see("end")

        try:
            source = Path(self.source_dir.get()).resolve()
            dest = source / "Organized_Files"
            dest.mkdir(exist_ok=True)

            categories = file_organizer.load_custom_mapping(None)

            # عد الملفات لحساب progress
            files = list(source.rglob("*") if self.recursive.get() else source.glob("*"))
            total_files = len([f for f in files if f.is_file()])
            self.progress["value"] = 0
            self.progress["maximum"] = total_files if total_files else 1

            processed = 0
            for item in files:
                if item.is_file():
                    if self.mode.get() == "type":
                        file_organizer.organize_by_type(
                            item, dest, categories, self.action.get(),
                            self.dry_run.get(), self.conflict.get()
                        )
                    else:
                        file_organizer.organize_by_name(
                            item, dest, self.action.get(),
                            self.dry_run.get(), self.conflict.get()
                        )
                    processed += 1
                    self.progress["value"] = processed
                    self.root.update_idletasks()

            self.txt_log.insert("end", self.tr.t("done") + "\n")
        except Exception as e:
            self.txt_log.insert("end", f"{self.tr.t('error')}: {e}\n")

        self.txt_log.see("end")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()
