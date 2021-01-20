"""cogeo_mosaic_plugins debug"""

import pathlib
from typing import Dict, Optional, Tuple

import attr
import mercantile
import uvicorn
from cogeo_mosaic.backends import MosaicBackend
from cogeo_mosaic.utils import get_footprints
from fastapi import APIRouter, FastAPI, Query
from fastapi.staticfiles import StaticFiles
from geojson_pydantic.features import Feature, FeatureCollection
from rio_tiler.constants import MAX_THREADS
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from cogeo_mosaic_plugins.ressources.responses import GeoJSONResponse

template_dir = str(pathlib.Path(__file__).parent.joinpath("templates"))
static_dir = str(pathlib.Path(__file__).parent.joinpath("static"))
templates = Jinja2Templates(directory=template_dir)


def bbox_to_feature(
    bbox: Tuple[float, float, float, float], properties: Optional[Dict] = None,
) -> Feature:
    """Create a GeoJSON feature polygon from a bounding box."""
    return Feature(
        **{
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [bbox[0], bbox[3]],
                        [bbox[0], bbox[1]],
                        [bbox[2], bbox[1]],
                        [bbox[2], bbox[3]],
                        [bbox[0], bbox[3]],
                    ]
                ],
            },
            "bbox": bbox,
            "properties": {} or properties,
            "type": "Feature",
        }
    )


@attr.s
class MosaicDebug:
    """Creates a very minimal server using fastAPI + Uvicorn."""

    src_path: str = attr.ib()

    app: FastAPI = attr.ib(default=attr.Factory(FastAPI))

    token: Optional[str] = attr.ib(default=None)
    port: int = attr.ib(default=8080)
    host: str = attr.ib(default="127.0.0.1")
    style: str = attr.ib(default="basic")
    config: Dict = attr.ib(default=dict)

    router: Optional[APIRouter] = attr.ib(init=False)

    def __attrs_post_init__(self):
        """Update App."""
        self.router = APIRouter()
        self.register_routes()
        self.app.include_router(self.router)
        self.app.mount("/static", StaticFiles(directory=static_dir), name="static")

    def register_routes(self):
        """Register routes to the FastAPI app."""

        @self.router.get(r"/assets")
        def assets(qk: str = Query(...)):
            """Handle /assets requests."""
            x, y, z = mercantile.quadkey_to_tile(qk)
            with MosaicBackend(self.src_path) as mosaic:
                return mosaic.assets_for_tile(x, y, z)

        @self.router.get(
            r"/shapes.geojson",
            response_model=FeatureCollection,
            response_model_exclude_none=True,
            responses={200: {"description": "Return info about the MosaicJSON"}},
            response_class=GeoJSONResponse,
        )
        def shapes(qk: str = Query(...)):
            """return info."""
            x, y, z = mercantile.quadkey_to_tile(qk)
            with MosaicBackend(self.src_path) as mosaic:
                assets = mosaic.assets_for_tile(x, y, z)
                features = get_footprints(assets, max_threads=MAX_THREADS)
            return FeatureCollection(features=features)

        @self.router.get(
            r"/info.geojson",
            response_model=Feature,
            response_model_exclude_none=True,
            responses={200: {"description": "Return info about the MosaicJSON"}},
            response_class=GeoJSONResponse,
        )
        def info():
            """return info."""
            with MosaicBackend(self.src_path) as mosaic:
                info = mosaic.info(quadkeys=True).dict(exclude_none=True)
                bounds = info.pop("bounds", None)
                info.pop("center", None)
                return bbox_to_feature(bounds, properties=info)

        @self.router.get(
            "/",
            responses={200: {"description": "Simple COG viewer."}},
            response_class=HTMLResponse,
        )
        async def viewer(request: Request):
            """Handle /index.html."""
            return templates.TemplateResponse(
                name="index.html",
                context={
                    "request": request,
                    "info_endpoint": request.url_for("info"),
                    "assets_endpoint": request.url_for("assets"),
                    "shapes_endpoint": request.url_for("shapes"),
                    "mapbox_access_token": self.token,
                    "mapbox_style": self.style,
                },
                media_type="text/html",
            )

    @property
    def endpoint(self) -> str:
        """Get endpoint url."""
        return f"http://{self.host}:{self.port}"

    @property
    def template_url(self) -> str:
        """Get simple app template url."""
        return f"http://{self.host}:{self.port}"

    @property
    def docs_url(self) -> str:
        """Get simple app template url."""
        return f"http://{self.host}:{self.port}/docs"

    def start(self):
        """Start tile server."""
        uvicorn.run(app=self.app, host=self.host, port=self.port, log_level="info")
