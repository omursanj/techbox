import re


def normalize_phone(phone: str) -> str:
    """
    Нормализует телефон для хранения в базе.

    Примеры:
    +7 (701) 123-45-67 -> +77011234567
    8 701 123 45 67    -> +77011234567
    77011234567        -> +77011234567
    """

    phone = phone.strip()

    if not phone:
        raise ValueError("Телефон не указан.")

    # Оставляем только цифры и ведущий +
    cleaned = re.sub(
        r"[^\d+]",
        "",
        phone,
    )

    # + разрешён только в начале
    if "+" in cleaned[1:]:
        raise ValueError(
            "Некорректный формат телефона."
        )

    digits = re.sub(
        r"\D",
        "",
        cleaned,
    )

    # Казахстан / совместимый формат через 8
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]

    # Уже начинается с 7
    if len(digits) == 11 and digits.startswith("7"):
        return f"+{digits}"

    # Если пользователь передал международный номер
    # другой страны, сохраняем его с +
    if 7 <= len(digits) <= 15:
        return f"+{digits}"

    raise ValueError(
        "Некорректная длина номера телефона."
    )


def is_valid_phone(phone: str) -> bool:
    """
    Проверяет, можно ли нормализовать телефон.
    """

    try:
        normalize_phone(phone)
        return True
    except ValueError:
        return False


def mask_phone(phone: str) -> str:
    """
    Маскирует телефон для логов или интерфейса.

    +77011234567 -> +7701***4567
    """

    normalized = normalize_phone(phone)

    if len(normalized) <= 8:
        return normalized

    return (
        normalized[:5]
        + "***"
        + normalized[-4:]
    )