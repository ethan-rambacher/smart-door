import os
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
        while True:
	    print("waiting for line...")
            line = self.buffer.readline()
	    print(line)
            if (line[0] == '>'): # new HCI Event
		print(line)
                if (line[-3:-1] == "26"):
                    # parse data for plen == 26
		    print("Parsing data for plen 26\n")
                    line = self.buffer.readline() # get to address line
		    print(line)
                    address = line[0:17]
		    print("Address: "+address)
                    if (address in self.tags):
                        for i in range(8):
                            line = self.buffer.readline()
                            rssi = int(line[11:])

                            # data has been gathered
                        self.rssi[address] = rssi
			print("-RSSI: "+rssi)
	                self.setFunc(rssi)

                    else:
                        break # data was for a different device, so pass
                else:
                    # parse data for plen == 30
		    print("Parsing data for plen 30\n")
#                        for i in range(5):
 #                           line = self.buffer.readline()
  #                      address = line
#                        if (address in self.tags):
# 	                        for i in range(3):
#                                line = self.buffer.readline()
#                                rssi = line

                            # data has been gathered
#                            self.rssi[address] = rssi

current_rssi = 0

def setRSSI(_rssi):
    current_rssi = _rssi
    print("RSSI="+current_rssi)

# MAIN #
bt_buffer = os.popen("sudo hcidump & sudo hcitool lescan --duplicates")
br = BluetoothRanger({"FF:FF:80:00:86:56"},-70,setRSSI,bt_buffer)

br.run()
