import re
from pathlib import Path

from antx import transfer


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
    text_without_newlines = re.sub(r"\n", "", text)

    return text_without_newlines


if __name__ == "__main__":
    source_text = Path("./TM0790.txt").read_text(encoding="utf-8")
    target_text = Path("./BO0790_segmented.txt").read_text(encoding="utf-8")
    target_text = remove_newlines(target_text)
    AnnotatedText = antxAnnotationTransfer(source_text, target_text)
    counter = 0
    with open("./new_TM0790.txt", "w", encoding="utf-8") as file:
        file.write(AnnotatedText)

    print(counter)
