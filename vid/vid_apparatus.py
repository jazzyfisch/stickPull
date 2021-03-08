import picamera
from datetime import datetime, timedelta
from time import sleep
import shutil
import os

#script settings:
length = 1 #duration of the each video file in hours
num = 10 #number of videos
ovl_pref = 'Enclosure 2 - ' #Overlay text prefix 
#f_name_pref = '/home/pi/Dev/record/videos/Enclosure_2_'
#f_name_pref = '/mnt/piwebcam/vid/Enclosure_2_'
f_name_pref = '/home/pi/Documents/vid/Enclosure_2_'


s_length = length*3600 #calculate seconds in hours

def cmd(_t):
    global f_name
    with picamera.PiCamera(resolution=(1024,768),framerate=15,sensor_mode=4) as camera:
        camera.start_preview()
        #camera.annotate_background = picamera.Color('black')
        #camera.annotate_background = picamera.Color('black')+ picamera.Color.Lightness(0.1)
        dt = datetime.now().strftime('%Y-%m-%d_%H:%M')
        camera.annotate_text = ovl_pref+dt
        f_name = f_name_pref+dt+'.h264'
        print('File name = '+f_name)
        print('')
        camera.start_recording(f_name)
        camera.exposure_mode='night'
        camera.awb_mode = 'off'
        camera.awb_gains = 0.3
        start = datetime.now()
        while (datetime.now() - start).seconds < _t:
            dt = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            camera.annotate_text = ovl_pref+dt
            camera.wait_recording(0.2)
        camera.stop_recording() 
            

for i in range(num):
    cmd(s_length)
    new_f_name = f_name.split('/')[5]
    print(new_f_name)
    try:
        shutil.move(f_name,('/mnt/piwebcam/vid/'+new_f_name))
        os.remove(f_name)
    except:
        pass
    
print('')
print('Done')



    
    
    
    
    
    
    
    







