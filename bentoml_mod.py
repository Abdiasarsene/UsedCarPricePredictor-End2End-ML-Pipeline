import bentoml
from datetime import datetime

for model in bentoml.models.list():
    # You can inspect model creation time via metadata or file timestamps
    model_path = model._model_store_path  # internal path
    created = datetime.fromtimestamp(model_path.stat().st_ctime)
    if created.month == 8 and created.year == 2025:
        print(f"{model.tag} - Created: {created}")