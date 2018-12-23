# To use this software, you must define constant variables.
# Make sure you understand the limitations of storage capacity.
#
# example :
#     1 hour video file
#     VIDEOLENGTH = 3600
#  ==>1 GB each file (with default PiCamera config values)
#
#     16 GB Sd Card 
#  ==>11 GB usable space
#     MAXDIRLENGHT = 10000 (usable space - each file size = 10 GB)
#
#author: Donavan Martin
#donavan.martin@algorithmesolutions.com
#
# LICENSE : MIT 
# enjoy :)
#

# camera
from picamera import PiCamera
camera = PiCamera()

# time
from datetime import datetime
from time import sleep
VIDEOLENGTH = 3600 # in secondes
MAXVIDEOINTERVAL = 86400 # 60 sec. * 60 min. * 24 hours
MAXNUMBERFILES = MAXVIDEOINTERVAL / VIDEOLENGTH;

# files
import os
MAXDIRLENGHT = 10000 # in Megabytes(MB)
PATH = '/home/pi/videos/'
format = '.h264'

def init():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    print("Video files path:"+PATH)

def get_size():
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(PATH):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size/1000 # in MegaBytes

def get_numberFiles():
    files = os.listdir(PATH)
    nb_files = len([name for name in files])
    return nb_files

def cleanDirectory():
    print("Folder size:"+str(get_size()))

    while get_size()>MAXDIRLENGHT or  get_numberFiles() > MAXNUMBERFILES:
        print("Need to release space.")
        print("\tSpace user: %d/%d (MB) used" % (get_size(),MAXDIRLENGHT))
        print("\tNumber of files: %d/%d" % (get_numberFiles(),MAXNUMBERFILES))

        files = os.listdir(PATH)
        full_path = [PATH+"/{0}".format(x) for x in files]
        if len([name for name in files]) > 0:
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)
            print("oldest file removed:"+oldest_file)
        else: 
           print("Error should nerver append!")
           break
    print("Enough space: %d/%d (MB)" % (get_size(),MAXDIRLENGHT))

def main():
    while(True):
        cleanDirectory()
        dt = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        file = PATH+dt+format
        camera.start_preview()
        camera.start_recording(PATH+dt+format)
        print('New file:'+file)

        for x in range(1,VIDEOLENGTH):
            print('.', end='',flush=True)
            sleep(1)

        camera.stop_recording()
        camera.stop_preview()
        print('File closed:'+file)

if __name__ == "__main__":
    while(True): # Recording is more important...
        try:
            print("Video surveillance software start")
            init()
            main()
        except ValueError as err:
            print("Software ERROR! cause:",err)
