# -*- coding: utf-8 -*-
"""
Serial_test.py

Sends commands to Arduino Uno via serial port to control a drone
using the nRF24L01 wireless boards.

The i,k control elevator, and j,l control aileron (forward/reverse and left/right)
and the w,s keys control throttle, and the a,d, keys control the rudder (yaw)

This uses the msvcrt library, so it only works under Windows. 

Created on Sun Feb 21 00:17:38 2016

@author: perrytsao
"""
import serial, time, msvcrt, pdb

COM = 'COM4'

# Initial value.
throttle=1000
aileron=1500
elevator=1500
rudder=1500 # yaw, rotates the drone

# Resolution.
tg=10
ag=50
eg=50
rg=50
try:
    arduino=serial.Serial(COM, 115200, timeout=.01)
    time.sleep(1) #give the connection a second to settle
    #arduino.write("1500, 1500, 1500, 1500\n")
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
            elif key == 119: #w
                throttle+=tg
            elif key == 97: #a
                rudder-=rg         
            elif key == 115: #s
                throttle-=tg
            elif key == 100: #d
                rudder+=rg
            elif key == 107: #k
                elevator-=eg
            elif key == 105: #i
                elevator+=eg
            elif key == 108: #l
                aileron+=ag
            elif key == 106: #j
                aileron-=ag
            elif key == 99: #c, Reset all controls
                throttle=1000
                aileron=1500
                elevator=1500
                rudder=1500               
            
            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            print("[PC]:", command)
            # pdb.set_trace()

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
