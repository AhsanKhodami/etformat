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

## CSV column names

### Sample File

| Column | Description | Note |
|--------|-------------|------|
| **trial** | Trial index | Added, not from EDF file |
| **time** | Timestamp of the sample (in milliseconds) | |
| **time_rel** | Time relative to recording start | Added |
| **pxL/pxR** | Left/Right eye pupil X position | |
| **pyL/pyR** | Left/Right eye pupil Y position | |
| **hxL/hxR** | Left/Right eye head-ref X coordinate | |
| **hyL/hyR** | Left/Right eye head-ref Y coordinate | |
| **paL/paR** | Left/Right eye pupil size or area | |
| **gxL/gxR** | Left/Right eye gaze X coordinate (screen) | |
| **gyL/gyR** | Left/Right eye gaze Y coordinate (screen) | |
| **rx** | Pixels per degree on X axis | |
| **ry** | Pixels per degree on Y axis | |
| **gxvelL/gxvelR** | Left/Right eye gaze X velocity | |
| **gyvelL/gyvelR** | Left/Right eye gaze Y velocity | |
| **hxvelL/hxvelR** | Left/Right eye head-ref X velocity | |
| **hyvelL/hyvelR** | Left/Right eye head-ref Y velocity | |
| **rxvelL/rxvelR** | Left/Right eye raw X velocity | |
| **ryvelL/ryvelR** | Left/Right eye raw Y velocity | |
| **fgxvelL/fgxvelR** | Left/Right eye fast gaze X velocity | |
| **fgyvelL/fgyvelR** | Left/Right eye fast gaze Y velocity | |
| **fhxvelL/fhxvelR** | Left/Right eye fast head-ref X velocity | |
| **fhyvelL/fhyvelR** | Left/Right eye fast head-ref Y velocity | |
| **frxvelL/frxvelR** | Left/Right eye fast raw X velocity | |
| **fryvelL/fryvelR** | Left/Right eye fast raw Y velocity | |
| **hdata0-hdata7** | Head-tracker data channels | 8 values |
| **flags** | Flags indicating what data is present | |
| **input** | Extra input value | |
| **buttons** | Button states and changes | |
| **htype** | Head-tracker type (0 = none) | |
| **errors** | Processing error flags | |

### Events File

| Column | Description | Note |
|--------|-------------|------|
| **trial** | Trial index | Added |
| **time** | Time of the event | |
| **type** | Type of event (e.g. blink, saccade) | |
| **read** | Flags for which data is present | |
| **sttime** | Start time of the event | |
| **sttime_rel** | Start time relative to recording start | Added |
| **entime** | End time of the event | |
| **entime_rel** | End time relative to recording start | Added |
| **duration** | Event duration | Computed |
| **hstx** | Head-ref X at start | |
| **hsty** | Head-ref Y at start | |
| **gstx** | Gaze X at start | |
| **gsty** | Gaze Y at start | |
| **sta** | Pupil size at start | |
| **henx** | Head-ref X at end | |
| **heny** | Head-ref Y at end | |
| **genx** | Gaze X at end | |
| **geny** | Gaze Y at end | |
| **ena** | Pupil size at end | |
| **havx** | Average head-ref X | |
| **havy** | Average head-ref Y | |
| **gavx** | Average gaze X | |
| **gavy** | Average gaze Y | |
| **ava** | Average pupil size | |
| **avel** | Average velocity | |
| **pvel** | Peak velocity | |
| **svel** | Start velocity | |
| **evel** | End velocity | |
| **supd_x** | Start units-per-degree (X axis) | |
| **eupd_x** | End units-per-degree (X axis) | |
| **supd_y** | Start units-per-degree (Y axis) | |
| **eupd_y** | End units-per-degree (Y axis) | |
| **eye** | Eye used | 0 = left, 1 = right |
| **status** | Event status flags | |
| **flags** | Additional flags | |
| **input** | Input state | |
| **buttons** | Button states | |
| **parsedby** | Who parsed this event | |
| **message** | Message string (if any) | |

### Recording Data

| Column | Description | Values |
|--------|-------------|--------|
| **time** | Time of recording start or end | |
| **sample_rate** | Sampling rate | Hz |
| **eflags** | Event-related flags | |
| **sflags** | Sample-related flags | |
| **state** | Recording state | 0 = END, 1 = START |
| **record_type** | What was recorded | 1 = samples, 2 = events, 3 = both |
| **pupil_type** | Pupil measurement | 0 = area, 1 = diameter |
| **recording_mode** | Recording mode | 0 = pupil only, 1 = corneal reflection |
| **filter_type** | Filter applied | 1, 2, or 3 |
| **pos_type** | Position type | 0 = gaze, 1 = HREF, 2 = raw |
| **eye** | Eye recorded | 1 = left, 2 = right, 3 = both |

For detailed usage instructions and API reference, visit the **full documentation** here:  
📖 **[etformat Documentation](https://khodami.info/etformat/)**
