# 🌾 YOLO-Agri: Automated Crop & Weed Identification

**AgriBot Vision**  
A YOLOv8-based system for real-time crop and weed detection to enable precision agriculture and selective herbicide spraying.

---

## 🐍 Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run a Python file
python filename.py
```

---

## 🧹 Script Descriptions

### ✅ clean_data.py
Deletes files that do not have corresponding pairs (image <-> label).  
- Removes image files without matching `.txt` label files.
- Removes label files without matching image files.

### 🗂️ organize_dataset.py
Organizes and splits the dataset into:
- `train/`
- `val/`
- `test/`

### 🔎 verify_counts.py
Checks that the number of image files matches the number of label files in all three folders:
- `train/`
- `val/`
- `test/`
