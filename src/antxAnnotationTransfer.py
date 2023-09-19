import re

from antx import transfer

from path_definations import BO_folder_path, TM_folder_path


def antxAnnotationTransfer(source_text, target_text):
    annotations = [
        ["One", r"(1️⃣)"],
        ["Two", r"(2️⃣)"],
        ["Three", r"(3️⃣)"],
        ["new_line", r"(\n)"],
    ]
    AnnotatedText = transfer(source_text, annotations, target_text, output="txt")
    return AnnotatedText


def remove_newlines(text):
    # Use regex to remove newlines
    text_without_newlines = re.sub(r"\n", " ", text)

    return text_without_newlines


if __name__ == "__main__":
    source_text = (TM_folder_path / "TM0790.txt").read_text(encoding="utf-8")
    target_text = (BO_folder_path / "BO0790_tokenized.txt").read_text(encoding="utf-8")
    target_text = remove_newlines(target_text)
    AnnotatedText = antxAnnotationTransfer(source_text, target_text)
    with open(TM_folder_path / "TM0790_cleaned.txt", "w", encoding="utf-8") as file:
        for AnnotatedLine in AnnotatedText.splitlines():
            file.write(f"{AnnotatedLine.strip()}\n")