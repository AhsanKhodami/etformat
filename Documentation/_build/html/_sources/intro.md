### 📌 Introduction to etformat

**etformat** is a Python package designed for **processing and analyzing eye-tracking data** from **EDF (Eye Data Format) files**. It provides tools to **convert, extract, visualize, and analyze** gaze data with ease.

### **🔹 Key Features**
✔ **Convert EDF to CSV** for easy access (`export()`)  
✔ **Extract metadata** like sampling rate & screen size (`edfinfo()`)  
✔ **Analyze trials** for fixations, saccades & blinks (`describe()`)  
✔ **Visualize gaze paths** (`plot_gaze()`)  
✔ **Plot saccades** with movement directions (`plot_saccades()`)  
✔ **Extract and validate calibration data** (`calibration()`)

### **🚀 Quick Example**
```python
import etformat as et

# Convert EDF file to CSV
et.export("test.EDF")

# Extract EDF metadata
et.edfinfo("test.EDF")

# Analyze trials
et.describe("test.EDF")

# Plot gaze for trial 3
et.plot_gaze(samples, trial_number=3)

# Plot saccades for trial 3
et.plot_saccades(events, trial_number=3)

# Extract calibration details
et.calibration("test.EDF")
```

✅ **Easy to use, powerful, and built for eye-tracking research!** 🚀

```{tableofcontents}
```
