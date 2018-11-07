import argparse
import sys
sys.path.append("/home/tao/tensorflow/facenet/src")
import time
if "/opt/ros/lunar/lib/python2.7/dist-packages" in sys.path:
    sys.path.remove("/opt/ros/lunar/lib/python2.7/dist-packages")
import cv2
import face
import numpy as np
import serial

faces = None
target = None

def serial_init():
    ser=serial.Serial()
    ser.baudrate = 115200
    ser.port = '/dev/ttyUSB0'
    ser.timeout = 3
    ser.open()
    if ser.isOpen():
        return ser
    else:
        print("////////\ncould not open port\n////////")
        exit()
    
def servo_control(face_bb, img, ser):
    center = (int((face_bb[0]+face_bb[2])/2), int((face_bb[1]+face_bb[3])/2))
    cv2.circle(img, center, 7, (0, 0, 255), cv2.FILLED)
    height, width, _ = img.shape
    if center[0] > width / 2 + 0.05 * width:
        ser.write([0x32, 0x0d])
        #print("2")
    elif center[0] < width / 2 - 0.05 * width:
        ser.write([0x31, 0x0d])
        #print("1")
    if center[1] > height / 2 + 0.05 * height:
        ser.write([0x33, 0x0d])
        #print("3")
    elif center[1] < height / 2 - 0.05 * height:
        ser.write([0x34, 0x0d])
        #print("4")
    
def locate_targets(faces, target, frame, frame_rate, servo, ser):
    if faces is not None:
        for face in faces:
            if face.name == None:
                face_bb = face.bounding_box.astype(int)
                cv2.rectangle(frame,
                              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                              (0, 255, 0), 2)
            elif face.name == target:
                face_bb = face.bounding_box.astype(int)
                #print(servo)
                if servo:
                    servo_control(face_bb, frame, ser)
                cv2.rectangle(frame,
                              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                              (0, 0, 255), 5)
                cv2.putText(frame, face.name + ' ' + face.prob + "%", (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        thickness=2, lineType=2)
            else:
                face_bb = face.bounding_box.astype(int)
                cv2.rectangle(frame,
                              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                              (0, 255, 0), 2)
                cv2.putText(frame, face.name + ' ' + face.prob + "%", (face_bb[0], face_bb[3]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        thickness=2, lineType=2)
    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def click_in_box(face_bb, x, y):
    if face_bb[0] > face_bb[2]:
        temp = face_bb[0]
        face_bb[0] = face_bb[2]
        face_bb[2] = temp
    if face_bb[1] > face_bb[3]:
        temp = face_bb[1]
        face_bb[1] = face_bb[3]
        face_bb[3] = temp
    if face_bb[0] < x < face_bb[2] and face_bb[1] < y < face_bb[3]:
        return True
    else:
        return False

def select_target(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if faces is None:
            return
        else:
            for face in faces:
                if face.name is not None:
                    face_bb = face.bounding_box.astype(int)
                    if click_in_box(face_bb, x, y):
                        global target
                        target = face.name
                        print("////////\ntarget:{}\n////////".format(target))
def main(args):
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 3  # seconds
    frame_rate = 0
    frame_count = 0
    global faces
    global target
    
    face_recognition = face.Recognition()
    start_time = time.time()

    face.recog_threshold = args.threshold
    target = args.target
    servo = args.servo
    print("////////\n{}\n////////".format(args))
    camera = args.camera
    video_capture = cv2.VideoCapture(camera)
    if not video_capture.isOpened():
        print("////////\nCould not open camera\n////////")
        exit()
    video_capture.isOpened()
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", select_target)
    '''
    mtx = np.eye(3)
    mtx[0][0] = 243.8972
    mtx[0][1] = 0.0
    mtx[0][2] = 320.5543
    mtx[1][1] = 251.9846
    mtx[1][2] = 233.7917

    dist = np.zeros((5,1))
    dist[0][0] = -0.1199
    dist[1][0] = 0.0092
    '''
    if servo:
        ser = serial_init()
    else:
        ser = None
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        """
        h, w = frame.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        """
        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        #add_overlays(frame, faces, frame_rate)
        locate_targets(faces, target, frame, frame_rate, servo, ser)
        frame_count += 1
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-target', type=str, default=None)
    parser.add_argument('-threshold', help='recognition threshold', type=float, default=0.5)
    parser.add_argument("-servo", action="store_true", default=False)
    parser.add_argument("-camera",type=int, default=0)
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
