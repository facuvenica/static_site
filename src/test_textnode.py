from textnode import TextNode, TextType
import pytest

TEST_CASES = [
    TextNode("Este es un TextNode en Negrita", TextType.BOLD),
    TextNode("Este tiene cursiva", TextType.ITALIC),
    TextNode('<a href="test_url">link</a>', TextType.CODE),
    TextNode("Kitten", TextType.IMAGE, 'url_to_image'),
    TextNode("Este es un enlace", TextType.LINK, 'url_to_test'),
    TextNode("Este es un TextNode Invalido", 'invalido'),
]


def test_eq():
    for one, two in zip(TEST_CASES, TEST_CASES):
        assert one == two


def test_non_eq():
    for one, two in zip(TEST_CASES, TEST_CASES[::-1]):
        assert one != two


def test_repr_():
    node = TextNode(None, TextType.ITALIC)
    
    assert node.__repr__() == 'TextNode(None, italic, None)'


def test_node_to_html():
    expected = [
        "<b>Este es un TextNode en Negrita</b>",
        "<i>Este tiene cursiva</i>",
        '<code><a href="test_url">link</a></code>',
        '<img src="url_to_image" alt="Kitten"></img>',
        '<a href="url_to_test">Este es un enlace</a>',
        "Wrong text type"
    ]

    with pytest.raises(Exception, match='Wrong text type'):
        for case, result in zip(TEST_CASES, expected):
            assert case.to_html() == result