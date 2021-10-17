from datetime import datetime
from time import sleep


class pir_motion_camera:

    sleeptimer = 30
    video_lenght = 15
    camera = None
    camera_focus_timer = 4
    path_images = None

    def __init__(self, camera, path_images):
        self.camera = camera
        self.path_images = path_images





    def capture_image(self):
        #open camera
        self.camera.start_preview()
        print("Capturing image")

        filename = datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
        sleep(self.camera_focus_timer)
        self.camera.capture(self.path_images + filename + '.jpg')
        self.camera.stop_preview()

        sleep(self.sleeptimer)
    
    def capture_video(self):
        self.camera.start_preview()
        print("Recording video")

        filename = 'video-' + datetime.now().strftime("%d-%m-%Y-%H.%M.%S") 
        self.camera.start_recording(self.path_images + filename + '.h264')
        self.camera.wait_recording(self.video_lenght)
        self.camera.stop_recording()
        self.camera.stop_preview()

        sleep(self.sleeptimer)
        


    
        