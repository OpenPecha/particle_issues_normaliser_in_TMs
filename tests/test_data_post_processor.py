from affix_normaliser.data_post_processor import adjust_tsek_position_with_whitespaces


def test_adjust_tsek_position_with_whitespaces():
    test_sentence = "བོད་ཀྱི་མཁས་པ་ཁ་ཅིག ་སྟོན་པ།"
    output_sentence = adjust_tsek_position_with_whitespaces(test_sentence)
    expected_sentence = "བོད་ཀྱི་མཁས་པ་ཁ་ཅིག་ སྟོན་པ།"
    assert output_sentence == expected_sentence
