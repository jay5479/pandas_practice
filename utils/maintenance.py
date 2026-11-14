# imports for cleaning data files created by this module, ignore for studies
from pathlib import Path
import shutil


def cleanup(folder_to_cleanup :str):
    """To clean up folder contents after studies"""

    # Point to the 'data' folder in your project root
    data_dir = Path(folder_to_cleanup)

    # Check that the folder exists before trying to empty it
    if data_dir.exists() and data_dir.is_dir():
        for item in data_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()  # Delete files and shortcuts
            elif item.is_dir():
                shutil.rmtree(item)  # Delete subfolders and their contents
        print(f"Successfully emptied '{data_dir}'.")
    else:
        print(f"Folder '{data_dir}' does not exist.")