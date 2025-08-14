import os
import random
import shutil

# --- Configuration ---
# 1. SET THE PATH to your folder containing all the images and .txt files.
SOURCE_DIR = r"C:\Users\VAIBHAV ADMANE\Downloads\agri_data\data" 

# 2. SET THE PATH to your target dataset directory.
DEST_DIR = r"E:\Crop-Weed-Detection\yolo-agri-vision\data\sesame_dataset"

# 3. SET THE SPLIT RATIO for your data.
TRAIN_RATIO = 0.7  # 70% for training
VAL_RATIO = 0.2    # 20% for validation
# The rest (10%) will be for testing.

# --- Main Script Logic ---

def organize_files():
    """
    Reads files from the source directory, shuffles them, and moves them
    into train, validation, and test sets according to the defined ratios.
    """
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory not found at '{SOURCE_DIR}'")
        return

    # Create destination directories if they don't exist
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(DEST_DIR, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(DEST_DIR, 'labels', split), exist_ok=True)

    # Get a list of all image files (assuming .jpg, add other extensions if needed)
    image_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(image_files) # Shuffle for random distribution

    # Calculate split indices
    total_files = len(image_files)
    train_split_index = int(total_files * TRAIN_RATIO)
    val_split_index = int(total_files * (TRAIN_RATIO + VAL_RATIO))

    # Split the file list
    train_files = image_files[:train_split_index]
    val_files = image_files[train_split_index:val_split_index]
    test_files = image_files[val_split_index:]

    # Function to move a file and its corresponding label
    def move_file_pair(file_list, split_name):
        for img_file in file_list:
            # Construct the label filename
            base_name = os.path.splitext(img_file)[0]
            label_file = f"{base_name}.txt"

            # Source paths
            src_img_path = os.path.join(SOURCE_DIR, img_file)
            src_label_path = os.path.join(SOURCE_DIR, label_file)

            # Destination paths
            dest_img_path = os.path.join(DEST_DIR, 'images', split_name, img_file)
            dest_label_path = os.path.join(DEST_DIR, 'labels', split_name, label_file)
            
            # Move the files
            if os.path.exists(src_label_path):
                shutil.move(src_img_path, dest_img_path)
                shutil.move(src_label_path, dest_label_path)
                print(f"Moved {img_file} and {label_file} to {split_name} set.")
            else:
                print(f"Warning: Label file not found for {img_file}. Skipping.")

    # Move files to their respective directories
    print("--- Starting Training Set Move ---")
    move_file_pair(train_files, 'train')
    print("\n--- Starting Validation Set Move ---")
    move_file_pair(val_files, 'val')
    print("\n--- Starting Test Set Move ---")
    move_file_pair(test_files, 'test')
    
    print("\nDataset organization complete!")

if __name__ == "__main__":
    organize_files()