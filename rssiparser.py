import os
import threading


class BluetoothRanger(threading.Thread):
    def __init__(self,_tags,_threshold):
        super(BluetoothRanger, self).__init__()
        #state variable intialization
        self.tags = _tags
        self.rssi = {}
        self.thres = _threshold
        self.in_range = False
        self.buffer = os.popen("sudo hcidump & sudo hcitool lescan --duplicates")

    def personInRange(self):
        for tag in self.tags:
            if (self.rssi[tag] > self.thres):
                return True
        return False

    def run(self):
        while True:
            #print("waiting for line...")
            line = self.buffer.readline()
            if (line[0] == '>'): # new HCI Event
                if (line[-3:-1] == "26"):
                    #print("Parsing data for plen 26\n")
                    # parse data for plen == 26
                    i=0
                    address = False
                    RSSI = False
                    while (i<10 and (not address or not RSSI)):
                        line = self.buffer.readline().strip()
                        #print("Waiting for data: "+line)
                        if (line.find("bdaddr") != -1):
                            address = line[7:24]
                        if (line.find("RSSI:") != -1):
                            RSSI = int(line[6:])
                        i += 1
                    #print("Address: "+str(address))
                    #print("--RSSI: "+str(RSSI))
                    if (address in self.tags and RSSI):
                        # only update data if the data is for an iTag
                        #print("Updating data")
                        self.rssi[address] = RSSI
                        self.in_range =self.personInRange()
                    else:
			pass
                        #print("Different device, or RSSI not found")
