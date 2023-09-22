import re
from pathlib import Path
from typing import List

from config import (
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
    tibetan_only_string = remove_spaces(tibetan_only_string)
    return tibetan_only_string


def remove_affixes_ignore_first(
    input_text, affix_issues: List[str] = affix_issues
) -> str:
    input_text
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


if __name__ == "__main__":
    input_text = Path(FILTERED_TOKENIZED_TM_FOLDER_DIR / "TM0791.txt").read_text(
        encoding="utf-8"
    )
    pattern_text = Path(FILTERED_TOKENIZED_BO_FOLDER_DIR / "BO0791.txt").read_text(
        encoding="utf-8"
    )

    output_text = learn_and_clean_affixes(input_text, pattern_text)
    output_file_path = Path(FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR / "TM0791.txt")
    output_file_path.write_text(output_text, encoding="utf-8")
