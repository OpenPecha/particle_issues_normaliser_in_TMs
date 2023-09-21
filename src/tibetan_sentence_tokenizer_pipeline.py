from op_mt_tools.tokenizers import bo_sent_tokenizer as sentence_tokenizer


def sentence_tokenizer_pipeline(text: str) -> str:
    text_tokenized = sentence_tokenizer(text)
    return text_tokenized


if __name__ == "__main__":
    bo_string = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    bo_string_tokenized = sentence_tokenizer_pipeline(bo_string)
    print(bo_string_tokenized)
    print(type(bo_string_tokenized))
