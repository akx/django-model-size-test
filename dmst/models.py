from django.db.models import Model, CharField
from django.db.models.base import ModelBase

MODELS = {}

for x in range(0, 256, 16):
    x = max(1, x)
    fields = [(f"field{f}", CharField(max_length=100)) for f in range(x)]
    name = f"Model{x:03d}"
    model = ModelBase(
        name,
        (Model,),
        dict(
            fields,
            __module__=__name__,
        ),
    )
    globals()[name] = model
    MODELS[name] = model
