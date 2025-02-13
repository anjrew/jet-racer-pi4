import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera device is accessible.")
else:
    print("Camera device is not accessible.")
cap.release()
