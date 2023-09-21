from pathlib import Path
from typing import List

from config import (
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
)

affix_issues = ["་འི", "་ས", "་ར"]


def remove_affixes_ignore_first(
    input_text, affix_issues: List[str] = affix_issues
) -> str:
    output_text = input_text
    for issue in affix_issues:
        output_text = output_text.replace(issue, issue[1:])
    return output_text


def learn_and_clean_affixes(input_text: str, pattern_text: str) -> str:
    output_text = ""
    input_lines = input_text.splitlines()
    pattern_lines = pattern_text.splitlines()
    for input_line in input_lines:
        matching_affixes = [affix for affix in affix_issues if affix in input_line]

        if matching_affixes:
            for pattern_line in pattern_lines:
                pattern_line_cleaned = remove_affixes_ignore_first(pattern_line)
                input_line_cleaned = remove_affixes_ignore_first(input_line)
                if pattern_line_cleaned == input_line_cleaned:
                    output_text += pattern_line + "\n"
                    break
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
