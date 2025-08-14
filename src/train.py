from ultralytics import YOLO

def main():
    """
    This function loads a pre-trained YOLOv8 model and trains it on the custom dataset.
    """
    # Load a pre-trained YOLO11n model. 
    # We start with 'yolov11n.pt' (small) for a good balance of speed and accuracy.
    # You can also use 'yolov11n.pt' (nano) for faster training or larger models for higher accuracy.
    model = YOLO('yolo11n.pt')

    print("Starting model training...")
    
    # Train the model using the dataset configuration file.
    # The training process will automatically use the augmentations specified in the library.
    results = model.train(
        data='\data\sesame_dataset\data.yaml',  # Path to your dataset config file
        epochs=100,                              # Number of training epochs
        imgsz=512,                               # Image size for training
        batch=16,                                # Number of images per batch (lower if you have VRAM issues)
        name='sesame_weed_yolov8s_final'         # Name for the training run folder
    )

    print("Training finished.")
    print(f"Model and results saved to: {results.save_dir}")

if __name__ == '__main__':
    main()