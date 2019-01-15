from ModuleConnector import ModuleConnector

class CVConnector(object):
    def __init__(self, ip):
        self.IP = ip
        pass

    def is_see_ball(self):
        return False

    def get_ball_center(self):
        return (0, 0)

    def get_ball_size(self):
        return (1, 1)