import picamera

# 安裝 sudo apt-get install python3-picamera
# 預設解析度1280x800
with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.capture('image.jpg')
