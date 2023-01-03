# Coded with <3 by Stephen Cupitt
import serial
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client

####### CONFIG VARIABLES #######
# Define the number of faders on your console
numFaders = 48
# Specify your OSC client
client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
# Specify an offset for your submasters
subOffset = 0

# Global Variables
data = []


def main():
    # Open a serial port
    ser = serial.Serial("/dev/tty.usbserial", baudrate=57600, timeout=1)
    while True:
        # Read a DMX-512 frame
        data = ser.read(512)

        for i in range(numFaders):
            print("[-] :: Fader " + str(i) + " :: Parameter " + data[i])
            build_message(i, data[i])

        # Add a delay of 1 second between each iteration
        time.sleep(1)
    # Close the serial port
    ser.close()


def build_message(fader, param):
    # Build the OSC message
    faderName = "/eos/key/fader_" + str(fader)
    msg = osc_message_builder.OscMessageBuilder(address=faderName)
    msg.add_arg(param)
    msg = msg.build()

    # Send the OSC message
    client.send(msg)
    print("[-] Completed build_message")


if __name__ == "__main__":
    main()
