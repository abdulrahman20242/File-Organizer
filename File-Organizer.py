#!/usr/bin/env python3
"""
File Organizer Tool
-------------------
Organize files inside a folder by type or by name.

Features:
- Organize by type (Videos, Images, Documents, Audio, etc.)
- Organize by name (each file gets its own folder)
- Move or Copy files
- Dry-run mode
- Conflict resolution: skip, overwrite, rename
- Recursive option to include subfolders
- Custom categorization via JSON config
- Logging (console + optional log file)

Usage:
    python File-Organizer.py "C:\path\to\folder" --mode type --action move --recursive
"""

import argparse
import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional

# Default file type mappings
DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".odt"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".php", ".rb"],
    "Programs": [".exe",],
    "Others": []
}


def load_custom_mapping(path: Optional[str]) -> Dict[str, list]:
    """Load custom extension mapping from JSON file if provided."""
    if not path:
        return DEFAULT_CATEGORIES
    try:
        with open(path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        return {**DEFAULT_CATEGORIES, **mapping}  # merge with defaults
    except Exception as e:
        logging.error(f"Failed to load custom mapping file: {e}")
        return DEFAULT_CATEGORIES


def resolve_conflict(destination: Path, conflict_policy: str) -> Path:
    """Resolve file conflicts based on the chosen policy."""
    if not destination.exists():
        return destination

    if conflict_policy == "skip":
        return None
    elif conflict_policy == "overwrite":
        return destination
    elif conflict_policy == "rename":
        counter = 1
        new_dest = destination
        while new_dest.exists():
            new_dest = destination.with_stem(f"{destination.stem}_{counter}")
            counter += 1
        return new_dest
    else:
        raise ValueError(f"Unknown conflict policy: {conflict_policy}")


def organize_by_type(file: Path, dest_root: Path, categories: Dict[str, list],
                     action: str, dry_run: bool, conflict_policy: str):
    """Organize file into a folder based on type."""
    ext = file.suffix.lower()
    category = next((cat for cat, exts in categories.items() if ext in exts), "Others")
    dest_folder = dest_root / category
    dest_folder.mkdir(parents=True, exist_ok=True)

    dest_file = dest_folder / file.name
    final_dest = resolve_conflict(dest_file, conflict_policy)
    if not final_dest:
        logging.info(f"Skipping (exists): {file}")
        return

    if dry_run:
        logging.info(f"[DRY-RUN] {action.upper()} {file} -> {final_dest}")
        return

    try:
        if action == "move":
            shutil.move(str(file), str(final_dest))
        else:
            shutil.copy2(str(file), str(final_dest))
        logging.info(f"{action.upper()} {file} -> {final_dest}")
    except Exception as e:
        logging.error(f"Failed to {action} {file}: {e}")


def organize_by_name(file: Path, dest_root: Path,
                     action: str, dry_run: bool, conflict_policy: str):
    """Organize file into its own folder by stem (filename)."""
    folder = dest_root / file.stem
    folder.mkdir(parents=True, exist_ok=True)
    dest_file = folder / file.name
    final_dest = resolve_conflict(dest_file, conflict_policy)
    if not final_dest:
        logging.info(f"Skipping (exists): {file}")
        return

    if dry_run:
        logging.info(f"[DRY-RUN] {action.upper()} {file} -> {final_dest}")
        return

    try:
        if action == "move":
            shutil.move(str(file), str(final_dest))
        else:
            shutil.copy2(str(file), str(final_dest))
        logging.info(f"{action.upper()} {file} -> {final_dest}")
    except Exception as e:
        logging.error(f"Failed to {action} {file}: {e}")


def process_directory(source: Path, dest: Path, mode: str, action: str,
                      dry_run: bool, recursive: bool, conflict_policy: str,
                      categories: Dict[str, list]):
    """Process files in directory."""
    files = source.rglob("*") if recursive else source.glob("*")
    for item in files:
        if item.is_file():
            if mode == "type":
                organize_by_type(item, dest, categories, action, dry_run, conflict_policy)
            elif mode == "name":
                organize_by_name(item, dest, action, dry_run, conflict_policy)


def main():
    parser = argparse.ArgumentParser(description="File Organizer Tool")
    parser.add_argument("source", help="Source folder containing files to organize")
    parser.add_argument("--mode", choices=["type", "name"], required=True,
                        help="Organize by type or by name")
    parser.add_argument("--action", choices=["move", "copy"], default="move",
                        help="Choose to move or copy files (default: move)")
    parser.add_argument("--recursive", action="store_true",
                        help="Process subdirectories recursively")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate actions without moving/copying files")
    parser.add_argument("--conflict", choices=["skip", "overwrite", "rename"],
                        default="rename", help="Conflict resolution policy")
    parser.add_argument("--config", help="JSON file with custom extension mappings")
    parser.add_argument("--log", help="Optional log file to save actions")

    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists() or not source.is_dir():
        print("Error: Source folder does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    dest_root = source / "Organized_Files"
    dest_root.mkdir(exist_ok=True)

    # Setup logging
    handlers = [logging.StreamHandler(sys.stdout)]
    if args.log:
        handlers.append(logging.FileHandler(args.log, encoding="utf-8"))
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=handlers)

    categories = load_custom_mapping(args.config)

    process_directory(
        source=source,
        dest=dest_root,
        mode=args.mode,
        action=args.action,
        dry_run=args.dry_run,
        recursive=args.recursive,
        conflict_policy=args.conflict,
        categories=categories,
    )


if __name__ == "__main__":
    main()

