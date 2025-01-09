import pytest

from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import markdown_to_html_node

# Main class HTMLNode

def test_valid_nodes():
    test_cases = [
        HTMLNode('a', 'Google',props={'href':'http://google.com'}),
        HTMLNode('p', 'This is a paragraph', 'a'),
        HTMLNode('div', children='a'),
        HTMLNode(value='This is a test')]

    expected = [
    "Tag: a, Value: Google, Children: None, Props: {'href': 'http://google.com'}",
    "Tag: p, Value: This is a paragraph, Children: a, Props: None",
    "Tag: div, Value: None, Children: a, Props: None",
    "Tag: None, Value: This is a test, Children: None, Props: None"]
    
    for zip_case in zip(test_cases, expected):
        assert zip_case[0].__repr__() == zip_case[1]


def test_props_to_html():
    a = HTMLNode('a', 'Search in Web',props={'href':'http://google.com'})
    img = HTMLNode('img', 'Kitten', props={'src': 'http://image.url','alt':'kitten'})

    assert a.props_to_html() == ' href="http://google.com"'
    assert img.props_to_html() == ' src="http://image.url" alt="kitten"'


def test_repr():
    node = HTMLNode('a','URL',props={'href':'link'})
    s = node.__repr__()

    assert s == "Tag: a, Value: URL, Children: None, Props: {'href': 'link'}"


# Subclass LeafNode

def test_no_value():
    with pytest.raises(ValueError, match='Value was not defined') as e:
        p = LeafNode('p', None)
        p.to_html()


def test_single_leaf():
    leaf_p = LeafNode('p','Este es un parrafo')

    assert leaf_p.to_html() == "<p>Este es un parrafo</p>"


def test_prop_leaves():
    test_cases = [LeafNode('a', 'Web Search', {'href':'http://www.google.com'}),
                  LeafNode('img', 'Kitten',{'src':'./image.png','alt':'kitten'}),
                  LeafNode(None, 'simple text', {'test':'test'})]

    expected = ['<a href="http://www.google.com">Web Search</a>',
                '<img src="./image.png" alt="kitten">Kitten</img>',
                'simple text']

    for zip_case in zip(test_cases, expected):
        assert zip_case[0].to_html() == zip_case[1]


# Subclass ParentNode

def test_childless():
    with pytest.raises(ValueError, match='ParentNode requires children') as e:
        p = ParentNode('p', None)
        p.to_html()


def test_tagless():
    with pytest.raises(ValueError, match='Missing HTML tag') as e:
        p = ParentNode(None, None)
        p.to_html()


def test_grandparent():
    grandpa = ParentNode('div',
                        [ParentNode(
                            'p',[
                            LeafNode(None, 'This is'),
                            LeafNode('b','normal text'),
                            LeafNode(None, 'in a paragraph.'),
                            ]
                        ),
                        LeafNode(None, 'Fin.'),]
                    )
    
    expected = "<div><p>This is<b>normal text</b>in a paragraph.</p>Fin.</div>"

    assert grandpa.to_html() == expected