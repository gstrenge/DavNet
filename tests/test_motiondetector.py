from src.DoorCam.motiondetector import MotionDetector
import cv2


cap = cv2.VideoCapture(0)

scale = .25

background = None




while True:

    # Capture Frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    if background is None:
        background = gray
        continue

    cv2.accumulateWeighted(gray, background, .5)



    # If no frame returned, continue
    if not ret:
        continue

    cv2.imshow('Webcam', cv2.flip(background, 1))
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
