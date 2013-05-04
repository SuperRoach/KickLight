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
        self.SlaveAddress = 0
        self.IpAddress = "169.254.255.255"
        self.live = True
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
        self.Command = 5

        #self.Data = '\x1000'   # 200 in int
        self.Data = temp
        self.SendCommand()
        return 'color temp %s is %r in hex.' % (temp, self.Data)

    def brightness(self, intensity):
        # Sets the brightness level

        self.Command = 6
        self.Data = intensity
        self.SendCommand()

    def rgbtest(self, *args):
        # Sets the RGB - device dependant and not calibrated, for testing only.
        # Takes Three Bytes

        if len(args) == 3:
            self.Command = 1
            self.Data = args
            self.SendCommand()
        else:
            print 'Supply Three bytes for R G B'

    def buttonmode(self, mode):
        # Changes how the buttons on the Kick function
        # 0 = normal
        # 1 = Brightness / Refresh
        # 2 = Demo buttons
        #
        # When powered off, the buttons go back to normal.
        # Sets the brightness level

        self.Command = 10
        self.Data = mode
        self.SendCommand()            


    def SendCommand(self):
        # You need to set data before this at the moment.

        # Hardcoded. 
        #self.Length = Length = '\x00\x02' # High byte plus length of data +1 for the command.

        self.Length = 4
        #self.Length = Length = len(self.Data) # It should be high byte and low byte. Data Length + 1 for command
        #self.Length = len(self.Data)
        #self.Length = '\x00', str(1+1)
        
        #print 'The length of the data is apparently %s' % (len(str((self.Data) + 1)))
        values = (self.Marker, self.SlaveAddress, self.Length, self.Command, self.Data)

        # Am I correctly setting the length? (third value should be two bytes.)
        #Packer = struct.Struct('2s 4s 1h 1i 1i')
        if self.Command == 1: #RGB Test
            Packer = struct.Struct('> 2s i h b 3B')
        elif self.Command == 5: # Colour Temp
            Packer = struct.Struct('> 2s i h b h')
        elif self.Command == 6: # Brightness
            Packer = struct.Struct('> 2s i h b B')
        elif self.Command == 10: # Button function
            Packer = struct.Struct('> 2s i h b B')
            
        PackedData = Packer.pack(*values)
        
        try:
            
            # Send data
            print >>sys.stderr, 'sending "%s"' % binascii.hexlify(PackedData), values
            if self.live:
                self.Sock.sendall(PackedData)
                

        finally:
            print >>sys.stderr, 'Sent.'
            #self.Sock.close()
