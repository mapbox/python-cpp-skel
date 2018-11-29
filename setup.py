from setuptools import setup, Extension
from build_scripts import Mason, get_pybind_include, BuildExt

__version__ = '0.0.1'

mason = Mason()
mason.use("boost", "1.66.0", header_only=True)

includes = [
    get_pybind_include(),
    get_pybind_include(user=True)
]
includes.extend(mason.includes("boost"))

ext_modules = [
    Extension(
        'python_cpp_skel',
        ['src/main.cpp'],
        include_dirs=includes,
        extra_compile_args=['-std=libc++'],
        language='c++'
    ),
]

setup(
    name='python_cpp_skel',
    version=__version__,
    author='Blake Thompson',
    author_email='blake@mapbox.com',
    url='https://github.com/mapbox/python-cpp-skel',
    description='A skeleton library example using pybind11',
    long_description='',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.2'],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
)
