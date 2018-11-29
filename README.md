python_cpp_skel
===============

A python skeleton project built with [pybind11](https://github.com/pybind/pybind11) and [mason](https://github.com/mapbox/mason/).

[![Build Status](https://travis-ci.org/mapbox/python-cpp-skel.svg?branch=master)](https://travis-ci.org/mapbox/python-cpp-skel)

Installation
------------

Clone this repository then run in the directory:

```
pip install .
```

If you are doing development on this library run:

```
pip install -e .
```

Testing
-------

Testing uses [pytest](https://docs.pytest.org/en/latest/).

If you do not have it installed run:

```
pip install pytest
```

then simply run:

```
pytest
```

Example
-------

```python
import python_cpp_skel
python_cpp_skel.add(1, 2)
```
