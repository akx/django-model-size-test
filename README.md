```
pip install -r requirements.txt
```

```
env DJANGO_SETTINGS_MODULE=dmst.settings pytest -vvs --benchmark-save-data --benchmark-autosave --benchmark-group-by=param:mode
```
