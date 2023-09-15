from pathlib import Path

current_directory = Path.cwd()
parent_directory = current_directory.parent
folder_name = "data"
BO_folder_path = parent_directory / folder_name / "BO_files"
TM_folder_path = parent_directory / folder_name / "TM_files"
