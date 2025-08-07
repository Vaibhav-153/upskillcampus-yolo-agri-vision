import os

# --- CONFIGURATION ---
# This path should point to your main dataset folder.
# It assumes you are running the script from the root of your project directory.
DATASET_BASE_DIR = r"E:\Crop-Weed-Detection\yolo-agri-vision\data\sesame_dataset"

# --- MAIN SCRIPT ---

def verify_file_counts():
    """
    Counts files in train, validation, and test sets for both images
    and labels, then prints a verification report.
    """
    if not os.path.isdir(DATASET_BASE_DIR):
        print(f"Error: Dataset directory not found at '{DATASET_BASE_DIR}'")
        print("Please make sure you are in your main project folder and the path is correct.")
        return

    print(f"--- Verifying Dataset at '{DATASET_BASE_DIR}' ---\n")
    
    counts = {}
    total_files = 0

    # Loop through each data split (train, val, test)
    for split in ['train', 'val', 'test']:
        print(f"--- Checking: {split} set ---")
        
        image_dir = os.path.join(DATASET_BASE_DIR, 'images', split)
        label_dir = os.path.join(DATASET_BASE_DIR, 'labels', split)
        
        # Count images
        try:
            num_images = len(os.listdir(image_dir))
            counts[f'{split}_images'] = num_images
            print(f"Found {num_images} files in images/{split}")
        except FileNotFoundError:
            num_images = 0
            counts[f'{split}_images'] = 0
            print(f"Directory not found: images/{split}")
            
        # Count labels
        try:
            num_labels = len(os.listdir(label_dir))
            counts[f'{split}_labels'] = num_labels
            print(f"Found {num_labels} files in labels/{split}")
        except FileNotFoundError:
            num_labels = 0
            counts[f'{split}_labels'] = 0
            print(f"Directory not found: labels/{split}")

        # Verify if counts match
        if num_images == num_labels:
            print("✅ Counts match!\n")
        else:
            print(f"⚠️ Mismatch! Images: {num_images}, Labels: {num_labels}\n")
        
        total_files += num_images + num_labels

    # Print a summary
    print("--- Summary ---")
    train_count = counts.get('train_images', 0)
    val_count = counts.get('val_images', 0)
    test_count = counts.get('test_images', 0)
    total_images = train_count + val_count + test_count
    
    print(f"Training images:   {train_count}")
    print(f"Validation images: {val_count}")
    print(f"Test images:       {test_count}")
    print("-----------------")
    print(f"Total images:      {total_images}")
    print(f"Total files (img + label): {total_files}")
    print("\nVerification complete.")


if __name__ == "__main__":
    verify_file_counts()