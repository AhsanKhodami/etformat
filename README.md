# etformat - Eye-Tracking Data Processing

etformat is a Python package designed to simplify the extraction, conversion, and analysis of eye-tracking data from EDF files. It provides tools for exporting data, analyzing fixations and saccades, validating calibration, and visualizing gaze movements. Whether you're conducting research in psychology, neuroscience, or usability testing, etformat makes handling eye-tracking data efficient and accessible.


# Important Note before using etformat

Before using the package it is neccessary to follow this steps:
(©️ Eylink Compnay & Alexander (Sasha) Pastukhov)

Install SR Research EyeLink Developers Kit
This package relies on edfapi library that is as part of the EyeLink Developers Kit, which can be downloaded from www.sr-research.com/support website. Note that you need to register and wait for your account to be activated. Next, follow instructions to install EyeLink Developers Kit for your platform. The forum thread should be under SR Support Forum › Downloads › EyeLink Developers Kit / API › Download: EyeLink Developers Kit / API Downloads (Windows, macOS, Linux).

Please note that this package will not work without Eyelink Developers Kit!

Specify location of the edfapi library
The package looks for edfapi either in the global environment (i.e., the folder is added to the PATH) or in a typical path for the OS. The typical locations are:

- For Windows: c:/Program Files (x86)/SR Research/EyeLink/libs/x64
- For Mac OSX: /Library/Frameworks
- For Linux: edpapi library is install in /usr/lib, so is in the global path.
If you installed EyeLink Developers Kit using defaults, the typical paths should work. However, you may have used a different folder for installation (relevant primarily for Windows) or it is possible that SR Research changed the defaults. In this case, you can specify path to the library as a parameter or set EDFAPI_LIB environment variable.

For detailed usage instructions and API reference, visit the **full documentation** here:  
📖 **[etformat Documentation](https://ahsankhodami.github.io/etformat/)**  
