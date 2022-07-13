import RPi.GPIO as GPIO
import time
import sys

seg_pin = [12, 5, 6, 16, 19, 20, 26, 21]

seg = [
    [12, 5, 6, 16, 19, 20],
    [5, 6],
    [12, 5, 16, 19, 26],
    [12, 5, 6, 16, 26],
    [5, 6, 20, 26],
    [12, 6, 16, 20, 26],
    [12, 6, 16, 19, 20, 26],
    [12, 5, 6, 20],
    [12, 5, 6, 16, 19, 20, 26],
    [12, 5, 6, 20, 26]
    ]

def setup():
    GPIO.setmode(GPIO.BCM)
    #touch
    GPIO.setup(17,GPIO.IN)
    #switch
    GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #7seg
    GPIO.setup(seg_pin,GPIO.OUT)
    GPIO.output(seg_pin, GPIO.LOW)

def count():
    GPIO.output(seg_pin, GPIO.LOW)
    prev = 0
    now = 0
    count = 0
    while GPIO.input(27)==0:
        now = GPIO.input(17)
        if now != prev:
            #print("change!!")
            if now == 1:
                count += 1
        #print(now)
        time.sleep(0.1)
        prev = now

    #print("count: ", count)
    GPIO.output(seg[count%10], GPIO.HIGH)
    time.sleep(3)
    #GPIO.output(seg[count%10], GPIO.LOW)
    #GPIO.cleanup()
    return count

def display(content):
    GPIO.output(seg_pin, GPIO.LOW)
    GPIO.output(seg[content.num], GPIO.HIGH)

def end():
    GPIO.cleanup()
