"""The step-by-step examples from the video work too."""

import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

EXAMPLES = Path(__file__).parent.parent / "examples"


def load(name):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return TestClient(module.app)


def test_hello():
    client = load("01_hello")
    assert client.get("/hello/Priya").json() == {"message": "Hello, Priya!"}


def test_params():
    client = load("02_params")
    assert client.get("/products/2").json()["name"] == "Mouse"
    assert client.get("/products/abc").status_code == 422
    assert client.get("/products/99").status_code == 404
    names = [p["name"] for p in client.get("/products?max_price=500&in_stock=true").json()]
    assert names == ["Mouse", "USB cable"]


def test_body():
    client = load("03_body")
    res = client.post("/courses", json={"title": "FastAPI basics", "price": 0, "tags": ["python"]})
    assert res.status_code == 201
    assert res.json()["id"] == 1
    assert client.post("/courses", json={"title": "x", "price": -1}).status_code == 422
    assert client.delete("/courses/1").status_code == 204


def test_async_dashboard_runs_concurrently():
    client = load("04_async")
    assert client.get("/dashboard").json()["total_seconds"] < 2
