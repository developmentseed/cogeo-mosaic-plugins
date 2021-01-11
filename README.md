# cogeo-mosaic-plugins

[![CI](https://github.com/developmentseed/cogeo-mosaic-plugins/workflows/CI/badge.svg)](https://github.com/developmentseed/cogeo-mosaic-plugins/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/developmentseed/cogeo-mosaic-plugins/branch/master/graph/badge.svg)](https://codecov.io/gh/developmentseed/cogeo-mosaic-plugins)
[![Packaging status](https://badge.fury.io/py/cogeo-mosaic-plugins.svg)](https://badge.fury.io/py/cogeo-mosaic-plugins)

## Install (python >=3)
```bash
$ pip install pip -U
$ pip install cogeo-mosaic-plugins

# Or from source

$ pip install git+http://github.com/developmentseed/cogeo-mosaic-plugins
```

## Plugins

### Debug

```
$ cogeo-mosaic debug --help
Usage: cogeo-mosaic debug [OPTIONS] SRC_PATH

  WEB UI to visualize Mosaic Quadkeys.

Options:
  --style [satellite|basic]  Mapbox basemap
  --port INTEGER             Webserver port (default: 8080)
  --host TEXT                Webserver host url (default: 127.0.0.1)
  --mapbox-token TOKEN       Pass Mapbox token
  --help                     Show this message and exit.
```

```
$ cogeo-mosaic debug mymosaic.json.gz
```

![](https://user-images.githubusercontent.com/10407788/104215238-80a89180-5406-11eb-9425-1584108c9736.png)


## Contribution & Development

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/developmentseed/cogeo-mosaic-plugins.git
$ cd cogeo-mosaic-plugins
$ pip install -e .[dev]
```

**Python >=3.7 only**

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```
$ pre-commit install

$ git add .

$ git commit -m'my change'
isort....................................................................Passed
black....................................................................Passed
Flake8...................................................................Passed
Verifying PEP257 Compliance..............................................Passed
mypy.....................................................................Passed

$ git push origin
```
