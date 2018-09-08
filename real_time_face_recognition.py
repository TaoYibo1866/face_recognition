import argparse
import sys
sys.path.append("/home/tao/tensorflow/facenet/src")
import time
if "/opt/ros/lunar/lib/python2.7/dist-packages" in sys.path:
    sys.path.remove("/opt/ros/lunar/lib/python2.7/dist-packages")
import cv2
import face


def locate_targets(faces, targets, frame, frame_rate):
    if faces is not None:
        for face in faces:
            if face.name == None:
                face_bb = face.bounding_box.astype(int)
                cv2.rectangle(frame,
                              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                              (0, 255, 0), 2)
            elif face.name in targets:
                face_bb = face.bounding_box.astype(int)
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

def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        for face in faces:
            face_bb = face.bounding_box.astype(int)
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (0, 255, 0), 2)
            if face.name is not None:
                cv2.putText(frame, face.name + ' ' + face.prob + "%", (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)


def main(args):
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    video_capture = cv2.VideoCapture(0)
    face_recognition = face.Recognition()
    start_time = time.time()

    face.recog_threshold = args.threshold
    targets = args.collection
    print(targets)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        #add_overlays(frame, faces, frame_rate)
        locate_targets(faces, targets, frame, frame_rate)
        frame_count += 1
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='append', dest='collection',
        default=[],
        help='Add repeated values to a list')
    parser.add_argument('-threshold', help='recognition threshold', type=float, default=0.5)
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
