import torch
from PIL import Image

# Load trained YOLOv5 model with custom weights
model = torch.hub.load('ultralytics/yolov8', 'custom', path='./best.pt', force_reload=True)

# Load image
img_path = 'ring4.jpg'
img = Image.open(img_path)

# Perform inference
results = model(img)

# Print results
results.print()

# Count detected objects
num_objects = len(results.xyxy[0])

print(f"Number of detected objects: {num_objects}")
