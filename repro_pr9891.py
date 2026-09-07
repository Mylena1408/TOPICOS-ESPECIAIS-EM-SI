from django.conf import settings

if not settings.configured:
    settings.configure(
        DEFAULT_CHARSET="utf-8",
    )

import django
django.setup()

from django.http import QueryDict
from rest_framework.fields import DictField


data = QueryDict("", mutable=True)

field = DictField(required=False, default={"nome": "valor"})

resultado = field.get_value(data)

print("Resultado:", resultado)
print("Tipo:", type(resultado))
print("É o default?", resultado == {"nome": "valor"})