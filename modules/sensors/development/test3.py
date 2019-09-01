#!/usr/bin/python3
from hx711 import HX711
import sys
import RPi.GPIO as GPIO
import math
import statistics
import os
import datetime


try:
   print("connecting")
   hx711 = HX711(
       dout_pin=5,
       pd_sck_pin=6,
       channel='A',
       gain=64
   )
   print("resetting")
   result =hx711.reset()   # Before we start, reset the HX711 (not obligate)
   if result:
       print("success")
   else:
       print("failure")
       raise ValueError("")


   print("connected")
   while(True):
       measures = hx711.get_raw_data()


       mea=sorted(measures)[2]/10000
       mea=int(mea)
       #val=math.floor(  math.log(abs(measures[0]))*10.0  )
       val=measures
       print(str(mea) + "\t" + str(val) +  "\t\t\t"+str(datetime.datetime.now()))
       print("█"*(int(mea/5)))
finally:
   GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
   print("cleaning up")