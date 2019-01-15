from MovementConnector import MovementConnector
from CVConnector import CVConnector


class Strategy(object):
    def __init__(self, IP):
        self.motion = MovementConnector(IP)
        self.cv = CVConnector(IP)


    def start(self):
        while not self.cv.is_see_ball();

    def head_to_ball(self):




    def try_find_ball(self):
        v_angles = [38.5, 38.5, -29.5, -29.5]
        h_angles = [119.5, -119.5, 119.5, -119.5]

        for h, v in zip(h_angles, v_angles):
            self.motion.SetHeadHorizontalAngle(h)
            self.motion.SetHeadVerticalAngle(v)

            if self.cv.is_see_ball():
                return True

def main():
    pass