import os

# --- CONFIGURATION ---
# IMPORTANT: SET THIS TO THE PATH OF YOUR FOLDER CONTAINING ALL IMAGES AND .TXT FILES
SOURCE_DIR = r"C:\Users\VAIBHAV ADMANE\Downloads\agri_data\data"

# --- MAIN SCRIPT ---

def clean_dataset_pairs():
    """
    Finds and removes image files without a matching .txt file and
    .txt files without a matching image file in the source directory.
    """
    if not os.path.isdir(SOURCE_DIR):
        print(f"Error: Source directory not found at '{SOURCE_DIR}'")
        return

    # Get the base filenames (without extensions) for all files
    image_basenames = set()
    label_basenames = set()
    
    # Store full paths to delete later
    files_to_delete = []
    
    # First, get all file names
    all_files = os.listdir(SOURCE_DIR)
    
    for filename in all_files:
        basename, extension = os.path.splitext(filename)
        extension = extension.lower()
        
        if extension in ['.jpg', '.jpeg', '.png']:
            image_basenames.add(basename)
        elif extension == '.txt':
            label_basenames.add(basename)

    print(f"Found {len(image_basenames)} unique image files and {len(label_basenames)} unique label files.")

    # Find images that don't have a corresponding label
    images_without_labels = image_basenames - label_basenames
    for basename in images_without_labels:
        # Find the full image filename (with original extension)
        for filename in all_files:
            if os.path.splitext(filename)[0] == basename and os.path.splitext(filename)[1].lower() in ['.jpg', '.jpeg', '.png']:
                files_to_delete.append(os.path.join(SOURCE_DIR, filename))
                print(f"Orphaned Image (no label): Found '{filename}'")
                break


    # Find labels that don't have a corresponding image
    labels_without_images = label_basenames - image_basenames
    for basename in labels_without_images:
        label_filename = f"{basename}.txt"
        files_to_delete.append(os.path.join(SOURCE_DIR, label_filename))
        print(f"Orphaned Label (no image): Found '{label_filename}'")
    
    if not files_to_delete:
        print("\n✅ Your dataset is perfectly paired. No files to delete.")
        return

    # Deletion confirmation
    print(f"\nFound {len(files_to_delete)} orphaned files to delete.")
    user_input = input("Are you sure you want to permanently delete these files? (yes/no): ").lower()

    if user_input == 'yes':
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                print(f"Deleted: {os.path.basename(filepath)}")
            except OSError as e:
                print(f"Error deleting {filepath}: {e}")
        print("\nCleanup complete.")
    else:
        print("\nCleanup cancelled. No files were deleted.")


if __name__ == "__main__":
    clean_dataset_pairs()