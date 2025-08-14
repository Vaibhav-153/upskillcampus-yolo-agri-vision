from ultralytics import YOLO

def main():
    """
    This function runs hyperparameter tuning on the YOLOv8 model
    to find the best possible training settings for the dataset.
    """
    # Load the base pre-trained model, not your custom one
    model = YOLO('yolo11n.pt')

    print("Starting hyperparameter tuning...")

    # Run the tuner
    # This will train the model multiple times with different settings.
    # It can take a long time to complete.
    results = model.tune(
        data='data/sesame_dataset/data.yaml',
        epochs=50,  # Use fewer epochs for tuning to save time
        imgsz=512,
        iterations=12 # Number of trials to run
    )

    print("Tuning finished.")
    print(f"Best hyperparameters saved to: {results.best_hyperparameters}")

if __name__ == '__main__':
    main()