import pytest
from django.db.models import Model

from dmst.models import MODELS


def make_instances(Model, count):
    fields = [f.name for f in Model._meta.fields if f.name != "id"]
    insns = []
    for i in range(count):
        kwargs = {f: f"{f}{i}" for f in fields}
        ins = Model(**kwargs)
        insns.append(ins)
    return insns


@pytest.mark.django_db
@pytest.mark.parametrize("model_id", sorted(MODELS))
def test_model(benchmark, model_id):
    ModelX: Model = MODELS[model_id]
    n_models = 1000
    insns = make_instances(ModelX, n_models)
    ModelX.objects.bulk_create(insns)
    benchmark(lambda: len(ModelX.objects.all()) == n_models)
