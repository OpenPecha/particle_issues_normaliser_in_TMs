import re

from antx import transfer

from config import BO_FOLDER_DIR, TM_FOLDER_DIR


def antx_annotation_transfer(source_text, target_text):
    annotations = [
        ["One", r"(1️⃣)"],
        ["Two", r"(2️⃣)"],
        ["Three", r"(3️⃣)"],
        ["new_line", r"(\n)"],
    ]
    annotated_text = transfer(source_text, annotations, target_text, output="txt")
    return annotated_text


def remove_newlines(text):
    # Use regex to remove newlines
    text_without_newlines = re.sub(r"\n", " ", text)

    return text_without_newlines


if __name__ == "__main__":
    source_text = (TM_FOLDER_DIR / "TM0790.txt").read_text(encoding="utf-8")
    target_text = (BO_FOLDER_DIR / "BO0790_tokenized.txt").read_text(encoding="utf-8")
    target_text = remove_newlines(target_text)
    annotated_text = antx_annotation_transfer(source_text, target_text)
    with open(TM_FOLDER_DIR / "TM0790_cleaned.txt", "w", encoding="utf-8") as file:
        for annotated_line in annotated_text.splitlines():
            file.write(f"{annotated_line.strip()}\n")
