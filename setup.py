from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy as np
import sys

C_COMPILE = True
USE_CYTHON = True

__version__ = "0.0.0"
exec(open('velocyto/_version.py').read())
print(sys.argv)

if C_COMPILE:
    package_data: dict = {}
    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = [Extension("velocyto.speedboosted",
                                ["velocyto/speedboosted.pyx"],
                                extra_compile_args=['-fopenmp'],
                                extra_link_args=['-fopenmp'])]
        extensions = cythonize(extensions, include_path=[np.get_include()])
    else:
        extensions = [Extension("velocyto.speedboosted",
                                ["velocyto/speedboosted.c"],
                                extra_compile_args=['-fopenmp'],
                                extra_link_args=['-fopenmp'])]
else:
    extensions = []
    if "darwin" in sys.platform:
        compiled = "velocyto/speedboosted.cpython-36m-darwin.so"
    elif "win" in sys.platform:
        sys.stdout.write("Sorry man, we do not support (or like) Windows OS")
        sys.exit()
    elif "linux" in sys.platform:
        compiled = "velocyto/speedboosted.cpython-36m-x86_64-linux-gnu.so"
    package_data = {'velocyto': [compiled]}

setup(
    name="velocyto",
    version=__version__,
    packages=find_packages(),
    install_requires=['numpy',
                      'scipy',
                      'numba',
                      'scikit-learn',
                      'h5py',
                      'loompy',
                      'pysam',
                      'Click'],
    # command
    entry_points='''
        [console_scripts]
        velocyto=velocyto.commands.velocyto:cli
    ''',
    ext_modules=extensions,
    include_dirs=[np.get_include()],
    package_data=package_data,
    # metadata
    author="Linnarsson Lab",
    author_email="sten.linnarsson@ki.se",
    description="RNA velocity analysis for single cell RNA-seq data",
    license="BSD2",
    url="https://github.com/linnarsson-lab/velocyto",
)
