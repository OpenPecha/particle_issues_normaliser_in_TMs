from pathlib import Path

from op_mt_tools.tokenizers import bo_sent_tokenizer as sentence_tokenizer

from config import FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR


def sentence_tokenizer_pipeline(text: str) -> str:
    text_tokenized = sentence_tokenizer(text)
    return text_tokenized


def sentence_tokenize_and_save_in_folder(folder_path: Path, output_folder_path: Path):
    txt_files = folder_path.glob("*.txt")
    counter = 0
    for txt_file in txt_files:
        file_content = txt_file.read_text(encoding="utf-8")
        tokenized_content = sentence_tokenizer_pipeline(file_content)
        output_file_path = Path(output_folder_path) / txt_file.name
        output_file_path.write_text(tokenized_content)
        if counter == 3:
            break
        counter += 1


if __name__ == "__main__":
    # bo_string = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    # bo_string_tokenized = sentence_tokenizer_pipeline(bo_string)
    # print(bo_string_tokenized)
    sentence_tokenize_and_save_in_folder(
        FILTERED_BO_FOLDER_DIR, FILTERED_TOKENIZED_BO_FOLDER_DIR
    )
