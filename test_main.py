from main import Parser


def test_negative_exponent_is_supported():
    parser = Parser()
    assert parser.evaluer("2**-3") == 0.125


def test_right_associative_exponentiation_stays_correct():
    parser = Parser()
    assert parser.evaluer("2**3**2") == 512


def test_unary_minus_keeps_pe_md_as_expected():
    parser = Parser()
    assert parser.evaluer("-2**2") == -4
