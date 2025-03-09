import pytest

from functions import split_nodes_delimiter, split_nodes_element
from textnode import TextNode, TextType

TEST_CASES = [
    TextNode("Este es un **TextNode** con negrita", TextType.TEXT),
    TextNode("Este tiene _cursiva_ tambien", TextType.TEXT),
    TextNode("Este es un enlace", TextType.LINK, 'url_to_test'),
    TextNode('Este tiene `<a href="test_url">link</a>` como ejemplo de codigo', TextType.TEXT),
    TextNode("Kitten", TextType.IMAGE, 'url_to_image'),
    TextNode("Este es un TextNode Invalido", 'invalido'),
]

# Split Text

def test_invalid_bold():
    test = [
        TextNode("Este no termina de definir la **negrita", TextType.TEXT),
        TextNode("Este **define** pero no **termina", TextType.TEXT),
        TextNode("Este **intenta** y **progresa** pero no **", TextType.TEXT),
    ]

    for each in test:
        with pytest.raises(Exception, match='Sintaxis Markdown invalida'):
            split_nodes_delimiter([each],'**', TextType.BOLD)


def test_invalid_italic():
    test = [
        TextNode("Este no termina de definir la _cursiva", TextType.TEXT),
        TextNode("Este _define_ pero inicia _una lista", TextType.TEXT),
        TextNode("Este _intenta_ y **progresa** pero no _", TextType.TEXT),
    ]

    for each in test:
        with pytest.raises(Exception, match='Sintaxis Markdown invalida'):
            split_nodes_delimiter([each],'_', TextType.ITALIC)


def test_invalid_code():
    test = [
        TextNode("Este no termina de definir el `codigo", TextType.TEXT),
        TextNode("Este `define` pero no `termina", TextType.TEXT),
        TextNode("Este `intenta` y `progresa` pero no `", TextType.TEXT),
    ]

    for each in test:
        with pytest.raises(Exception, match='Sintaxis Markdown invalida'):
            split_nodes_delimiter([each],'`', TextType.CODE)



def test_bold():
    expected = [
        TextNode("Este es un ", TextType.TEXT),
        TextNode("TextNode", TextType.BOLD),
        TextNode(" con negrita", TextType.TEXT),
    ]

    expected.extend(TEST_CASES[1:])

    assert split_nodes_delimiter(TEST_CASES, '**', TextType.BOLD) == expected


def test_italic():
    res = [
        TextNode("Este tiene ", TextType.TEXT),
        TextNode("cursiva", TextType.ITALIC),
        TextNode(" tambien", TextType.TEXT),
    ]

    assert split_nodes_delimiter([TEST_CASES[1]], '_', TextType.ITALIC) == res

def test_code():
    res = [
        TextNode("Este tiene ", TextType.TEXT),
        TextNode('<a href="test_url">link</a>', TextType.CODE),
        TextNode(" como ejemplo de codigo", TextType.TEXT),
    ]

    assert split_nodes_delimiter([TEST_CASES[3]], '`', TextType.CODE) == res


def test_all():
    expected = [
    TextNode("Este es un ", TextType.TEXT),
    TextNode("TextNode", TextType.BOLD),
    TextNode(" con negrita", TextType.TEXT),
    TextNode("Este tiene ",TextType.TEXT),
    TextNode("cursiva", TextType.ITALIC),
    TextNode(" tambien", TextType.TEXT),
    TextNode("Este es un enlace", TextType.LINK, 'url_to_test'),
    TextNode("Este tiene ", TextType.TEXT),
    TextNode('<a href="test_url">link</a>',TextType.CODE),
    TextNode(" como ejemplo de codigo", TextType.TEXT),
    TextNode("Kitten", TextType.IMAGE, 'url_to_image'),
    TextNode("Este es un TextNode Invalido", 'invalido'),
    ]

    retval = split_nodes_delimiter(TEST_CASES,'**',TextType.BOLD)
    retval = split_nodes_delimiter(retval,'`',TextType.CODE)
    retval = split_nodes_delimiter(retval,'_',TextType.ITALIC)

    assert retval == expected


# Split Images

def test_split_image():
    test_case = [TextNode("Este texto contiene imagenes ![de un gato](url_gato)"
                         " y ![un perro](https://i.imgur.com/XgbZdeA.jpeg)"
                         , TextType.TEXT)]

    result = [
        TextNode("Este texto contiene imagenes ", TextType.TEXT),
        TextNode("de un gato", TextType.IMAGE, "url_gato"),
        TextNode(" y ", TextType.TEXT),
        TextNode("un perro", TextType.IMAGE, "https://i.imgur.com/XgbZdeA.jpeg")
    ]

    assert split_nodes_element(test_case, TextType.IMAGE) == result


# # Split Links

def test_split_link():
    test_case = [TextNode("Usa el buscador [google](http://www.google.com) o"
                         " prueba en [wikipedia](https://www.wikipedia.com) si"
                         " ya sabes que buscar.", TextType.TEXT)]

    result = [
        TextNode("Usa el buscador ", TextType.TEXT),
        TextNode("google", TextType.LINK, "http://www.google.com"),
        TextNode(" o prueba en ", TextType.TEXT),
        TextNode("wikipedia", TextType.LINK, "https://www.wikipedia.com"),
        TextNode(" si ya sabes que buscar.", TextType.TEXT),
    ]

    assert split_nodes_element(test_case, TextType.LINK) == result
