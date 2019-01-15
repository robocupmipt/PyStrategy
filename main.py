from connectors import MotionConnector
from connectors import MovementConnector
from CVConnector import CVConnector
import time


class Strategy(object):
    def __init__(self, IP):
        self.IP = IP
        self.motion = MovementConnector(IP)
        self.standard_motion = MotionConnector(IP)
        self.cv = CVConnector(IP)
        self.FIRST_MAGIC_CONST = 1
        self.SECOND_MAGIC_CONST = 0.3
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.head_x = 0
        self.head_y = 0
        self.head_height = 51.2
        self.F = 600

    def test(self):
        self.update_ball_data()

    def start(self):
        self.standard_motion.StandUp()

        while True:
            self.motion.LookDown(0)

            if self.grid_search():
                angle = self.get_ball_angle()
                print(angle)

                self.motion.Move(0, 0, angle)

                self.motion.SetHeadHorizontalAngle(0)
                self.motion.SetHeadVerticalAngle(0)
                self.motion.Move(0.5, 0, 0)
            else:
                self.motion.Move(1, 0, 0)

    def grid_search(self):
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(0)

        horizontal_range = 60
        dir_sign = 1

        bottomVerticalBound = -5
        topVerticalBound = 20

        self.head_y = bottomVerticalBound
        while self.head_y < topVerticalBound:
            self.motion.SetHeadVerticalAngle(self.head_y)  # set vertical angle

            self.head_x = -horizontal_range * dir_sign
            while dir_sign * self.head_x - horizontal_range <= 0:
                self.motion.SetHeadHorizontalAngle(self.head_x )  # set horizontal angle
                time.sleep(0.1)
                self.update_ball_data()

                if self.is_see_ball():
                    print("Find ball in " + str((self.x, self.y)))
                    return True
                self.head_x += dir_sign * 10
            self.head_y += 8
            dir_sign *= -1

        return False

    def get_ball_angle(self):
        image_w = 640
        view_degree = 45

        print("ball coordinates: ", self.x, self.y)
        find_angle = -view_degree * self.x / image_w
        print("Find ball angle on pics is " + str(find_angle))
        print(self.head_x)

        return -view_degree * self.x / image_w + self.head_x

    def get_ball_distace(self):
        pass
        #return self.F * self.head_height /

    def update_ball_data(self):
        self.x, self.y, self.w, self.h = self.cv.get_all_ball_data()

    def is_see_ball(self):
        return self.x is not None


def main():
    a = Strategy("192.168.1.5")
    #a.test()
    a.start()

main()
