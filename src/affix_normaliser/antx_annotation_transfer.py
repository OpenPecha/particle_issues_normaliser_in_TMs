import re
from pathlib import Path

from antx import transfer

from .config import (
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_CLEANED_TM_FOLDER_DIR,
    FINAL_CLEANED_ANNOTATED_TM_FOLDER_DIR,
)
from .file_utils import count_files_in_folder


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


def non_tibetan_chars_annotation_transfer(source_text, target_text):
    annotations = [
        ["tab", r"(\t)"],
        ["new_line", r"(\n)"],
        ["space_line", r"(\s+)"],
        ["non_tibetan_chars", r"([A-Za-z0-9.,;:(){}\[\]'\"`^1️⃣2️⃣3️⃣]+)"],
    ]

    source_text = source_text.replace("1️⃣", "").replace("2️⃣", "").replace("3️⃣", "")
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
        output_file_name = add_bo_to_filename(txt_file.name)
        output_file_path = Path(output_folder_path) / output_file_name
        output_file_path.write_text(annotated_content, encoding="utf-8")
        counter += 1


def add_bo_to_filename(file_name):
    base_name, extension = file_name.split(".")

    # remove version name if exists
    if "-v" in base_name:
        base_name = base_name.split("-v")[0]
    # Add "-bo" to the base name
    new_base_name = base_name + "-bo"
    new_file_name = f"{new_base_name}.{extension}"

    return new_file_name


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
