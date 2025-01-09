from functions import markdown_to_html_node

# DIV > P > B
def test_bold_md_to_html():
    test_case = 'This is **normal text** in a paragraph.'
    expected = "<div><p>This is <b>normal text</b> in a paragraph.</p></div>"

    assert markdown_to_html_node(test_case).to_html() == expected


# DIV > UL > LI > I
def test_italic_ulist_md_to_html():
    test_case = '* This is a list for test\n* It also has some *italic* text.'
    expected = ("<div><ul><li>This is a list for test</li>"
                "<li>It also has some <i>italic</i> text.</li></ul></div>")

    assert markdown_to_html_node(test_case).to_html() == expected


# DIV > OL > LI > CODE
def test_olist_code_md_to_html():
    test_case = '1. This is a list for test\n2. It also has `code` inside.'
    expected = ("<div><ol><li>This is a list for test</li>"
                "<li>It also has <code>code</code> inside.</li></ol></div>")

    assert markdown_to_html_node(test_case).to_html() == expected



# DIV > CODE
def test_code_md_to_html():
    test_case = '```<a href="url_de_ejemplo">Test de **codigo**</a>```'
    expected = ('<div><pre><code><a href="url_de_ejemplo">Test de **codigo**'
                "</a></code></pre></div>")

    assert markdown_to_html_node(test_case).to_html() == expected


# DIV > QUOTE > B-IMG
def test_quote_bold_img_md_to_html():
    test_case = '>Esta es una cita que incluye\n>una ![imagen](url_de_prueba)'
    expected = ('<div><blockquote>Esta es una cita que incluye\nuna <img src='
                '"url_de_prueba" alt="imagen"></img></blockquote></div>')

    assert markdown_to_html_node(test_case).to_html() == expected


# DIV > HEADING > LINK
def test_heading_link_md_to_html():
    test_case = '### Este es un titulo con [un link](url_prueba)'
    expected = ('<div><h3>Este es un titulo con <a href="url_prueba">un link'
                "</a></h3></div>")

    assert markdown_to_html_node(test_case).to_html() == expected

# DIV
def test_full_doc():
    test_case = ('## Documento\n\nEsta es una **prueba**\n\n# Ejemplo\n\n```'
                '<a href="test_url">link</a>```\n\nCierto *famoso* dijo:\n\n'
                '> Al que le quede el saco `que se lo ponga`\n\n### Razones '
                'para seguir:\n\n* Se puede\n- Se debe\n* Se quiere\n\n## Lista '
                'final:\n\n1. Cuenta al final del ejemplo\n2. Listo')

    expected = ('<div><h2>Documento</h2><p>Esta es una <b>prueba</b></p><h1>'
                'Ejemplo</h1><pre><code><a href="test_url">link</a></code></pre>'
                '<p>Cierto <i>famoso</i> dijo:</p><blockquote>Al que le quede '
                'el saco <code>que se lo ponga</code></blockquote><h3>Razones '
                'para seguir:</h3><ul><li>Se puede</li><li>Se debe</li><li>Se '
                'quiere</li></ul><h2>Lista final:</h2><ol><li>Cuenta al final '
                'del ejemplo</li><li>Listo</li></ol></div>')
    
    assert markdown_to_html_node(test_case).to_html() == expected