"""
Welcome to etformat!
Use it and feel free.
"""

# Dynamically retrieve version from setuptools-scm
try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = "dev"  # Fallback for development mode

# Print a message when the package is imported
print(f"📖 etformat {__version__} - For Documentation, visit: https://ahsankhodami.github.io/etformat/intro.html")

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
from .clean import clean  # Add data cleaning functionality
from .saccade_analysis import saccade_amplitude_average  # Add saccade amplitude analysis
from .report import report  # Add trial report generation
