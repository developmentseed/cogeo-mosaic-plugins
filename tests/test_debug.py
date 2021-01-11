"""Tests for tilebench."""

import os

from geojson_pydantic.features import Feature
from starlette.testclient import TestClient

from cogeo_mosaic_plugins.debug import MosaicDebug

mosaic = os.path.join(os.path.dirname(__file__), "fixtures", "mosaic.json.gz")


def test_debug():
    """Should work as expected (create app object)."""
    app = MosaicDebug(src_path=mosaic)
    assert app.port == 8080
    assert app.endpoint == "http://127.0.0.1:8080"
    assert app.template_url == "http://127.0.0.1:8080"

    client = TestClient(app.app)

    response = client.get("/info.geojson")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/geo+json"
    info = Feature(**response.json())
    print(info)
    assert info.properties["quadkeys"]
    assert info.bbox

    qk = info.properties["quadkeys"][0]
    response = client.get(f"/assets?qk={qk}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert isinstance(body, list)
