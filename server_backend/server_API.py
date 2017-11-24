from gevent.wsgi import WSGIServer
from flask import Flask, request, Response
import time
import os
app = Flask(__name__)

userhome = os.path.expanduser('~')
path_for_files = userhome + "/MyFancyDoorOpener_BackEnd_ver2/server_backend"


@app.route('/')
def index():
    return 'Under construction!'


@app.route('/setframerate')
def set_framerate():
    rate = request.args.get("rate", default="24", type=str)
    if rate == '0':
        rate = '24'

    with open(path_for_files + "/frame_rate.txt", "w") as f:
        f.write(rate)
        return "Frame rate set!"


@app.route('/getnotification')
def get_notification():
    with open(path_for_files + "/notification.txt") as f:
        notification = f.read()  # 0 for no and 1 for yes
    print notification
    return notification


@app.route('/getname')
def get_name():
    #person_name = fr.recognize(path_for_files + '/video/web_cap.jpg')
    with open(path_for_files + "/person_name.txt", 'r') as f:
        person_name = f.read()

    # with open(path_for_files + "/person_name.txt", "r") as fin:
    #     person_name = fin.read()
    #     # print person_info
    #     return person_name
    return person_name


@app.route('/getdistance')
def get_distance():
    with open(path_for_files + "/person_distance.txt", "r") as fin:
        person_distance = fin.read()
        # print person_info
        return person_distance


@app.route('/setauth', methods=['GET', 'POST'])
def set_auth():
    # with open(path_for_files + "/person_name.txt", 'r') as f:
    #     person_name = f.read()
    with open(path_for_files + "/person_distance.txt", "r") as f:
        person_distance = int(f.read())
    # if person_name != 'Huy':
    #     return "Name not exist!"
    if person_distance > 1500 or person_distance < 500:
        return "Distance not matched!"
    else:
        with open(path_for_files + "/auth_stat.txt", "w") as f:
            f.write("1")
        return "Auth set!"


@app.route('/resetauth', methods=['GET', 'POST'])
def reset_auth():
    with open(path_for_files + "/auth_stat.txt", "w") as f:
        f.write("0")
    return "Auth reset!"


def load_photo():
    start = time.time()
    while True:
        end = time.time()
        if end - start > 10:
            with open(path_for_files + "/frame_rate.txt", "r") as f:
                rate = f.read()
                frame_rate = int(rate)
                print "Current frame rate: " + rate + "fps"
            start = time.time()
        frame = open(path_for_files + '/video/web_cap.jpg').read()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(1.0/frame_rate)


@app.route('/video_feed')
def video_feed():
    return Response(load_photo(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()
