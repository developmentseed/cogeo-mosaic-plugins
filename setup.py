"""Setup tilebench."""

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = [
    "fastapi",
    "uvicorn",
    "jinja2",
    "aiofiles",
    "geojson_pydantic",
    "cogeo-mosaic>=3.0.0b1,<3.1",
]
extra_reqs = {
    "test": ["pytest", "pytest-cov", "pytest-asyncio"],
    "dev": ["pytest", "pytest-cov", "pytest-asyncio", "pre-commit"],
}


setup(
    name="cogeo_mosaic_plugins",
    version="0.1.0",
    description=u"",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    keywords="",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/developmentseed/cogeo-mosaic-plugins",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points="""
      [cogeo_mosaic.plugins]
      debug=cogeo_mosaic_plugins.scripts.cli:debug
    """,
)
