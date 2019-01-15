from naoqi import ALProxy
import cv2
from PIL import Image, ImageDraw
import numpy as np
import time

class CVConnector(object):
    def __init__(self, ip, 
                 ballfinder_dirs=['top_cascade.xml','other_cascade.xml','bottom_cascade.xml'],
                 camera_id=1):
        '''
        ballfinder_dir - directory of classifier
        camera_id - id of camera.
        Note: we use top_cascade.xml only with camera_id = 0
        and bottom_casca
        '''
        self.IP = ip
        self.PORT = 9559
        self.ballfinders= [cv2.CascadeClassifier(ballfinder_dir)
        for ballfinder_dir in ballfinder_dirs]
        self.camera_id = camera_id
        self.last_image=None

    def get_image(self, image_dir=None):
        '''
        yaw is a horisontal angle ( -2.0857 to 2.0857 )
        pitch is a vertical angle ( -0.6720 to 0.5149)
        speed is a speed of head rotation ( from 0 to 1)
        num_balls = number of balls
        Note that max abs of pitch value depends on the max abs of yaw value
        http://doc.aldebaran.com/1-14/family/robots/joints_robot.html
        '''
        #ses = qi.Session()
        #ses.connect(self.IP)
        #video = ses.service('ALVideoDevice')
        if image_dir:
            self.last_image = cv2.imread(image_dir)
        else:
            video = ALProxy('ALVideoDevice', self.IP, self.PORT)
            videoClient = video.subscribeCamera("python_client",
                                                self.camera_id, 2, 11, 5)
        
            naoImage = video.getImageRemote(videoClient)
            video.unsubscribe(videoClient)
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            array = naoImage[6]
            im = Image.frombytes("RGB", (imageWidth, imageHeight), str(array))
            if im is None:
                print('IMAGE TAKING FAILED')
            self.last_image = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

    def _get_ball(self, get_image=True,
                  scale_factor=1,
                  haar_params=(1.3, 5),
                  save_image=False,
                  save_dir='DETECTED_BALL.jpg',
                  print_=False,
                  num_balls=1):
        '''
        if get_image=True, we make new image, with parameters yaw,pitch,speed
        scale_factor is a parameter on which we rescale image before detect
        haar_params are params for ball finder
        if save_image=True, we save image after detection in save_dir.
        '''
        if get_image or self.last_image is not None:
            self.get_image()

        try:
            image1 = cv2.resize(self.last_image, 
                    (self.last_image.shape[0] // scale_factor,
                     self.last_image.shape[1] // scale_factor))
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        except:
            if print_:
                print('No image received')
            return None
        balls=[]
        for ballfinder in self.ballfinders:
            if len(balls)==0:
                balls_found = scale_factor*ballfinder.detectMultiScale(
                    image1, haar_params[0],haar_params[1])
                balls = balls_found

        balls = balls[:num_balls]
        for (x, y, w, h) in balls:
            image1 = cv2.rectangle(image1, (x,y),(x+w,y+h),(255,0,0),2)

        if save_image:
            cv2.imwrite(save_dir, image1)

        if len(balls)==0:
            if print_:
                print('No balls found - returning empty')
                #raise Exception
            return None
        
        return balls[0]

    def get_all_ball_data(self):
        ball_coords = self._get_ball()
        if ball_coords is None or len(ball_coords) == 0:
            cv2.imwrite("images/bad/{}.jpg".format(time.time()), self.last_image)
            return None, None, None, None


        x, y, w, h = ball_coords
        img = self.last_image
        cv2.rectangle(img,
                      (x, y), (x + w, y + h),
                      (255, 0, 0), 2)
        image_h, image_w = img.shape[:2]

        cv2.imwrite("images/good/{}.jpg".format(time.time()), img)

        print("DEBUG: " + str(ball_coords))
        print("DEBUF: " + str(img.shape[:2]))

        y = image_h - y
        center_x = x + w // 2 - image_w // 2
        center_y = y + h // 2 - image_h // 2
        return center_x, center_y, w, h

