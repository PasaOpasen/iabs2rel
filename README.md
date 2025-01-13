[![PyPI version](https://badge.fury.io/py/iabs2rel.svg)](https://pypi.org/project/iabs2rel/)
[![Downloads](https://pepy.tech/badge/iabs2rel)](https://pepy.tech/project/iabs2rel)
[![Downloads](https://pepy.tech/badge/iabs2rel/month)](https://pepy.tech/project/iabs2rel)
[![Downloads](https://pepy.tech/badge/iabs2rel/week)](https://pepy.tech/project/iabs2rel)

# iabs2rel

```
pip install iabs2rel
```

A Python utility / library to convert absolute Python imports to relative

## About

This package is purposed for conversion python code imports from absolute to relative. It is very useful in case of nested packages there it is preferable to use `..parent.file` imports instead of `root.package1.package2.package3.parent.file`.

## Advantages

- many parameters to control imports depth and code zones
- high performance
- detailed logging
- CLI allowed

## Limitations

- only `from ... import ...`  imports are allowed; other imports will be not converted to relative
- to use this package u need Python3.8 environment at least, but updating (target) code may be written in older Python
- u often need to specify proper `--python-path` paths to resolve absolute imports 

## CLI

### `iabs2rel`

```
usage: iabs2rel [-h] [--dry-run] [--python-path PYTHON_PATH [PYTHON_PATH ...]] [--allowed-paths ALLOWED_PATHS [ALLOWED_PATHS ...]] [--denied-paths DENIED_PATHS [DENIED_PATHS ...]]
                [--loglevel {NO,ERROR,WARNING,INFO,DEBUG}] [--max-depth MAX_DEPTH]
                sources [sources ...]

Replaces absolute file imports to relative in all sources

positional arguments:
  sources               paths to python files or directories with python files

optional arguments:
  -h, --help            show this help message and exit
  --dry-run, -n         Whether to run without performing file processing operations (default: False)
  --python-path PYTHON_PATH [PYTHON_PATH ...], -p PYTHON_PATH [PYTHON_PATH ...]
                        PYTHONPATH elements to resolve absolute imports; if nothing set then only CWD will be used; absolute imports that cannot be resolved will not be converted to relative (default: )
  --allowed-paths ALLOWED_PATHS [ALLOWED_PATHS ...], -a ALLOWED_PATHS [ALLOWED_PATHS ...]
                        allowed import destination files/folder; if nothing set then any destination is allowed; if absolute import points not to allowed location it will not be converted to relative (default: )
  --denied-paths DENIED_PATHS [DENIED_PATHS ...], -e DENIED_PATHS [DENIED_PATHS ...]
                        forbidden import destination files/folder; if absolute import points to forbidden location (even allowed) it will not be converted to relative (default: )
  --loglevel {NO,ERROR,WARNING,INFO,DEBUG}, -l {NO,ERROR,WARNING,INFO,DEBUG}
                        using loglevel (default: DEBUG)
  --max-depth MAX_DEPTH, -d MAX_DEPTH
                        max relative import depth; 0 means only local imports to same package are allowed (start with 1 dot);1 means 0 + imports 1 level upper (start with 2 dots); higher values are available; values <0
                        disable any limits (default: 1)
```

## `iabs2rel-file`

```
usage: iabs2rel-file [-h] [--destination DESTINATION] [--python-path PYTHON_PATH [PYTHON_PATH ...]] [--allowed-paths ALLOWED_PATHS [ALLOWED_PATHS ...]] [--denied-paths DENIED_PATHS [DENIED_PATHS ...]]
                     [--loglevel {NO,ERROR,WARNING,INFO,DEBUG}] [--max-depth MAX_DEPTH]
                     source

Replaces absolute file imports to relative

positional arguments:
  source                python file path to replace imports

optional arguments:
  -h, --help            show this help message and exit
  --destination DESTINATION, -o DESTINATION
                        destination file; empty means to print to stdout (default: None)
  --python-path PYTHON_PATH [PYTHON_PATH ...], -p PYTHON_PATH [PYTHON_PATH ...]
                        PYTHONPATH elements to resolve absolute imports; if nothing set then only CWD will be used; absolute imports that cannot be resolved will not be converted to relative (default: )
  --allowed-paths ALLOWED_PATHS [ALLOWED_PATHS ...], -a ALLOWED_PATHS [ALLOWED_PATHS ...]
                        allowed import destination files/folder; if nothing set then any destination is allowed; if absolute import points not to allowed location it will not be converted to relative (default: )
  --denied-paths DENIED_PATHS [DENIED_PATHS ...], -e DENIED_PATHS [DENIED_PATHS ...]
                        forbidden import destination files/folder; if absolute import points to forbidden location (even allowed) it will not be converted to relative (default: )
  --loglevel {NO,ERROR,WARNING,INFO,DEBUG}, -l {NO,ERROR,WARNING,INFO,DEBUG}
                        using loglevel (default: DEBUG)
  --max-depth MAX_DEPTH, -d MAX_DEPTH
                        max relative import depth; 0 means only local imports to same package are allowed (start with 1 dot);1 means 0 + imports 1 level upper (start with 2 dots); higher values are available; values <0
                        disable any limits (default: 1)
```