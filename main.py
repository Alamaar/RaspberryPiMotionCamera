from flask import Flask, render_template, request
import pir_motion_camera
from picamera import PiCamera
from gpiozero import MotionSensor

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


if __name__ == "__main__":

    

    app.run(host="0.0.0.0")