import re
from pathlib import Path
from typing import List

from affix_check_script import count_files_in_folder
from config import (  # DATA_FOLDER_DIR
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
)

affix_issues = ["་འི་", "་ས་", "་ར་", "་འི།", "་ས།", "་ར།"]


def remove_spaces(input_string: str) -> str:
    return input_string.replace(" ", "")


def filter_tibetan_characters(input_string: str) -> str:
    # Use a regular expression to remove non-Tibetan characters
    tibetan_only_string = re.sub(r"[^\u0F00-\u0FFF\s]", "", input_string)
    return remove_spaces(tibetan_only_string)


def remove_affixes_ignore_first(
    input_text, affix_issues: List[str] = affix_issues
) -> str:
    for issue in affix_issues:
        input_text = input_text.replace(issue, issue[1:])
    return input_text


def learn_and_clean_affixes(input_text: str, pattern_text: str) -> str:
    output_text = ""
    input_lines = input_text.splitlines()
    pattern_lines = pattern_text.splitlines()
    for input_line in input_lines:
        matching_affixes = [affix for affix in affix_issues if affix in input_line]

        if matching_affixes:
            found_match = False
            for pattern_line in pattern_lines:
                if remove_affixes_ignore_first(
                    filter_tibetan_characters(input_line)
                ) == remove_affixes_ignore_first(
                    filter_tibetan_characters(pattern_line)
                ):
                    output_text += pattern_line + "\n"
                    found_match = True
                    break
            if not found_match:
                output_text += input_line + "\n"
        else:
            output_text += input_line + "\n"
    return output_text


def clean_affix_and_save_in_folder(
    input_folder_path: Path, pattern_folder_path: Path, output_folder_path: Path
):
    txt_files = input_folder_path.glob("*.txt")
    file_count = count_files_in_folder(input_folder_path)
    counter = 1
    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name}...")
        file_content = txt_file.read_text(encoding="utf-8")
        pattern_file_name = txt_file.name.replace("TM", "BO")
        patter_file_path = pattern_folder_path / pattern_file_name
        pattern_content = patter_file_path.read_text(encoding="utf-8")
        cleaned_content = learn_and_clean_affixes(file_content, pattern_content)
        output_file_path = Path(output_folder_path) / txt_file.name
        output_file_path.write_text(cleaned_content)
        counter += 1


if __name__ == "__main__":
    clean_affix_and_save_in_folder(
        FILTERED_TOKENIZED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_BO_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    )
