import argparse
import shutil
import json
from pathlib import Path
import mimetypes

# =========================
# Translator Class (i18n)
# =========================
class Translator:
    def __init__(self, lang_file="lang_en.json"):
        lang_path = Path(lang_file)
        if lang_path.exists():
            with open(lang_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            self.translations = {}

    def t(self, key, **kwargs):
        text = self.translations.get(key, key)
        return text.format(**kwargs)


# =========================
# Helper functions
# =========================
def load_custom_mapping(config_path):
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def detect_category(file_path: Path, categories: dict) -> str:
    # أولاً: جرب بالـ JSON mapping
    ext = file_path.suffix.lower()
    for category, exts in categories.items():
        if ext in exts:
            return category

    # ثانياً: جرب بالـ mimetypes
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type:
        if mime_type.startswith("image"):
            return "Images"
        elif mime_type.startswith("video"):
            return "Videos"
        elif mime_type.startswith("audio"):
            return "Audio"
        elif mime_type.startswith("text") or mime_type in [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]:
            return "Documents"

    # لو فشل → Others
    return "Others"


def handle_conflict(dest: Path, conflict_policy: str) -> Path:
    if not dest.exists():
        return dest

    if conflict_policy == "skip":
        return None
    elif conflict_policy == "overwrite":
        return dest
    elif conflict_policy == "rename":
        counter = 1
        new_dest = dest
        while new_dest.exists():
            new_dest = dest.with_name(f"{dest.stem}_{counter}{dest.suffix}")
            counter += 1
        return new_dest
    else:
        return None


def process_directory(
    source: Path,
    dest: Path,
    mode: str,
    action: str,
    dry_run: bool,
    recursive: bool,
    conflict_policy: str,
    categories: dict,
    tr: Translator,
):
    print(tr.t("starting"))

    files = source.rglob("*") if recursive else source.glob("*")

    for file in files:
        if file.is_file():
            if mode == "type":
                category = detect_category(file, categories)
                target_folder = dest / category
                target_folder.mkdir(parents=True, exist_ok=True)
                target_path = target_folder / file.name
            elif mode == "name":
                target_folder = dest / file.stem
                target_folder.mkdir(parents=True, exist_ok=True)
                target_path = target_folder / file.name
            else:
                continue

            final_path = handle_conflict(target_path, conflict_policy)
            if final_path is None:
                print(tr.t("skipped", file=file.name))
                continue

            if dry_run:
                print(tr.t("dryrun", src=file, dest=final_path))
            else:
                try:
                    if action == "move":
                        shutil.move(str(file), str(final_path))
                        print(tr.t("moved", src=file, dest=final_path))
                    elif action == "copy":
                        shutil.copy2(str(file), str(final_path))
                        print(tr.t("copied", src=file, dest=final_path))
                except Exception as e:
                    print(tr.t("error", msg=str(e)))

    print(tr.t("done"))


# =========================
# Main CLI
# =========================
def main():
    parser = argparse.ArgumentParser(description="📂 File Organizer with i18n")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("--mode", choices=["type", "name"], default="type", help="Organization mode")
    parser.add_argument("--action", choices=["move", "copy"], default="move", help="Move or copy files")
    parser.add_argument("--dry-run", action="store_true", help="Simulation without changes")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders")
    parser.add_argument("--conflict", choices=["skip", "overwrite", "rename"], default="rename", help="Conflict policy")
    parser.add_argument("--config", help="JSON config for custom extension mapping")
    parser.add_argument("--lang", default="lang_en.json", help="Language file (default: lang_en.json)")

    args = parser.parse_args()

    source = Path(args.source).resolve()
    dest = source / "Organized_Files"
    dest.mkdir(exist_ok=True)

    categories = load_custom_mapping(args.config)
    tr = Translator(args.lang)

    process_directory(
        source=source,
        dest=dest,
        mode=args.mode,
        action=args.action,
        dry_run=args.dry_run,
        recursive=args.recursive,
        conflict_policy=args.conflict,
        categories=categories,
        tr=tr,
    )


if __name__ == "__main__":
    main()
