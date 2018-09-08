import sys
if "/opt/ros/lunar/lib/python2.7/dist-packages" in sys.path:
    sys.path.remove("/opt/ros/lunar/lib/python2.7/dist-packages")
import cv2
import os
import time


script_path = os.path.abspath(__file__)
raw_dir = os.path.abspath(os.path.join(script_path, '..', 'data', 'raw'))
cap = cv2.VideoCapture(0)
while True:
    print("Name:")
    person = input("> ")
    person_dir = os.path.join(raw_dir, person)
    all_person = os.listdir(raw_dir)
    print("There are {} people in raw_dir.".format(len(all_person)))
    bool = True
    while bool:
        if not person in all_person:
            os.mkdir(person_dir)
            break
        else:
            print("{} is already in the dir".format(person))
            print("Are you sure to continue? (y/n)")
            while True:
                ans = input("> ")
                if ans == 'y':
                    bool = False
                    break
                elif ans == 'n':
                    print("Name:")
                    person = input("> ")
                    person_dir = os.path.join(raw_dir, person)
                    break
                else:
                    print("Please enter 'y' or 'n'.")
    print("Press enter to take photos.")
    input("> ")

    if not cap.isOpened():
        print("Error! Unable to open camera!")
    else:
        font = cv2.FONT_HERSHEY_COMPLEX
        img_count = len(os.listdir(person_dir))
        while True:
            ret, frame = cap.read()
            frame_copy = frame
            cv2.putText(frame, "Press 's' to save image, 'q' to quit.", (0, 20), font, 0.6, (0, 0, 255), 1)
            cv2.imshow("sampling", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):
                t = time.localtime(time.time())
                img = os.path.join(person_dir, "{}{}{}{}{}{}.png".format(t.tm_year, t.tm_mon, t.tm_mday,
                        t.tm_hour, t.tm_min, t.tm_sec))
                print(img)
                cv2.imwrite(img, frame_copy)
                img_count = img_count + 1
                print("There are {} photos in dir.".format(img_count))
            elif key == ord("q"):
                cv2.destroyAllWindows()
                break
    print("Now there are {} photos in {}'s dir.".format(img_count, person))
    print("Enter 'c' to continue sampling.")
    ans = input("> ")
    if ans != 'c':
        break
