import sys
import threading


class BluetoothRanger(threading.Thread):
    def __init__(self,_tags,_threshold,_setFunc,_btBuffer):
        self.tags = _tags
        self.rssi = {}
        self.thres = _threshold
        self.setFunc = _setFunc
	self.buffer = _btBuffer

    def personInRange(self):
        for tag in self.tags:
            if (self.rssi[tag] > self.thres):
                return True
        return False

    def run(self):
        try:
            while True:
                line = self.buffer.readline()
                if (line[0] == '>'): # new HCI Event
                    if (line[-2:-1] == "26"):
                        # parse data for plen == 26
			print("Parsing data for plen 26")
                        line = self.buffer.readline() # get to address line
                        address = line[0:17] # TODO: parse out address
                        if (address in self.tags):
                            for i in range(8):
                                line = self.buffer.readline()
                                rssi = int(line[11:]) # TODO: parse out rssi

                            # data has been gathered
                            self.rssi[address] = rssi
                        else:
                            break # data was for a different device, so pass
                    else:
                        # parse data for plen == 30
			print("Parsing data for plen 30")
#                        for i in range(5):
 #                           line = self.buffer.readline()
  #                      address = line # TODO: parse out address
#                        if (address in self.tags):
# 	                        for i in range(3):
#                                line = self.buffer.readline()
#                                rssi = line # TODO: parse out rssi

                            # data has been gathered
#                            self.rssi[address] = rssi
                    self.setFunc(self.personInRange())
        except:
            print("ERROR, exiting")
