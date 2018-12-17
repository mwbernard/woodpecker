# Code for a woodpecker robot using CPX with Crickit, a Solenoid, and a pan/tilt servo motor
# Project for Creative Technologies with Phil Van Allen
# Martin Bernard

from varspeed import Vspeed
from adafruit_crickit import crickit
import board

from busio import I2C
import board
import time
import random
import audiobusio
import array
import math

# create a Vspeed object 
servo1_position = Vspeed(False) # get decimal values for the servo
servo2_position = Vspeed(False) # get only integer values for the NeoPixels

# set up solenoid drive
crickit.drive_1.frequency = 1000

# set up mic
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth = 16)
samples = array.array('H', [0] * 200)
mic.record(samples, len(samples))

last_magnitude = 0

# sequences for random pecks 
sequences = [
            [(75,50)],
            [(80,50)],
            [(65,50)],
            [(90,50)],
            [(95,50)],
            [(100,50)],
            [(105,50)],
            [(110,50)],
            [(115,50)]
]

current_sequence = random.choice(sequences)
last_sequence = current_sequence

# Returns the average
def mean(values):
    return sum(values) / len(values)
 
# Audio root-mean-square
def normalized_rms(values):
    minbuf = int(mean(values))
    return math.sqrt(sum(float(sample-minbuf)*(sample-minbuf) for sample in values) / len(values))

# bird pauses and drums
def drum():

    # movement that shows acknowledgement of the knocking by the user and positions the bird
    crickit.servo_2.angle = 140
    time.sleep(1)
    crickit.servo_1.angle = 40
    time.sleep(.2)
    crickit.servo_2.angle = 140
    time.sleep(.2)
    crickit.servo_2.angle = 169

    # solenoid pecks
    for i in range(0,2):
        for j in range (0,20):
            crickit.drive_1.fraction = 0.0
            time.sleep(0.05)
            crickit.drive_1.fraction = 1.0

        time.sleep(.25)

# main function
while True:
    
    # get sound level
    mic.record(samples, len(samples))   
    magnitude = normalized_rms(samples)
    
    # unless someone knocks loud enough, the bird will do a random pecking routine
    if magnitude < 5000:
        # if sensor_read value just transitioned from below to above 512, initialize the sequences
        if last_magnitude >= 5000:
            servo1_position.sequence_reset()
            
        last_magnitude = magnitude
        
        value, running, changed = servo1_position.sequence(current_sequence, False)
        if running:
            crickit.servo_1.angle = value
        else:

            ## the sequences were working, but then got all choppy for a reason I couldn't figure out,
            ## so for just this section I wrote the servo posistions out and used sleeps
            ## if I used the sleeps only in the servo2 sequence, the shaking was not visible,
            ## and there is still time for it to hear the knocking 

            #value, running, changed = servo2_position.sequence([(125,40),(170,100),(165,40)],False)
            #if running:
                #crickit.servo_2.angle = value
            #else:

            crickit.servo_2.angle = 125
            time.sleep(.4)
            crickit.servo_2.angle = 135
            time.sleep(.01)
            crickit.servo_2.angle = 145
            time.sleep(.01)
            crickit.servo_2.angle = 155
            time.sleep(.01)
            crickit.servo_2.angle = 172
            time.sleep(.01)
            crickit.servo_2.angle = 145
            time.sleep(.2)

            servo1_position.sequence_reset()
            current_sequence = random.choice(sequences)
    else:
        
        # if someone knocks loud enough
        drum()
