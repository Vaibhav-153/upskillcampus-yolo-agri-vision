# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
from ultralytics import YOLO
from PIL import Image
import io
import torch

# --- Configuration ---
# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes. This is crucial for allowing your
# frontend to communicate with this backend.
CORS(app)

# Check if a GPU is available and set the device accordingly
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loading model on device: {device}")

# Load your final, trained YOLO model
# IMPORTANT: Make sure this path points to your best model file
MODEL_PATH = 'models/crop_weed_detector_v1.pt' 
try:
    model = YOLO(MODEL_PATH).to(device)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- API Endpoint for Prediction ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Defines the /predict API endpoint. It receives an image,
    runs inference, and returns the detected object data as JSON.
    """
    if not model:
        return jsonify({'error': 'Model is not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))

            # Run YOLO model prediction
            results = model(image, conf=0.5) # 50% confidence threshold

            # Process results
            detections = []
            for result in results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    confidence = float(box.conf[0])
                    coords = box.xyxy[0].tolist()
                    
                    detections.append({
                        'class_name': class_name,
                        'confidence': round(confidence, 2),
                        'coordinates': coords
                    })
            
            print(f"Detections: {detections}")
            return jsonify(detections)

        except Exception as e:
            print(f"Error processing image: {e}")
            return jsonify({'error': 'Error processing image'}), 500

# --- Main Function to Run the App ---
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible from any IP address
    app.run(host='0.0.0.0', port=7860)