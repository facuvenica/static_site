from functions import extract_markdown_element
from textnode import TextType


def test_extract_images():
    test_case = ("Este es un texto con ![texto inicial](url_de_una_imagen) "
                 "como ejemplo, y esta otra es una ![imagen real 123456!]"
                 "(https://i.imgur.com/fJRm4Vk.jpeg)")
    url_result = [("texto inicial", "url_de_una_imagen"),
                ("imagen real 123456!", "https://i.imgur.com/fJRm4Vk.jpeg")]

    text_result = ["Este es un texto con "," como ejemplo, y esta otra es una "]
    elements, text = extract_markdown_element(test_case, TextType.IMAGE)
    
    assert elements == url_result and text == text_result


def test_extract_links():
    test_case = ("Este es un texto con [texto inicial](url_de_una_pagina) "
                 "como ejemplo, y esta otra es una [pagina real 12$·@56!]"
                 "(https://google.com)")

    url_result = [("texto inicial", "url_de_una_pagina"),
                ("pagina real 12$·@56!", "https://google.com")]

    text_result = ["Este es un texto con "," como ejemplo, y esta otra es una "]
    elements, text = extract_markdown_element(test_case, TextType.LINK)
    
    assert elements == url_result and text == text_result


def test_both():
    test_case = ("Este es un texto con ![texto](url_de_una_imagen) como prueba"
                 ", y esta otra es [localhost!](https://localhost)")

    expected_a = ([("texto","url_de_una_imagen")],
                  ["Este es un texto con "," como prueba, y esta otra es "
                   "[localhost!](https://localhost)"])

    expected_b = ([("localhost!","https://localhost")],
                  ["Este es un texto con !", " como prueba, y esta otra es "])

    assert extract_markdown_element(test_case, TextType.IMAGE) == expected_a
    assert extract_markdown_element(test_case, TextType.LINK) == expected_b