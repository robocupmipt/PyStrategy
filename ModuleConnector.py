import sys
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
        print("Oooops")
        #sys.stderr.write(sys.exc_info()[0])