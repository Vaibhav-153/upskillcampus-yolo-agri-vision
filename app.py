# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import torch
import os

# --- Configuration ---
app = Flask(__name__, static_folder='.')
CORS(app)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loading model on device: {device}")

# Construct the model path in a platform-independent way
MODEL_PATH = os.path.join('models', 'sesame_weed_detector_v1.pt')

# --- Model Loading with Better Error Checking ---
model = None
# Check if the model file exists before trying to load it
if os.path.exists(MODEL_PATH):
    try:
        model = YOLO(MODEL_PATH).to(device)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"FATAL ERROR: Model file not found at '{MODEL_PATH}'")
    print("Please ensure the 'models' folder and the '.pt' file exist in the correct location.")


# --- NEW: Route for the main page ---
@app.route('/')
def index():
    """
    This function serves the main index.html file when a user visits
    the root URL of the web application.
    """
    return send_from_directory('.', 'index.html')

# --- API Endpoint for Prediction ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Defines the /predict API endpoint. It receives an image,
    runs inference, and returns the detected object data as JSON.
    """
    if not model:
        return jsonify({'error': 'Model is not loaded or failed to load. Check server logs.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))

            results = model(image, conf=0.5)

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
    # Get the port from the environment variable, default to 7860
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
