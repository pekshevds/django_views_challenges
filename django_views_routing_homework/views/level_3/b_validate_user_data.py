"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""

import re
import json
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest


def check_that_the_length_of_full_name_is_beetwen_5_and_256(full_name):
    if isinstance(full_name, str):
        return 5 <= len(full_name) <= 256
    return False


def check_that_email_similate_email(email):
    if isinstance(email, str):
        return (
            re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", email)
            is not None
        )
    return False


def check_registered_from_contain_website_or_mobile_app(registered_from):
    if isinstance(registered_from, str):
        return True if registered_from.lower() in ["website", "mobile_app"] else False
    return False


def check_age(age):
    return isinstance(age, int)


def binary_to_dict(binary):
    return json.loads(binary.decode("utf-8"))


def handle_incoming_data(data):
    return (
        data.get("full_name"),
        data.get("email", ""),
        data.get("registered_from"),
        data.get("age"),
    )


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        data = binary_to_dict(request.body)
    except json.decoder.JSONDecodeError:
        return HttpResponseBadRequest()

    full_name, email, registered_from, age = handle_incoming_data(data)
    result = all(
        [
            full_name
            and check_that_the_length_of_full_name_is_beetwen_5_and_256(full_name),
            email and check_that_email_similate_email(email),
            registered_from
            and check_registered_from_contain_website_or_mobile_app(registered_from),
            check_age(age) if age else True,
        ]
    )
    return HttpResponse(json.dumps({"is_valid": result}))
