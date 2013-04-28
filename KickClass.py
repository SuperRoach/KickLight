# The Kick light - Python interface to control it via the Wireless api.
#
# Before using this class, it's currently required for you to connect
# your kick to the device running this, using AD-HOC. If the connection drops,
# you have Wi-Fi drivers that do not support AD-HOC mode.
#
# Changing colour will have no effect unless the light is visible.

import binascii
import socket
import struct
import sys


# HOW IT WORKS:

# A packet is sent containing:
# Marker Address Length Command Data
# All of these are fixed except the last three.
# - The length should be split into a "high and low byte"
# - The command is always one byte.
# - The data is usually one or two bytes.

# Source of knowledge: Page 2 of the Kick API:
# https://docs.google.com/document/d/1TnYrs8QB-Gi5ReVWuMrgrOhmeV3k2KEGuIERLUjjRqI/edit?pli=1

class KickLight:
    def __init__(self):

        # The following data does not change between each command.
        self.Marker = 'RL'
        self.SlaveAddress = '\x00\x00\x00\x00'
        self.IpAddress = "169.254.255.255"
        self.live = False
        if self.live:
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.ServerAddress = ('169.254.255.255', 8080)
            self.Sock.connect(self.ServerAddress)
            print "Live, connected."
        else:
            print "Not live - Just pretending to send data."
        

    def __del__(self):
        print >>sys.stderr, 'closing socket'
        self.Sock.close()
        
    def colortemp(self, temp):
        # Sets the color temperature in Kelvin.
        # Typical values are between 2500 and 10000.

        # This is the data command to change the colour temp.
        self.Command = '\x05'

        #self.Data = '\x1000'   # 200 in int
        self.Data = hex(temp)
        self.SendCommand()
        return 'color temp %s is %r in hex.' % (temp, self.Data)

    def brightness(self, intensity):
        # Set's the brightness level

        self.Command = '\x06'
        self.Data = hex(intensity)
        self.SendCommand()

    def SendCommand(self):
        # You need to set data before this at the moment.

        # Hardcoded. 
        self.Length = Length = '\x00\x03' # High byte plus length of data +1 for the command.


        #self.Length = Length = len(self.Data) # It should be high byte and low byte. Data Length + 1 for command
        #self.Length = '\x00', str(len(self.Data) + 1)
        #self.Length = '\x00', str(1+1)
        
        print 'The length of the data is apparently %s' % (str(len(self.Data) + 1))
        values = (self.Marker, self.SlaveAddress, self.Length, self.Command, self.Data)

        # Am I correctly setting the length? (third value should be two bytes.)
        Packer = struct.Struct('2s 4s 2s 2s 2s')
        PackedData = Packer.pack(*values)
        
        try:
            
            # Send data
            print >>sys.stderr, 'sending "%s"' % binascii.hexlify(PackedData), values
            if self.live:
                self.Sock.sendall(PackedData)
                

        finally:
            print >>sys.stderr, 'Sent.'
            #self.Sock.close()
