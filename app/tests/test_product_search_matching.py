from app.repositories.product_repository import _product_matches_query
from app.repositories.product_repository import _get_search_terms


PRODUCT = {
    "name": "Anker 323 Charger",
    "brand": "Anker",
    "description": "Компактное зарядное устройство.",
    "category": "charger",
    "specifications": {
        "Мощность": "33W",
    },
}


def test_search_matches_partial_model_name():
    search_terms = _get_search_terms("Anker 323")

    assert _product_matches_query(PRODUCT, search_terms) is True


def test_search_matches_words_in_any_order():
    search_terms = _get_search_terms("charger anker")

    assert _product_matches_query(PRODUCT, search_terms) is True


def test_search_matches_model_with_separator():
    search_terms = _get_search_terms("323-Charger")

    assert _product_matches_query(PRODUCT, search_terms) is True


def test_search_rejects_unrelated_model():
    search_terms = _get_search_terms("Anker 511")

    assert _product_matches_query(PRODUCT, search_terms) is False
