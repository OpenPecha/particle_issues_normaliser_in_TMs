import csv
from collections import OrderedDict
from pathlib import Path
from typing import List, Tuple

from antx.core import get_diffs

from .config import FILTERED_TM_FOLDER_DIR  # noqa
from .config import (
    AFFIX_ISSUES,
    DATA_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
)
from .file_utils import count_files_in_folder

ANTX_ERROR_LOG_FILE = "antx_annotation_transfer_error_log.txt"
ANTX_LOG_FILE = "antx_annotation_transfer_log.txt"


def empty_antx_log_files():
    log_file_path = DATA_FOLDER_DIR / ANTX_LOG_FILE
    error_log_file_path = DATA_FOLDER_DIR / ANTX_ERROR_LOG_FILE

    # Clear the log files if they exist
    if log_file_path.exists():
        log_file_path.unlink()
    if error_log_file_path.exists():
        error_log_file_path.unlink()


def count_affix_in_string(file_content: str):
    affix_counts = OrderedDict((affix, 0) for affix in AFFIX_ISSUES)
    for affix in AFFIX_ISSUES:
        affix_counts[affix] = file_content.count(affix)
    return affix_counts


def count_affix_in_files(folder_path: Path, comparison_folder_path: Path):
    txt_files = folder_path.glob("*.txt")
    data = []

    for txt_file in txt_files:

        file_content = txt_file.read_text(encoding="utf-8")
        file_name_with_issues = filter_hyphen_bo(txt_file.name)
        file_content_with_issues = Path(
            comparison_folder_path / file_name_with_issues
        ).read_text(encoding="utf-8")

        affix_counts = count_affix_in_string(file_content)
        initial_affix_counts = count_affix_in_string(file_content_with_issues)

        affix_counts_values: List = []

        affix_counts_values.extend(
            [f"{key}: ", f"{value1:<6}", f"{value2:<6}"]
            for key, value1, value2 in zip(
                affix_counts.keys(),
                affix_counts.values(),
                initial_affix_counts.values(),
            )
        )

        data.append([f"{txt_file.name:<30}"] + affix_counts_values)

    # Write the data to a CSV file
    output_file = Path(DATA_FOLDER_DIR / "affix_counts_in_TMs.tsv")
    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerows(data)


def get_differences(source_text: str, target_text: str) -> List[tuple]:
    diffs = get_diffs(source_text, target_text)
    return list(diffs)


def validate_missing_annotation_condition(diffs: List[tuple]) -> Tuple[bool, List]:
    missing_annotations = [diff for diff in diffs if diff[0] == -1]
    valid_missing_annotations = ["་", "", "༌"]
    for missing_annotation in missing_annotations:
        if missing_annotation[1] not in valid_missing_annotations:
            return False, [
                diff
                for diff in missing_annotations
                if diff[1] not in valid_missing_annotations
            ]
    return True, []


def validate_extra_annotation_condition(diffs: List[tuple]) -> Tuple[bool, List]:
    extra_annotations = [diff for diff in diffs if diff[0] == 1]
    validate_extra_annotations = [""]
    for extra_annotation in extra_annotations:
        if extra_annotation[1] not in validate_extra_annotations:
            return False, [
                diff
                for diff in extra_annotations
                if diff[1] not in validate_extra_annotations
            ]
    return True, []


def verify_annotation_transfer(
    original_text: str, modified_text: str, modified_file_name: str
):
    diffs = get_differences(original_text, modified_text)
    extra_annotations = [diff for diff in diffs if diff[0] == 1]
    missing_annotations = [diff for diff in diffs if diff[0] == -1]

    if extra_annotations or missing_annotations:
        error_annotations = []
        type_of_error = ""
        if extra_annotations:
            (
                isExtraAnnotationValid,
                unvalid_extra_annotations,
            ) = validate_extra_annotation_condition(diffs)
            if not isExtraAnnotationValid:
                error_annotations.append(unvalid_extra_annotations)
                type_of_error = "Extra "
        if missing_annotations:
            (
                isMissingAnnotationValid,
                unvalid_missing_annotations,
            ) = validate_missing_annotation_condition(diffs)
            if not isMissingAnnotationValid:
                error_annotations.append(unvalid_missing_annotations)
                type_of_error += "Missing "
        if error_annotations:
            write_to_antx_error_log(
                modified_file_name,
                f"{type_of_error} annotations found:{error_annotations}",
            )
        else:
            write_to_antx_log(modified_file_name)
    else:
        write_to_antx_error_log(modified_file_name, "File identical to original file.")


def write_to_antx_log(filename):
    log_file_path = DATA_FOLDER_DIR / ANTX_LOG_FILE
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{filename}:\n")


def write_to_antx_error_log(filename, error_message):
    error_log_file_path = DATA_FOLDER_DIR / ANTX_ERROR_LOG_FILE
    with open(error_log_file_path, "a") as log_file:
        log_file.write(f"{filename}: {error_message} \n")


def filter_hyphen_bo(file_name: str) -> str:
    return file_name.replace("-bo", "")


def verify_antx_modification(original_folder_path: Path, modified_folder_path: Path):
    txt_files = modified_folder_path.glob("*.txt")
    file_count = count_files_in_folder(modified_folder_path)
    counter = 1
    # Empyting the log files
    empty_antx_log_files()

    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name}...")
        modified_content = txt_file.read_text(encoding="utf-8")

        original_file_name = filter_hyphen_bo(txt_file.name)
        original_file_path = original_folder_path / original_file_name
        original_content = original_file_path.read_text(encoding="utf-8")
        verify_annotation_transfer(original_content, modified_content, txt_file.name)
        counter += 1


if __name__ == "__main__":
    # verify_antx_modification(
    #     FILTERED_TM_FOLDER_DIR, FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR
    # )
    count_affix_in_files(
        FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR, FILTERED_TOKENIZED_TM_FOLDER_DIR
    )
