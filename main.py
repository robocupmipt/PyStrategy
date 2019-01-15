from MovementConnector import MovementConnector
from CVConnector import CVConnector
import time

class Strategy(object):
    def __init__(self, IP):
        self.motion = MovementConnector(IP)
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
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(0)
        while True:

            b = raw_input()

            self.update_ball_data()
            print(self.x, self.y)

    def start2(self):
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(0)

        while not self.grid_search():
            continue

        angle = self.get_ball_angle()
        print(angle)

        #self.motion.Move(0, 0, angle / 180 * 3.1415)




    def start(self):
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(-29.5)
        while True:
            while not self.cv.is_see_ball():
                self.motion.Move(2, 0, 0)

            w, h = self.cv.get_ball_size()
            while w * h >= self.FIRST_MAGIC_CONST:
                self.motion.Move(0.5, 0, 0)

            x, y = self.cv.get_ball_center()
            self.motion.Move(self.SECOND_MAGIC_CONST, 0, 0)

            if x >= 0:
                self.motion.RightKick()
            else:
                self.motion.LeftKick()

    def grid_search(self):
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(0)

        leftHorizontalBound = -60
        rightHorizontalBound = 60

        bottomVerticalBound = -5
        topVerticalBound = 20

        self.head_y = bottomVerticalBound
        self.head_x = leftHorizontalBound

        while self.head_y < topVerticalBound:
            self.motion.SetHeadVerticalAngle(self.head_y)  # set vertical angle


            while self.head_x < rightHorizontalBound:
                self.motion.SetHeadHorizontalAngle(self.head_x )  # set horizontal angle
                time.sleep(0.1)
                self.update_ball_data()

                if self.is_see_ball():
                    print("Find ball in " + str((self.x, self.y)))
                    return True
                self.head_x += 10
            self.head_y += 8

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
    a.test()
    #a.start2()

main()
