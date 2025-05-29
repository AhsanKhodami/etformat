# Converting EDF to CSV


## 📌 How to Use `export()`

The **`export` function** takes an EDF file as input and converts it into **CSV files**.

### ✅ Basic Usage (File in the Same Directory)
If your `.EDF` file is in the same directory as your script, simply run:

```python
import etformat as et

# Convert 'test.EDF' (must be in the same folder as your script)
et.export("test.EDF")
```
- The CSV files will be saved in the same folder as `test.EDF`.


### 📂 Specifying a File Path
If your `.EDF` file is located **in another folder**, provide the full or relative path:

```python
# Convert an EDF file located in another folder
et.export("/path/to/your/file.EDF")
```

For example:
```python
et.export("C:/Users/YourName/Documents/myfile.EDF")
```
or on macOS/Linux:
```python
et.export("~/Documents/myfile.EDF")
```

## 🎯 What Happens After Running `export()`?
- The **EDF file is processed** and converted.
- Two CSV files are **created in the same directory** as the EDF file:
  1. `filename_events.csv` → Contains **event-related data**.
  2. `filename_samples.csv` → Contains **sampled eye-tracking data**.

### Example Output:
If you run:
```python
et.export("C:/data/test.EDF")
```
You will get:
```
C:/data/test_events.csv
C:/data/test_samples.csv
```


## ⚠️ Common Errors & Solutions

### ❌ File Not Found
**Error Message:**
```
FileNotFoundError: Error: The file 'test.EDF' does not exist. Check the path and try again.
```
**Solution:**  
- Make sure the file **exists** at the specified location.
- Use an **absolute path** if needed.
- Double-check **spelling** and file **extensions**.

### ❌ Permission Error
**Solution:**
- Ensure you have **read/write access** to the folder where the file is stored.
- Try **running the script as an administrator** (Windows) or using `sudo` (Mac/Linux).