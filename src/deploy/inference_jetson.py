# src/deploy/inference_jetson.py

# This script is designed to run on an NVIDIA Jetson Nano or similar device.
# It captures video from a camera, runs real-time inference, and activates a sprayer
# when a weed is detected.

import cv2
from ultralytics import YOLO
import torch
import time
import gpio_controller as sprayer # Import your GPIO controller script

# --- Configuration ---
MODEL_PATH = 'models/crop_weed_detector_v1.pt'
CONFIDENCE_THRESHOLD = 0.65 # Be 65% sure it's a weed before spraying
SPRAY_DURATION = 0.3 # Spray for 0.3 seconds

# --- Main Application Logic ---
def main():
    """
    Initializes the model, camera, and GPIO, then enters a real-time
    detection loop.
    """
    # Check for GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    # Load the trained YOLO model
    try:
        model = YOLO(MODEL_PATH).to(device)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Initialize the camera
    # '0' is typically the default built-in camera. If you have a USB camera,
    # it might be '1' or higher.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    print("Camera started successfully.")

    # Set up the GPIO pins for the sprayer
    sprayer.setup_gpio()

    try:
        while True:
            # Read a frame from the camera
            success, frame = cap.read()
            if not success:
                print("Error: Failed to capture frame.")
                break

            # Run inference on the current frame
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False) # verbose=False cleans up console output

            # The 'results' object is a list. We work with the first element.
            result = results[0]

            # Assume no weed is detected in this frame initially
            weed_is_detected = False

            # Loop through all detected objects in the frame
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                # Check if the detected object is a 'weed'
                if class_name.lower() == 'weed':
                    weed_is_detected = True
                    
                    # Draw a red box around the detected weed for visualization
                    coords = box.xyxy[0].tolist()
                    x1, y1, x2, y2 = map(int, coords)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    label = f"Weed: {box.conf[0]:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # After checking all objects, if a weed was found, activate the sprayer
            if weed_is_detected:
                sprayer.activate_sprayer(SPRAY_DURATION)
                print("Weed detected! Activating sprayer.")
                # Add a small delay to prevent continuous spraying for the same weed
                time.sleep(1) 

            # Display the resulting frame (optional, but good for debugging)
            cv2.imshow("Crop & Weed Detection", frame)

            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        # Release all resources
        cap.release()
        cv2.destroyAllWindows()
        sprayer.cleanup_gpio()
        print("Resources released. Exiting.")

if __name__ == '__main__':
    main()
