from ultralytics import YOLO

def main():
    """
    This function loads a trained YOLOv8 model and evaluates its performance
    on the validation set defined in the data.yaml file.
    """
    # IMPORTANT: Update this path to your specific 'best.pt' file
    model_path = 'models/crop_weed_detector_v1.pt'
    
    print(f"Loading trained model from: {model_path}")
    
    # Load the trained model
    model = YOLO(model_path)

    print("Starting model validation...")
    
    # Evaluate the model's performance
    metrics = model.val(
        data='data/sesame_dataset/data.yaml',  # Path to your dataset config file
        split='val'                             # Specify you want to run on the validation set
    )
    
    print("Validation finished.")
    # The 'metrics' object contains detailed performance results like mAP50-95, precision, and recall.
    # The results are also printed to the console automatically.
    # You can access specific metrics like this:
    print(f"mAP50-95: {metrics.box.map}")
    print(f"Precision: {metrics.box.mp}")
    print(f"Recall: {metrics.box.mr}")


if __name__ == '__main__':
    main()