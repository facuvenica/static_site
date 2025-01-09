from functions import markdown_to_blocks

def test_three_blocks():
    markdown = ("# This is a heading\n\nThis is a paragraph of text. It has "
                "some **bold** and *italic* words inside of it.\n\n* This is "
                "the first list item in a list block\n* This is a list item\n"
                "* This is another list item")

    result = ["# This is a heading", "This is a paragraph of text. It has some"
              " **bold** and *italic* words inside of it.","* This is the "
              "first list item in a list block\n* This is a list item\n* This "
              "is another list item"]
    
    assert markdown_to_blocks(markdown) == result


def test_extra_newlines():
    markdown = "This is a test.\n\n\n\n\n# Heading.\n\n* List 1\n* List 2"
    expected = ["This is a test.", "# Heading.", "* List 1\n* List 2"]

    assert markdown_to_blocks(markdown) == expected


def test_extra_spaces():
    markdown = " This is a test.\n\n* List 1   "
    expected = ["This is a test.", "* List 1"]

    assert markdown_to_blocks(markdown) == expected