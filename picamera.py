from picamera2 import Picamera2

# Create a Picamera2 instance and start the camera
picam2 = Picamera2()
picam2.start()

# Capture an image as a NumPy array
image = picam2.capture_array()

# Save or process the image as needed...
