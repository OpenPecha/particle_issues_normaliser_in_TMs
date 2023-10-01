import re
from pathlib import Path
from typing import List

from antx.core import get_diffs

from .config import (  # DATA_FOLDER_DIR
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
)
from .file_utils import (
    count_files_in_folder,
    file_name_without_txt,
    remove_version_number_from_file_name,
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


def filter_common_characters(input_text: str, pattern_text: str) -> str:
    common_characters = [
        diff[1]
        for diff in get_diffs(input_text, pattern_text)
        if diff[0] == 0 or diff[0] == -1 and diff[1] in ["་", "༌"]
    ]
    return "".join(common_characters)


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
                    filtered_pattern_line = filter_common_characters(
                        input_line, pattern_text
                    )
                    output_text += filtered_pattern_line + "\n"
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
        tm_file_name = file_name_without_txt(txt_file.name)
        pattern_file_name = f"BO{tm_file_name[2:]}"
        pattern_file_name = remove_version_number_from_file_name(pattern_file_name)
        pattern_file_name = f"{pattern_file_name}.txt"

        pattern_file_path = pattern_folder_path / pattern_file_name

        output_file_path = Path(output_folder_path) / txt_file.name
        if pattern_file_path.exists():
            pattern_content = pattern_file_path.read_text(encoding="utf-8")
            cleaned_content = learn_and_clean_affixes(file_content, pattern_content)
            output_file_path.write_text(cleaned_content)
        else:
            output_file_path.write_text(file_content)
        counter += 1


if __name__ == "__main__":
    clean_affix_and_save_in_folder(
        FILTERED_TOKENIZED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_BO_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    )
