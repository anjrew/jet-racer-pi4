import os

if os.path.exists('/dev/video0'):
    print("Camera device is present.")
else:
    print("Camera device is not present.")
