import sys
import traceback
from naoqi import ALProxy


class ModuleConnector(object):
    def __init__(self, module_name, IP):
        self.IP = IP
        self.PORT = 9559
        self.module_name = module_name
        self.proxy = None
        self.connect()

    def connect(self):
        while not self.try_connect():
            continue

    def try_connect(self):
        try:
            self.proxy = ALProxy(self.module_name, self.IP, self.PORT)
        except RuntimeError:
            self.eprint()
            return False

        return True

    def eprint(self):
        print("ERROR:", traceback.format_exc())

class MovementConnector(ModuleConnector):
    def __init__(self, ip):
        ModuleConnector.__init__(self, "MovementGraph", ip)

    def Move(self, x, y, theta):
        try:
            self.proxy.Move(x, y, theta)
        except RuntimeError:
            self.eprint()
            return False

    def RightKick(self):
        try:
            self.proxy.RightKick()
        except RuntimeError:
            self.eprint()
            return False

    def LeftKick(self):
        try:
            self.proxy.LeftKick()
        except RuntimeError:
            self.eprint()
            return False

    def GetHeadVerticalAngle(self):
        try:
            self.proxy.GetHeadVerticalAngle()
        except RuntimeError:
            self.eprint()
            return False

    def GetHeadHorizontalAngle(self):
        try:
            self.proxy.GetHeadHorizontalAngle()
        except RuntimeError:
            self.eprint()
            return False

    def SetHeadVerticalAngle(self, angle):
        try:
            self.proxy.SetHeadVerticalAngle(angle)
        except RuntimeError:
            self.eprint()
            return False

    def SetHeadHorizontalAngle(self, angle):
        try:
            self.proxy.SetHeadHorizontalAngle(angle)
        except RuntimeError:
            self.eprint()
            return False


class MotionConnector(ModuleConnector):
    def __init__(self, ip):
        ModuleConnector.__init__(self, "ALMotion", ip)

    def RightKick(self):
        # Kick towards left with right leg
        #self.proxy.setFallManagerEnabled(False)
        names = ['RShoulderRoll', 'RShoulderPitch', 'LShoulderRoll', 'LShoulderPitch', 'RHipRoll',
                 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'LHipRoll', 'LHipPitch',
                 'LKneePitch', 'LAnklePitch', 'LAnkleRoll']
        angles = [[-0.3], [0.4], [1.0], [1.0], [0.0], [-0.4, -0.2], [0.95, 1.5], [-0.55, -1],
                  [0.2], [0.0], [-0.4], [0.95], [-0.55], [0.2]]
        times = [[0.5], [0.5], [0.5], [0.5], [0.5], [0.4, 0.8], [0.4, 0.8], [0.4, 0.8],
                 [0.4], [0.5], [0.4], [0.4], [0.4], [0.4]]

        self.proxy.angleInterpolation(names, angles, times, True)

        self.proxy.angleInterpolation(['RShoulderPitch', 'RHipPitch', 'RKneePitch',
                                         'RAnklePitch', 'LShoulderPitch'],
                                        [1.0, -0.7, 1.05, -0.5, 0.2],
                                        [[0.1], [0.1], [0.1], [0.1], [0.1]], True)

        self.proxy.angleInterpolation(['RHipPitch', 'RKneePitch', 'RAnklePitch'],
                                        [-0.5, 1.1, -0.65],
                                        [[0.25], [0.25], [0.25]], True)

    def LeftKick(self):
        self.proxy.setFallManagerEnabled(False)
        names = ['LShoulderRoll', 'LShoulderPitch', 'RShoulderRoll', 'RShoulderPitch', 'LHipRoll',
                 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipRoll', 'RHipPitch',
                 'RKneePitch', 'RAnklePitch', 'RAnkleRoll']
        angles = [[0.3], [0.4], [-0.5], [1.0], [0.0], [-0.4, -0.2], [0.95, 1.5], [-0.55, -1],
                  [-0.2], [0.0], [-0.4], [0.95], [-0.55], [-0.2]]
        times = [[0.5], [0.5], [0.5], [0.5], [0.5], [0.4, 0.8], [0.4, 0.8], [0.4, 0.8],
                 [0.4], [0.5], [0.4], [0.4], [0.4], [0.4]]

        self.proxy.angleInterpolation(names, angles, times, True)

        self.proxy.angleInterpolation(['LShoulderPitch', 'LHipPitch', 'LKneePitch', 'LAnklePitch'],
                                        [1.0, -0.7, 1.05, -0.5],
                                        [[0.1], [0.1], [0.1], [0.1]], True)
        self.proxy.angleInterpolation(['LHipPitch', 'LKneePitch', 'LAnklePitch'],
                                        [-0.5, 1.1, -0.65],
                                        [[0.25], [0.25], [0.25]], True)