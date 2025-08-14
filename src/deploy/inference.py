from ultralytics import YOLO

def main():
    """
    This function trains the final model using the best hyperparameters
    found during the tuning process.
    """
    # Load the base model you want to train
    model = YOLO('yolo11n.pt')

    print("Starting final model training with tuned hyperparameters...")

    # Train the model with the new, optimized parameters
    results = model.train(
        data='data/sesame_dataset/data.yaml',
        epochs=150,  # Train for a good number of epochs for the final model
        imgsz=512,
        name='final_yolo11n_tuned_model',
        
        # Add the best hyperparameters you found from tuning
        lr0=0.01108,
        lrf=0.01006,
        momentum=0.90513,
        weight_decay=0.00054,
        warmup_epochs=2.59818,
        warmup_momentum=0.65406,
        box=5.10279,
        cls=0.52171,
        dfl=1.51701,
        hsv_h=0.01442,
        hsv_s=0.6187,
        hsv_v=0.35444,
        degrees=0.0,
        translate=0.11739,
        scale=0.46235,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.42938,
        bgr=0.0,
        mosaic=0.97391,
        mixup=0.0,
        cutmix= 0.0,
        copy_paste= 0.0
    )

    print("Final training finished.")
    print(f"Your best model is saved in: {results.save_dir}")

if __name__ == '__main__':
    main()