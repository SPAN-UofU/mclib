import socket
import time
import struct
import sys
import numpy as np

class KS53230A:
    PORT = 5025

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        self.f = self.s.makefile("rb")

        #RESET
        self.s.send("*RST\n")
        self.s.send("*CLS\n")

        self.s.send("FORM:DATA ASC\n")

    def confChannel1(self):
        self.s.send("CONF:FREQ\n")

    def confChannel2(self):
        self.s.send("CONF:FREQ ,(@2)\n")

    def setInitiate(self):
        self.s.send("INIT\n")

    def setTriggerSource(self, source="IMM"):
        self.s.send("TRIGGER:SOURCE %s\n"%(source,))

    def setTriggerCount(self, count="MIN"):
        self.s.send("TRIGGER:COUNT %s\n"%(count,))

    def setSampleCount(self, count="MAX"):
        self.s.send("SAMP:COUN %s\n"%(count,))

    def getMeasurements(self, channel=1):
        self.s.send("MEAS:FREQ? MAX,DEF,(@%s)\n"%channel)

        time.sleep(1)
        str = self.s.recv(1000)

        return float(str)

if __name__ == "__main__":

    ip = "10.42.0.111"
    samples = int(sys.argv[1])

    ea = KS53230A(ip)

    chan1 = []
    chan2 = []
    for i in range(samples):
        chan1.append(ea.getMeasurements(1))
        chan2.append(ea.getMeasurements(2))
        
        print str(chan1[-1]) + " " + str(chan2[-1]) + " " + str(abs(chan1[-1]-chan2[-1]))
        
    delta = np.array(chan1) - np.array(chan2)
    print "Mean Channel 1 " + str(np.mean(chan1)) + " Hz"
    print "Mean Channel 2 " + str(np.mean(chan2)) + " Hz"
    print "Mean: "      + str(np.mean(delta)) + " Hz"
    print "STD: "       + str(np.std(delta))  + " Hz"

