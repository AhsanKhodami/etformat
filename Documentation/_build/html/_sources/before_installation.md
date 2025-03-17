# Before Installation

## Prerequisites

To effectively use **etformat**, you need to install:

### SR Research EyeLink Developers Kit

1. This package depends on the `edfapi` library, which is included in the EyeLink Developers Kit
2. Download the kit from [SR Research Support](https://www.sr-research.com/support)
3. Requirements for download:
   - Create an account on SR Research website
   - Wait for account activation
   - Navigate to: SR Support Forum › Downloads › EyeLink Developers Kit / API › Download: EyeLink Developers Kit / API Downloads (Windows, macOS, Linux)
4. Follow the platform-specific installation instructions provided with the kit

> **Important:** The **etformat** package will not function without the EyeLink Developers Kit installed.

### EDFAPI Library Location

The package searches for the `edfapi` library in the following locations:

#### Default Installation Paths
- **Windows**: `C:/Program Files (x86)/SR Research/EyeLink/libs/x64`
- **macOS**: `/Library/Frameworks`
- **Linux**: `/usr/lib` (globally accessible)

#### Custom Installation
If you installed the EyeLink Developers Kit in a non-default location, you have two options to specify the `edfapi` library path:

1. Set the `EDFAPI_LIB` environment variable
2. Provide the path as a parameter when using the package

> **Note:** If you used the default installation settings, no additional configuration should be necessary.

