from pathlib import Path
from typing import List

from antx.core import get_diffs

from .config import (
    DATA_FOLDER_DIR,
    FILTERED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
)
from .file_utils import count_files_in_folder

ANTX_ERROR_LOG_FILE = "unsuccessful_antx_annotation_transfer.txt"
ANTX_LOG_FILE = "antx_annotation_transfer.txt"


def get_differences(source_text: str, target_text: str) -> List[tuple]:
    diffs = get_diffs(source_text, target_text)
    return list(diffs)


def validate_missing_annotation_condition(diffs: List[tuple]) -> bool:
    missing_annotations = [diff for diff in diffs if diff[0] == -1]
    for missing_annotation in missing_annotations:
        if missing_annotation[1] not in ["་", ""]:
            return False
    return True


def verify_annotation_transfer(
    original_text: str, modified_text: str, modifed_file_name
):
    diffs = get_differences(original_text, modified_text)
    has_extra_annotation = any(diff[0] == 1 for diff in diffs)
    if has_extra_annotation:
        write_to_antx_error_log(modifed_file_name, "Extra annotation found")
    missing_annotation = any(diff[0] == -1 for diff in diffs)
    if missing_annotation:
        if validate_missing_annotation_condition(diffs):
            write_to_antx_log(modifed_file_name)
        write_to_antx_error_log(modifed_file_name, "Missing annotation found.")
    write_to_antx_error_log(modifed_file_name, "File identiacal to original file.")


def write_to_antx_log(filename):
    log_file_path = DATA_FOLDER_DIR / ANTX_LOG_FILE
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{filename}:\n")


def write_to_antx_error_log(filename, error_message):
    error_log_file_path = DATA_FOLDER_DIR / ANTX_LOG_FILE
    with open(error_log_file_path, "a") as log_file:
        log_file.write(f"{filename}: {error_message} \n")


def filter_hyphen_bo(file_name: str) -> str:
    return file_name.replace("-bo", "")


def verify_antx_modification(original_folder_path: Path, modified_folder_path: Path):
    txt_files = modified_folder_path.glob("*.txt")
    file_count = count_files_in_folder(modified_folder_path)
    counter = 1

    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name}...")
        modified_content = txt_file.read_text(encoding="utf-8")

        original_file_name = filter_hyphen_bo(txt_file.name)
        original_file_path = original_folder_path / original_file_name
        original_content = original_file_path.read_text(encoding="utf-8")
        verify_annotation_transfer(original_content, modified_content, txt_file.name)
        counter += 1


if __name__ == "__main__":
    verify_antx_modification(
        FILTERED_TM_FOLDER_DIR, FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR
    )
