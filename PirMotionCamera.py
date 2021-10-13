

















class pir_motion_camera:

    def capture_image():
    #open camera
    camera.start_preview()

    filename = datetime.now().strftime("%d-%m-%Y-%H.%M.%S")
    sleep(4)
    camera.capture(os.getcwd() +PATH_IMAGES + filename + '.jpg')
    camera.stop_preview()

    return filename