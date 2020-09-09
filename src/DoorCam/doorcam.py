from flask import Response, Flask, render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

lock = threading.Lock()

app = Flask(__name__)

cam = cv2.VideoCapture(0)

outputFrame = None

@app.route('/')
def index():
    return render_template("index.html")


def capture_image():
    global outputFrame, lock
    while True:
        _, frame = cam.read()
        with lock:
            outputFrame = frame.copy()
        time.sleep(1.0/30.0)

def generate():
    global lock, cam

    while True:
        with lock:

            if outputFrame is None:
                continue

            (flag, encodedImage) = cv2.imencode('.jpg', outputFrame)
            if not flag:
                continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line argumentshow to make and run a bas
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=capture_image)
    t.daemon = True
    t.start()
    # start the flask app

    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)
# release the video stream pointer


cam.release()

# python doorcam.py --ip 127.0.0.1 --port 80