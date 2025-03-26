from django.core.exceptions import ValidationError


def validate_parus_url(parus_url):
    """Валидатор для проверки ссылки на Парус"""
    if not parus_url.startswith("https://pyrus.sovcombank.ru/"):
        raise ValidationError("Ссылка должна начинаться с https://pyrus.sovcombank.ru/")
