from flask import Flask, render_template, request, Response
import pir_motion_camera
from picamera import PiCamera
from gpiozero import MotionSensor
from threading import Condition
import io

camera = PiCamera()

PATH_IMAGES = "/home/pi/MotionCamera/images/"



app = Flask(__name__)


pir_motion_camera = pir_motion_camera.pir_motion_camera(camera, PATH_IMAGES)

pir = MotionSensor(4)

camera_state = "Off"



def camera_status(status):

    global camera_state
    camera_state = status

    if status == "On":
        pir.when_motion = pir_motion_camera.capture_image
    else:
        pir.when_motion = None

            




@app.route("/")
def index():
    

    templateData = { 
      	'camerastatus' : camera_state,
        'videolength': pir_motion_camera.video_lenght,
        'sleeptimer' : pir_motion_camera.sleeptimer
      	}


          ##ei toimi template


    return render_template('index.html', **templateData)



@app.route("/<controll>/<action>")
def serverControll(controll, action):
    if controll == 'camera':
        camera_status(action)


         

    return index()   


@app.route("/videolength/")
def video_lenght_controll():
    length = request.args.get('length')

    print(length)

    pir_motion_camera.video_lenght = (int)(length)
    


    return index()   


@app.route("/sleeptimer/")
def sleeptime_controll():
    length = request.args.get('length')

    pir_motion_camera.sleeptimer = (int)(length)


    return index() 


@app.route("/liveView/")
def live_view(): 


    
    return index()


def gen(camera):
    #get camera frame
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

if __name__ == "__main__":

    
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')

    app.run(host="0.0.0.0")