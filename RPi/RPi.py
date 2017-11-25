import socket
import cv2
import VL53L0X
import pyttsx
import time
import RPi_facerecapi as fr


# Get the server IP from the terminal
HOST = raw_input("Server address: ")
PORT = 9999
PORT_UDP = 10000


def send_video_file(file_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buf = 100*1024
    f = open(file_to_send, "rb")
    data = f.read(buf)
    s.sendto(data, (HOST, PORT_UDP))

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)


def get_distance_from_sensor():

    try:
        distance = tof.get_distance()

        return str(distance)
    except Exception as err:
        print "Error: " + err
        tof.stop_ranging()
        return '0'


def send_distance(distance):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("person_distance")
    print "person distance sent!"
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(distance)
    s.close()


def send_name(person_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("person_name")
    print "person name sent!"
    s.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(person_name)
    s.close()


def asking_auth():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send("asking_for_auth")

    auth_code = s.recv(10)
    auth_code = auth_code.strip()
    print(auth_code)
    if auth_code == '1':
        engine = pyttsx.init()
        engine.say('Welcome home Huy')
        engine.runAndWait()
    return


# Start streaming webcam
print "Starting camera."
cam = cv2.VideoCapture(0)
time.sleep(1)

# Retrieving frame rate for the first time
#frame_rate = asking_for_framerate()
start = time.time()

print "Start capturing images"
frames = 0
while 1:
    end = time.time()
    #Check new frame rate after every 15 seconds and call Kairos API
    #if end - start > 15:
        #frame_rate = asking_for_framerate()
        #print "Request Kairos API"
        #person_name = fr.recognize("webcam_cap.jpg")
        #print "name retrieved: " + str(person_name)

        #send_name(person_name)
        #person_distance = get_distance_from_sensor()
        #send_distance(person_distance)

        #start = time.time()

    #print "Frame rate: " + str(frame_rate)
    if end - start > 300:
        print "Num of frame sent: " + str(frames)
        break

    ret, frame = cam.read()
    if ret:
        # Resize before sending
        frame = cv2.resize(frame, (480, 270))
        cv2.imwrite("webcam_cap.jpg", frame)

        print "Sending a frame"
        send_video_file("webcam_cap.jpg")
        frames += 1
        #asking_auth()

        #have_face, face, rect = extract_a_face(frame, 1.2)
        #person_info = ""
        #if have_face:
        #   frame, person = predict(frame)
        #     person_info = "{person: " + person + ", distance: 500mm }"
        # else:
        #     person_info = "{person: none, distance: 0mm}"
        #cv2.imshow("Livestream", frame)

    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     break

    #time.sleep(1.0/frame_rate)
    #time.sleep(0.04)

tof.stop_ranging()
cam.release()
cv2.destroyAllWindows()



