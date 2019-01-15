from ModuleConnector import ModuleConnector


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

