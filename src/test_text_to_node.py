from textnode import TextNode, TextType
from functions import text_to_textnodes

def test_text_to_node():
    test_case = ("Esto es **texto** con una _palabra_ en cursiva y un `poco de"
                 " codigo` seguido de una ![imagen de obi wan](https://i.imgur"
                 ".com/fJRm4Vk.jpeg) y un [enlace](https://boot.dev)")

    expected = [
        TextNode("Esto es ", TextType.TEXT),
        TextNode("texto", TextType.BOLD),
        TextNode(" con una ", TextType.TEXT),
        TextNode("palabra", TextType.ITALIC),
        TextNode(" en cursiva y un ", TextType.TEXT),
        TextNode("poco de codigo", TextType.CODE),
        TextNode(" seguido de una ", TextType.TEXT),
        TextNode("imagen de obi wan", TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" y un ", TextType.TEXT),
        TextNode("enlace", TextType.LINK, "https://boot.dev")
    ]

    assert text_to_textnodes(test_case) == expected