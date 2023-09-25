import re
from pathlib import Path

from antx import transfer

from .affix_check_script import count_files_in_folder
from .config import (
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
    target_text = remove_newlines_tabs_spaces(target_text)
    annotated_text = transfer(source_text, annotations, target_text, output="txt")
    return annotated_text


def annotation_transfer_and_save_in_folder(
    source_folder_path: Path, target_folder_path, output_folder_path
):
    txt_files = source_folder_path.glob("*.txt")
    file_count = count_files_in_folder(source_folder_path)
    counter = 1

    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name}...")
        source_content = txt_file.read_text(encoding="utf-8")
        target_file_path = target_folder_path / txt_file.name
        target_content = target_file_path.read_text(encoding="utf-8")
        annotated_content = antx_annotation_transfer(source_content, target_content)
        output_file_path = Path(output_folder_path) / txt_file.name
        output_file_path.write_text(annotated_content, encoding="utf-8")
        counter += 1


def remove_newlines_tabs_spaces(text):
    # Use regex to remove newlines
    text = re.sub(r"[\n\t\s]+", "", text)
    return text


if __name__ == "__main__":
    annotation_transfer_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR,
        FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
        FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
    )
