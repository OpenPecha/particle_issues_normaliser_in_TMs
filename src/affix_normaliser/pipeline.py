import csv
import os
import shutil
from pathlib import Path
from typing import List

from antx.core import get_diffs

from .affix_checker import identify_files_with_affix_issues
from .affix_cleaner import clean_affix_and_save_in_folder, learn_and_clean_affixes
from .antx_annotation_transfer import (
    annotation_transfer_and_save_in_folder,
    antx_annotation_transfer,
)
from .config import (
    AFFIX_ISSUES,
    ALL_TM_FOLDER_DIR,
    DATA_FOLDER_DIR,
    FILTERED_BO_FOLDER_DIR,
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
    TEST_DIR,
)
from .file_utils import convert_tm_file_name_to_bo_file_name
from .repo_file_downloader import (
    download_bo_files_from_github_with_TM_file_names,
    download_tm_files_from_github,
)
from .settings import GITHUB_TOKEN
from .tibetan_sentence_tokenizer_pipeline import (
    remove_key_caps,
    sentence_tokenize_and_save_in_folder,
    sentence_tokenizer_pipeline,
    transfer_non_tibetan_chars,
)
from .verify_antx_modification import (
    count_affix_in_string,
    validate_extra_annotation_condition,
    validate_missing_annotation_condition,
)

token = GITHUB_TOKEN


def pipeline():

    # Downloading the TM files
    tm_files = (
        Path(DATA_FOLDER_DIR / "all_TMs_list.txt")
        .read_text(encoding="utf-8")
        .split("\n")
    )
    tm_files = [element for element in tm_files if element != ""]
    download_tm_files_from_github(tm_files, ALL_TM_FOLDER_DIR)
    # files with issues
    files_with_issues, files_without_issues = identify_files_with_affix_issues(
        ALL_TM_FOLDER_DIR, AFFIX_ISSUES
    )
    Path(DATA_FOLDER_DIR / "TM_files_with_issues.txt").write_text(
        "\n".join(files_with_issues), encoding="utf-8"
    )
    Path(DATA_FOLDER_DIR / "TM_files_without_issues.txt").write_text(
        "\n".join(files_without_issues), encoding="utf-8"
    )

    # Downloading the BO files where TM had problems
    download_bo_files_from_github_with_TM_file_names(
        files_with_issues, FILTERED_BO_FOLDER_DIR
    )

    # Copying the TM files with issues to filtered_TM_folder
    files_with_issues_txt = [file_name + ".txt" for file_name in files_with_issues]
    # Specify the source and destination directories
    source_directory = ALL_TM_FOLDER_DIR
    destination_directory = FILTERED_TM_FOLDER_DIR

    # List of file names you want to copy
    files_to_copy = files_with_issues_txt

    # Loop through the list of file names and copy each file
    for file_name in files_to_copy:
        source_path = os.path.join(source_directory, file_name)
        destination_path = os.path.join(destination_directory, file_name)

        try:
            shutil.copy2(source_path, destination_path)
            print(f"Copied {file_name} to {destination_directory}")
        except FileNotFoundError:
            print(f"File {file_name} not found in {source_directory}")
        except Exception as e:
            print(f"Error copying {file_name}: {str(e)}")

    # Tokenizing the TM and BO files
    # Only TM files with issues and their corresponding BO files are tokenized
    sentence_tokenize_and_save_in_folder(
        FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR
    )
    sentence_tokenize_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR, FILTERED_TOKENIZED_TM_FOLDER_DIR
    )

    # Cleaning the TM files

    clean_affix_and_save_in_folder(
        FILTERED_TOKENIZED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_BO_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    )

    # Annotating the TM files
    annotation_transfer_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
        FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
    )


def test_tokenize_individual_file(tm_file_name: str):

    tm_file_path = Path(FILTERED_TM_FOLDER_DIR / tm_file_name)
    # Copy the file
    shutil.copy(tm_file_path, TEST_DIR)

    tm_text = tm_file_path.read_text(encoding="utf-8")
    tm_text = remove_key_caps(tm_text)
    tokenized_tm_text = sentence_tokenizer_pipeline(tm_text)
    tokenized_tm_text = transfer_non_tibetan_chars(tm_text, tokenized_tm_text)
    Path(TEST_DIR / f"t_{tm_file_name}").write_text(tokenized_tm_text, encoding="utf-8")

    bo_file_name = convert_tm_file_name_to_bo_file_name(tm_file_name)

    bo_file_path = Path(FILTERED_BO_FOLDER_DIR / bo_file_name)
    # Copy the file
    shutil.copy(bo_file_path, TEST_DIR)

    bo_text = bo_file_path.read_text(encoding="utf-8")
    bo_text = remove_key_caps(bo_text)
    tokenized_bo_text = sentence_tokenizer_pipeline(bo_text)
    tokenized_bo_text = transfer_non_tibetan_chars(bo_text, tokenized_bo_text)
    Path(TEST_DIR / f"t_{bo_file_name}").write_text(tokenized_bo_text, encoding="utf-8")


def test_clean_affixes_individual_file(tm_file_name: str):
    tm_text = Path(TEST_DIR / f"t_{tm_file_name}").read_text(encoding="utf-8")
    bo_file_name = convert_tm_file_name_to_bo_file_name(tm_file_name)
    bo_text = Path(TEST_DIR / f"t_{bo_file_name}").read_text(encoding="utf-8")
    cleaned_tm_text = learn_and_clean_affixes(tm_text, bo_text)
    Path(TEST_DIR / f"c_{tm_file_name}").write_text(cleaned_tm_text, encoding="utf-8")


def test_annotate_individual_file(tm_file_name: str):
    source_text = Path(FILTERED_TM_FOLDER_DIR / tm_file_name).read_text(
        encoding="utf-8"
    )
    target_text = Path(TEST_DIR / f"c_{tm_file_name}").read_text(encoding="utf-8")
    annotated_text = antx_annotation_transfer(source_text, target_text)
    Path(TEST_DIR / f"a_{tm_file_name}").write_text(annotated_text, encoding="utf-8")


def test_individual_file(file_name: str):
    # test_tokenize_individual_file(file_name)
    # test_clean_affixes_individual_file(file_name)
    # test_annotate_individual_file(file_name)
    annotated_file_content = Path(TEST_DIR / f"a_{file_name}").read_text(
        encoding="utf-8"
    )
    original_file_content = Path(TEST_DIR / file_name).read_text(encoding="utf-8")
    differences = list(get_diffs(original_file_content, annotated_file_content))

    (
        has_valid_missing_annotations,
        invalid_missing_annotations,
    ) = validate_missing_annotation_condition(differences)
    (
        has_valid_extra_annotations,
        invalid_extra_annotations,
    ) = validate_extra_annotation_condition(differences)

    if not has_valid_missing_annotations:
        print(invalid_missing_annotations)
    if not has_valid_extra_annotations:
        print(invalid_extra_annotations)

    affix_counts = count_affix_in_string(annotated_file_content)
    print(affix_counts)

    initial_affix_counts = count_affix_in_string(original_file_content)
    print(initial_affix_counts)

    affix_counts_values: List = []
    affix_counts_values.extend(
        [f"{key}: ", f"{value1:<6}", f"{value2:<6}"]
        for key, value1, value2 in zip(
            affix_counts.keys(),
            affix_counts.values(),
            initial_affix_counts.values(),
        )
    )
    data = [f"{file_name}"] + affix_counts_values
    # Write the data to a CSV file
    output_file = Path(TEST_DIR / "affix_counts.tsv")
    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerows(data)


if __name__ == "__main__":
    pipeline()
