import re

from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode

def split_nodes_delimiter(nodos, delimitador, type_text):
    retval = []
    for nodo in nodos:
        if nodo.text_type == TextType.TEXT:
            if nodo.text.count(delimitador) % 2 != 0:
                raise Exception(f'Sintaxis Markdown invalida: {nodo.text}')
            else:
                texto = nodo.text.split(delimitador)

                for split in texto:
                    indice = texto.index(split)
                    tipo = TextType.TEXT if indice % 2 == 0 else type_text
                    retval.append(TextNode(split,tipo))
        else:
            retval.append(nodo)

    return retval


def split_nodes_element(nodos, text_type):
    retval = []
    for nodo in nodos:
        if not nodo.text:
            continue

        if nodo.text_type == TextType.TEXT:
            datos, texto = extract_markdown_element(nodo.text, text_type)

            for alt, url in datos:
                retval.append(TextNode(texto.pop(0),TextType.TEXT))
                retval.append(TextNode(alt,text_type, url))
            
            if texto:
                retval.append(TextNode(texto[0], TextType.TEXT))
 
        else:
            retval.append(nodo)

    return retval


def extract_markdown_element(texto, text_type):
    elements = text = None

    match text_type:
        case TextType.IMAGE:
            elements = re.findall(r"!\[(.*?)\]\((.*?)\)", texto)
            text = re.split(r"!\[.*?\]\(.*?\)", texto)

        case TextType.LINK:
            elements = re.findall(r"\s\[(.*?)\]\((.*?)\)", texto)
            text = re.split(r"\[.*?\]\(.*?\)", texto)

    if not text[-1]:
        text.pop()

    return elements, text


def text_to_textnodes(texto):
    nodo = TextNode(texto,TextType.TEXT)

    nodos = split_nodes_delimiter([nodo], '**', TextType.BOLD)
    nodos = split_nodes_delimiter(nodos, '_', TextType.ITALIC)
    nodos = split_nodes_delimiter(nodos, '`', TextType.CODE)
    nodos = split_nodes_element(nodos,TextType.IMAGE)
    nodos = split_nodes_element(nodos,TextType.LINK)

    return nodos


def text_to_quote(texto):
    if texto[0] != '>':
        raise Exception('No es una cita markdown')

    bloque = re.sub(r'\n>\s|\n>', '\n', texto.lstrip('>').strip())
    children = text_to_textnodes(bloque)
    return ParentNode('blockquote', children)


def text_to_list_node(texto, tipo):
    if not re.search(r'\d\.\s|\*\s|\-\s', texto[:3]):
        raise Exception('No es una lista markdown')

    tag = 'ul' if tipo == 'Ulist' else 'ol'

    children, lista = [], texto.splitlines()

    for item in lista:
        content = item[2:] if tag == 'ul' else item[3:]
        children.append(ParentNode('li', text_to_textnodes(content)))

    return ParentNode(tag, children)


def markdown_to_title(documento):
    return re.findall(r'#\s(.*?)\n', documento)[0]


def markdown_to_blocks(documento):
    lines = documento.split('\n\n')
    retval = []

    for block in lines:
        if block:
            retval.append(block.strip())

    return retval


def get_block_type(bloque):
    match bloque[0]:
        case '#': # Bloque de cabecera
            for char in bloque[1:7]:
                if char != '#':
                    break

            if char == ' ': return 'Heading'

        case '`': # Bloque de código:
            if bloque[:3] == '```' and bloque[-3:] == "```":
                return 'Code'

        case '>': # Bloque de Cita
            saltos = re.findall(r'\n.', bloque)
            citas = re.findall(r'\n>', bloque[1:])

            if saltos and citas != saltos:
                return 'Paragraph'

            return 'Quote'
        case _:
            pass

    # Lista desordenada
    if bloque[:2] in ('* ', '- '):
        items = re.findall(r'\n\*\s', bloque)
        items.extend(re.findall(r'\n\-\s', bloque))

        if len(re.findall(r'\n', bloque)) == len(items):
            return 'Ulist'

    # Lista Ordenada
    if bloque[:3] == '1. ':
        items = re.findall(r'\n\d\.\s', bloque[1:])
        saltos = re.findall(r'\n', bloque)

        if len(saltos) == len(items):
            is_list = True
            for num in range(len(items)):
                if str(num + 2) not in items[num]:
                    is_list = False
                    break

            if is_list:
                return 'Olist'

    return 'Paragraph'


def markdown_to_html_node(markdown):
    bloques = markdown_to_blocks(markdown)
    html_children = []

    for bloque in bloques:
        match get_block_type(bloque):
            case 'Heading':
                header = bloque.count('#',0,6)
                children = text_to_textnodes(re.sub(r'#+\s','',bloque,1))
                nodo = ParentNode(f'h{header}', children)
            case 'Code':
                bloque = bloque.strip('```')
                code = ParentNode('code', [TextNode(bloque, TextType.TEXT)])
                nodo = ParentNode('pre', [code])
            case 'Quote':
                nodo = text_to_quote(bloque)
            case 'Ulist':
                nodo = text_to_list_node(bloque, 'Ulist')
            case 'Olist':
                nodo = text_to_list_node(bloque, 'Olist')
            case _:
                children = text_to_textnodes(bloque)
                nodo = ParentNode('p', children)

        html_children.append(nodo)

    return ParentNode('div', html_children)