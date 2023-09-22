import re

from antx import transfer

from config import (
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
)


def antx_annotation_transfer(source_text, target_text):
    annotations = [
        ["One", r"(1️⃣)"],
        ["Two", r"(2️⃣)"],
        ["Three", r"(3️⃣)"],
        ["tab", r"(\t)"],
        ["new_line", r"(\n)"],
        ["space_line", r"(\s+)"],
    ]
    annotated_text = transfer(source_text, annotations, target_text, output="txt")
    return annotated_text


def remove_newlines_tabs_spaces(text):
    # Use regex to remove newlines
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\t", "", text)
    text = re.sub(r"\s+", "", text)
    return text


if __name__ == "__main__":
    file_name = "TM0001.txt"
    source_text = (FILTERED_TM_FOLDER_DIR / file_name).read_text(encoding="utf-8")
    target_text = (FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR / file_name).read_text(
        encoding="utf-8"
    )
    target_text = remove_newlines_tabs_spaces(target_text)
    annotated_text = antx_annotation_transfer(source_text, target_text)
    output_file_path = FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR / file_name
    output_file_path.write_text(annotated_text, encoding="utf-8")
