from op_mt_tools.tokenizers import bo_sent_tokenizer


def bo_sent_tokenizer_pipeline(bo_string):
    bo_string_sent_tokenizer = bo_sent_tokenizer(bo_string)
    return bo_string_sent_tokenizer


if __name__ == "__main__":
    bo_string = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    bo_string_segmented = bo_sent_tokenizer_pipeline(bo_string)
    print(bo_string_segmented)
    print(type(bo_string_segmented))
