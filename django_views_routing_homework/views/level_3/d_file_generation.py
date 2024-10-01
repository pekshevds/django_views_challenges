"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

import csv
import random
import string
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods


def get_random_string(length):
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])


@require_http_methods(["GET"])
def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    length = int(request.GET.get("length", "0"))
    if length < 1 or length > 128:
        return HttpResponseForbidden()
    random_string = get_random_string(length)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow([random_string])
    return response
