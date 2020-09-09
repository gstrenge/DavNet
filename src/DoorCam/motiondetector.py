import cv2


class MotionDetector:
    """
    Detects the motion in a Camera Feed based on previous frames
    :param cam: The Camera ID that is streaming the feed (Defaultly 0)
    :param scale_factor: The Scale factor that the frames will be scaled to

    """

    def __init__(self, cam=0):

        self.cap = cv2.VideoCapture(cam, scale_factor)

        if not self.cap.isOpened():
            raise Exception(f"Cannot open camera: {cam}")
            exit()

        self.scale_factor = scale_factor




