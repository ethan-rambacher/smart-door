import sys

threshold = -70 # RSSI threshold
inRange = False # is someone within range of the hub?


try:
    while True:
        line = sys.stdin.readline()
        if (line[0] == '>'): # new HCI Event


class BluetoothRanger(threading.Thread):
    def __init__(self,_tags,_threshold,_setFunc):
        self.tags = _tags
        self.rssi = {}
        self.thres = _threshold
        self.setFunc = _setFunc
        
    def personInRange(self):
        for tag in self.tags:
            if (self.rssi[tag] > self.thres):
                return True
        return False
        
    def run(self):
        try:
            while True:
                line = sys.stdin.readline()
                if (line[0] == '>'): # new HCI Event
                    if (line[-2:-1] == "26"):
                        # parse data for plen == 26
                        for i in range(5):
                            line = sys.stdin.readline() # get to address line
                        address = line # TODO: parse out address
                        if (address in self.tags):
                            for i in range(9):
                                line = sys.stdin.readline()
                                rssi = line # TODO: parse out rssi
                                
                            # data has been gathered
                            self.rssi[address] = rssi
                        else:
                            break # data was for a different device, so pass
                    else:
                        # parse data for plen == 30
                        for i in range(5):
                            line = sys.stdin.readline()
                        address = line # TODO: parse out address
                        if (address in self.tags):
                            for i in range(3):
                                line = sys.stdin.readline()
                                rssi = line # TODO: parse out rssi

                            # data has been gathered
                            self.rssi[address] = rssi
                    self.setFunc(self.personInRange())
        except:
            print("ERROR, exiting")

br = BluetoothRanger()
br.start()
