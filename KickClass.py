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


class KickLight:
    def __init__(self):
        self.Marker = 'RL'
        self.SlaveAddress = '\x00\x00\x00\x00'
        self.IpAddress = "169.254.255.255"
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ServerAddress = ('169.254.255.255', 8080)
        self.Sock.connect(self.ServerAddress)

     def __del__(self):
        print >>sys.stderr, 'closing socket'
        self.Sock.close()
        
    def colortemp(self, temp):
        # Sets the color temperature in Kelvin.
        # Typical values are between 2500 and 10000.

        
        self.Command = '\x05'
        #self.Data = '\x1000'   # 200 in int
        self.Data = hex(temp)
        return 'color temp %s is %r in hex.' % (temp, self.Data)

    def SendCommand(self):
        # You need to set data before this at the moment.
        
        self.Length = Length = '\x00\x03' # Low byte plus length of data +1
        # self.Length = '\x00', len(Data) + 1
        values = (self.Marker, self.SlaveAddress, self.Length, self.Command, self.Data)
        
        Packer = struct.Struct('2s 4s 2s 2s 2s')
        PackedData = Packer.pack(*values)
        
        try:
            
            # Send data
            print >>sys.stderr, 'sending "%s"' % binascii.hexlify(PackedData), values
            self.Sock.sendall(PackedData)

        finally:
            print >>sys.stderr, 'Sent.'
            #self.Sock.close()
