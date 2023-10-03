import re


def adjust_tsek_position_with_whitespaces(text: str) -> str:
    # བོད་ཀྱི་མཁས་པ་ཁ་ཅིག ་སྟོན་པ། -> བོད་ཀྱི་མཁས་པ་ཁ་ཅིག་ སྟོན་པ།
    """
    བོད་ཀྱི་མཁས་པ་ཁ་ཅིག
    ་སྟོན་པ།
    ->
    བོད་ཀྱི་མཁས་པ་ཁ་ཅིག་
    སྟོན་པ།
    """

    pattern = r"([^།༎༏༐༔༴༻༽༾࿚])([\s\n]+)་"
    replacement = r"\1་\2"
    return re.sub(pattern, replacement, text)


if __name__ == "__main__":
    test_sentence = "བོད་ཀྱི་མཁས་པ་ཁ་ཅིག ་སྟོན་པ།"
    print(adjust_tsek_position_with_whitespaces(test_sentence))
