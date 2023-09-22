import re
from pathlib import Path

from op_mt_tools.tokenizers import bo_sent_tokenizer as sentence_tokenizer

from affix_check_script import count_files_in_folder
from config import (
    FILTERED_BO_FOLDER_DIR,
    FILTERED_TM_FOLDER_DIR,
    FILTERED_TOKENIZED_BO_FOLDER_DIR,
    FILTERED_TOKENIZED_TM_FOLDER_DIR,
)


def remove_key_caps(input_string: str) -> str:
    key_caps_to_remove = ["1️⃣", "2️⃣", "3️⃣"]
    for key_cap in key_caps_to_remove:
        input_string = re.sub(key_cap, "", input_string)
    return input_string


def sentence_tokenizer_pipeline(text: str) -> str:
    text_tokenized = sentence_tokenizer(text)
    return text_tokenized


def sentence_tokenize_and_save_in_folder(folder_path: Path, output_folder_path: Path):
    txt_files = folder_path.glob("*.txt")
    file_count = count_files_in_folder(folder_path)
    counter = 1
    for txt_file in txt_files:
        print(f"[{counter}/{file_count}]] File {txt_file.name}...")
        file_content = txt_file.read_text(encoding="utf-8")
        file_content = remove_key_caps(file_content)
        tokenized_content = sentence_tokenizer_pipeline(file_content)
        output_file_path = Path(output_folder_path) / txt_file.name
        output_file_path.write_text(tokenized_content)
        counter += 1


if __name__ == "__main__":
    sentence_tokenize_and_save_in_folder(
        FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR
    )
    sentence_tokenize_and_save_in_folder(
        FILTERED_TM_FOLDER_DIR, FILTERED_TOKENIZED_TM_FOLDER_DIR
    )
