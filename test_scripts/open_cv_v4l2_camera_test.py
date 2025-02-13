import cv2
pipeline = "v4l2src device=/dev/video0 ! videoconvert ! appsink"
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

ret, frame = cap.read()
if ret:
    cv2.imwrite('capture.jpg', frame)
cap.release()
