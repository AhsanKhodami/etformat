"""
Welcome to etformat!
Use it and feel free.
"""

# Dynamically retrieve version from setuptools-scm
try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = "dev"  # Fallback for development mode

# Importing necessary modules to make them accessible when using `import etformat`
from .calibration import *
from .channels import *
from .describe import *
from .edfdata import *
from .edfdata_containers import *
from .edffile import *
from .edfinfo import *
from .export import export  # Ensure export is accessible
from .plot_gaze import *
from .plot_saccades import *
