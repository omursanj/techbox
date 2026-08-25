from app.services.ai_service import normalize_currency_in_response


def test_ai_response_uses_tenge_symbol():
    result = normalize_currency_in_response(
        "Цена: 24 990 ₽, доставка 3 000 руб."
    )

    assert result == "Цена: 24 990 ₸, доставка 3 000 ₸"


def test_ai_response_keeps_tenge_unchanged():
    result = normalize_currency_in_response(
        "Цена: 24 990 ₸"
    )

    assert result == "Цена: 24 990 ₸"
