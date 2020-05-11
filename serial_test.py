# -*- coding: utf-8 -*-
"""
Serial_test.py

Sends commands to Arduino Uno via serial port to control a drone
using the nRF24L01 wireless boards.

The i,k control elevator, and j,l control aileron (forward/reverse and left/right)
and the w,s keys control throttle, and the a,d, keys control the rudder (yaw),
r to reset controls to initial value.

This uses the msvcrt library, so it only works under Windows. 

Created on Sun Feb 21 00:17:38 2016

@author: perrytsao
"""
import serial, time, msvcrt, pdb

# COM setting.
COM = 'COM3'

# Resolution.
tg=50
ag=100
eg=100
rg=100

# Initial value.
throttle=1000
aileron=1500
elevator=1500
rudder=1500 # yaw, rotates the drone.

# Bounds.
CONTROL_MAX = 2000
CONTROL_MIN = 1000


# Gyroscope auto-calibration.
def auto_calibrate():
    throttle=1000
    aileron=1000
    elevator=1000
    rudder=1000
    command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
    arduino.write(bytes(command+"\n", 'utf-8'))
    time.sleep(4)

    aileron=1500
    elevator=1500
    rudder=1500
    command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
    arduino.write(bytes(command+"\n", 'utf-8'))


# Adjust throttle a bit to make sure drone has been connected (test connection).
# The drone's onboard blue LED should go solid after this.
def test_connection():
    aileron=1500     # Recenter.
    elevator=1500
    rudder=1500

    for _ in range(2):
        throttle=1020
        command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
        arduino.write(bytes(command+"\n", 'utf-8'))
        time.sleep(0.5)

        throttle=1000
        command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
        arduino.write(bytes(command+"\n", 'utf-8'))
        time.sleep(0.5)


# Main loop.
try:
    arduino = serial.Serial(COM, 115200, timeout=.01)
    time.sleep(1) #give the connection a second to settle
    #arduino.write("1500, 1500, 1500, 1500\n")

    # Initial actions.    
    print("\nCalibrating gyroscope...")
    auto_calibrate()
    
    print("Testing connection...\n")
    test_connection()

    while True:
        
        data = arduino.readline()
        if data:
            #String responses from Arduino Uno are prefaced with [AU]
            print("[AU]:", data)
            
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27: #ESC
                print("[PC]: ESC exiting")
                break
            elif key == 13: #Enter
                #select()
                print("[PC]: Enter")
            elif key == 119 and throttle < CONTROL_MAX: #w
                throttle+=tg
            elif key == 97 and rudder > CONTROL_MIN: #a
                rudder-=rg        
            elif key == 115 and throttle > CONTROL_MIN: #s
                throttle-=tg
            elif key == 100 and rudder < CONTROL_MAX: #d
                rudder+=rg
            elif key == 107 and elevator > CONTROL_MIN: #k
                elevator-=eg
            elif key == 105 and elevator < CONTROL_MAX: #i
                elevator+=eg
            elif key == 108 and aileron < CONTROL_MAX: #l
                aileron+=ag
            elif key == 106 and aileron > CONTROL_MIN: #j
                aileron-=ag
            
            # Throttle setting using number keys.
            elif key == 96: #`
                throttle = 1000
            elif key == 48: #0
                throttle = 2000
            elif key in range(49, 58): # Between 1-9.
                throttle = 1000 + 100*(key-48)  
            
            elif key == 103: #g, calibrate gyroscope
                throttle=1000
                aileron=1000
                elevator=1000
                rudder=1000
            elif key == 114: #r, Reset all controls
                throttle=1000
                aileron=1500
                elevator=1500
                rudder=1500               
            
            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            # print("[PC]:", command)

            # Must replace with array of bytes instead of string.
            arduino.write(bytes(command+"\n", 'utf-8'))

finally:
    # close the connection
    arduino.close()
    # re-open the serial port which will also reset the Arduino Uno and
    # this forces the quadcopter to power off when the radio loses conection. 
    arduino=serial.Serial(COM, 115200, timeout=.01)
    arduino.close()
    # close it again so it can be reopened the next time it is run.  
