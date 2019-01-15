from MovementConnector import MovementConnector
from CVConnector import CVConnector


class Strategy(object):
    def __init__(self, IP):
        self.motion = MovementConnector(IP)
        self.cv = CVConnector(IP)
        self.FIRST_MAGIC_CONST = 1
        self.SECOND_MAGIC_CONST = 0.3

    def test(self):
        self.motion.SetHeadHorizontalAngle(0)
        self.motion.SetHeadVerticalAngle(-29.5)
        while True:

            b = raw_input()

            print self.cv.get_ball_center()
            print self.cv.get_ball_size()

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

    def head_to_ball(self):
        pass

    def try_find_ball(self):
        v_angles = [ 38.5,   38.5,  -29.5, -29.5]
        h_angles = [119.5, -119.5, -119.5, 119.5]

        for h, v in zip(h_angles, v_angles):
            self.motion.SetHeadHorizontalAngle(h)
            self.motion.SetHeadVerticalAngle(v)

            if self.cv.is_see_ball():
                return True


def main():
    a = Strategy("192.168.1.5")
    a.test()

main()
