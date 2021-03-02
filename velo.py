from __future__ import division, print_function
from tfmini import TFmini
import pyttsx3
import time

# Voice Thingy
engine = pyttsx3.init()
engine.startLoop(False)
engine.say("Program initiated Velo at your service")
engine.iterate()
while engine.isBusy():
    time.sleep(0.05)
# What to do with Taller or shorter road bikers
# STEEP ROADS?!

# t= TFmini('/dev/tty.usbserial-A506BOT5',mode=TFmini.STD_MODE)
tf = TFmini('/dev/ttyS0', mode=TFmini.STD_MODE)
print('=' * 25)
print("\a")
try:
    print('=' * 25)
    expectedDistance = tf.read()
    count = 0
    Sumofcurrentdistances = 0
    Avg = 0
    while True:
        currentdistance = tf.read()

        if currentdistance:
            print('Distance: ' + str(currentdistance))
        else:
            print('No valid response')
            continue

            engine.say("Oi! Move it!")
        time.sleep(2)

        # Finding the average for the base to act as expectedvalue
        count = count+1
        if count % 30 == 0:
            print("resetting base")
            expectedDistance= currentdistance


        # Sumofcurrentdistances = Sumofcurrentdistances + currentdistance
        # Avg =  Sumofcurrentdistances / count
        # expectedDistance = Avg

        # The Base value: Distance between lidar and road
        # If base= {0.45,049}: engine.sleep

        # expectedDistance = 0.47
        difference = currentdistance - expectedDistance

        roadCondition = "Normal"

        # finding if bump or dip
        if difference > 0:
            roadCondition = "Dip"
        elif difference < 0:
            roadCondition = "Bump"

        # Calculating absV to determine Bump and Dip levels
        absDiff = abs(difference)

        Level0 = 0.025
        Level1 = 0.05
        Level2 = 0.1
        Level3 = 0.15

        if absDiff < Level0:
            print("Fine/Safe")
        elif absDiff > Level0 and absDiff < Level1:
            print("level 1 Min danger : " + roadCondition)
            engine.say("L1 "+ roadCondition+" Minor" )
        elif absDiff > Level1 and absDiff < Level2:
            print("level 2 dip Min danger : " + roadCondition)
            engine.say("L2 "+ roadCondition+" Caution" )
        elif absDiff > Level2 and absDiff < Level3:
            print("Danger Steer Clear Unsafe : " + roadCondition)
            engine.say("L3 "+ roadCondition+" Danger" )
        elif absDiff > Level3:
            print("VERY DANGEROUS MOVE AWAY NOW : " + roadCondition)
            engine.say("L4 "+ roadCondition+" Stop Now " )

        #     engine.say ("DANger DANgER!!!")
        # print(dif)
        # elif d < base:
        #     print("bump")
        #     engine.say("Speed Bump Ahoy!")

except KeyboardInterrupt:
    engine.say("Buh BYE!")

    tf.close()

engine.endLoop()
