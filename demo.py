import random
import time
import KickClass as k

light = k.KickLight()

# Give it a new number each time to show it changing. Needs to be two bytes. Still figuring this one out.
light.colortemp(random.randrange(650,653))

time.sleep(2)

# Range is 0-255 (one byte)
light.brightness(125)

# Being sent: sending "524c00000000000306003078" ('RL', '\x00\x00\x00\x00', '\x00\x03', '\x06', '0x9b')

# Set the buttons of the kick to be preset mode demos. It's back to normal on a reset.
light.buttonmode(2)
