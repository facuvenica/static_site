from functions import get_block_type

TEST_CASES = {
    'code': [
        "```Esto es codigo valido```",
        "```Esto no lo es``",
        "`Ni esto tampoco``",
    ],
    'quotes':[
        ">Esta es una cita valida\n>con dos lineas",
        ">Esta es una cita invalida\nmala linea",
        ">Esta viene con >lineas>duplicadas pero es una cita",
        "> Esta es otra cita valida\n> con espacios",
    ],
    'ulists':[ # Lista desordenada
        "* Lista desordenada con\n- una mezcla de signos",
        "*Mala lista porque falta el espacio",
        "* Buena lista con\n* los mismos simbolos",
        "* Lista a la que le * falta el salto de linea",
        "* Mala lista porque \n*No tiene espacio",
    ],
    'olists': [ # Lista ordenada
        "1. Buena lista\n2. En secuencia\n3. Si",
        "1. Mala lista\n3. No secuencia",
        "1.Mala lista, falta espacio",
        "2. Mala lista, no empieza en 1",
    ],
    'headings':[
        "# Buena cabecera",
        "###### Buena cabecera",
        "#Mala cabecera#",
        "######Mala cabecera",
    ]
}


def test_get_headings():
    expected_results = [
        "Heading",
        "Heading",
        "Paragraph",
        "Paragraph",
    ]

    for case, result in zip(TEST_CASES['headings'], expected_results):
        assert get_block_type(case) == result


def test_get_quotes():
    expected_results = [
        "Quote",
        "Paragraph",
        "Quote",
        "Quote",
    ]

    for case, result in zip(TEST_CASES['quotes'], expected_results):
        assert get_block_type(case) == result


def test_get_code():
    expected_results = [
        "Code",
        "Paragraph",
        "Paragraph",
    ]

    for case, result in zip(TEST_CASES['code'], expected_results):
        assert get_block_type(case) == result


def test_get_ordered_lists():
    expected_results = [
        "Olist",
        "Paragraph",
        "Paragraph",
        "Paragraph",
    ]

    for case, result in zip(TEST_CASES['olists'], expected_results):
        assert get_block_type(case) == result


def test_get_unordered_lists():
    expected_results = [
        "Ulist",
        "Paragraph",
        "Ulist",
        "Ulist",
        "Paragraph",
    ]

    for case, result in zip(TEST_CASES['ulists'], expected_results):
        assert get_block_type(case) == result