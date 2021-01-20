"""cogeo_mosaic_plugins CLI."""

import os

import click

from cogeo_mosaic_plugins.debug import MosaicDebug


class MbxTokenType(click.ParamType):
    """Mapbox token type."""

    name = "token"

    def convert(self, value, param, ctx):
        """Validate token."""
        try:
            if not value:
                return ""

            assert value.startswith("pk")
            return value

        except (AttributeError, AssertionError):
            raise click.ClickException(
                "Mapbox access token must be public (pk). "
                "Please sign up at https://www.mapbox.com/signup/ to get a public token. "
                "If you already have an account, you can retreive your "
                "token at https://www.mapbox.com/account/."
            )


@click.command()
@click.argument("src_path", type=str, nargs=1, required=True)
@click.option(
    "--style",
    type=click.Choice(["dark", "satellite", "basic"]),
    default="dark",
    help="Mapbox basemap",
)
@click.option("--port", type=int, default=8080, help="Webserver port (default: 8080)")
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Webserver host url (default: 127.0.0.1)",
)
@click.option(
    "--mapbox-token",
    type=MbxTokenType(),
    metavar="TOKEN",
    default=lambda: os.environ.get("MAPBOX_ACCESS_TOKEN", ""),
    help="Pass Mapbox token",
)
def debug(src_path, style, port, host, mapbox_token):
    """WEB UI to visualize Mosaic Quadkeys."""
    application = MosaicDebug(
        src_path=src_path, token=mapbox_token, port=port, host=host, style=style,
    )

    click.echo(f"Viewer started at {application.template_url}", err=True)
    click.launch(application.template_url)

    application.start()
