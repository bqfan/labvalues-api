# test_main.py
from fastapi.testclient import TestClient
from app.src.main import app
from app.src.utilities import reference_loader
from app.src.api.models.schemas.references import Reference
from typing import Final

from typing import Final
import json

REFERENCES: Final[dict] = reference_loader.load_references("default")
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "LabTest API"}

def test_reference():
    response = client.get("/v1/References/glucose")
    response_content_json = json.loads(response.content)
    reference_model = Reference

    assert response.status_code == 200

    validated_reference = reference_loader.validate_data(REFERENCES["Observations"]["glucose"], reference_model)
    assert isinstance(validated_reference, Reference)

    validated_response_content_json = reference_loader.validate_data(response_content_json, reference_model)
    assert isinstance(validated_response_content_json, Reference)

    assert(is_subset(REFERENCES["Observations"]["glucose"], response_content_json))

def is_subset(subset, superset):
    match subset:
        case dict(_): return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())
        case list(_) | set(_): return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)
        # assume that subset is a plain value if none of the above match
        case _: return subset == superset



