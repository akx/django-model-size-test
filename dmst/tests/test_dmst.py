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
@pytest.mark.parametrize(
    "mode",
    (
        "all",
        "only",
        "defer",
        "values_all",
        "values_list_all",
        "values_1",
        "values_list_1",
    ),
)
def test_model(benchmark, model_id, mode):
    ModelX: Model = MODELS[model_id]
    n_models = 1000
    insns = make_instances(ModelX, n_models)
    ModelX.objects.bulk_create(insns)
    if mode == "defer":
        benchmark(lambda: len(ModelX.objects.all().defer("field0")) == n_models)
    elif mode == "only":
        benchmark(lambda: len(ModelX.objects.all().only("field0")) == n_models)
    elif mode == "all":
        benchmark(lambda: len(ModelX.objects.all()) == n_models)
    elif mode == "values_all":
        benchmark(lambda: len(ModelX.objects.all().values()) == n_models)
    elif mode == "values_list_all":
        benchmark(lambda: len(ModelX.objects.all().values_list()) == n_models)
    elif mode == "values_1":
        benchmark(lambda: len(ModelX.objects.all().values("field0")) == n_models)
    elif mode == "values_list_1":
        benchmark(lambda: len(ModelX.objects.all().values_list("field0")) == n_models)
    else:
        raise NotImplementedError("...")
