import smbus
import time
import os
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)

# Set PPM limit variable to whatever would be an alarm for you
# For Uncalibrated sensors, use your better judgement or get it calibrated (390 is a fresh air outdoor baseline, depending on area)
# My system registers car exhaust at about 1000 and Fresh air at around 390 after calibration. I've set 500 as an alarm (Baseline + 100 PPM).
# Possible future enhancement, set up a baseline on boot, then throw an alarm for a significant positive deviation from that baseline?
limit_ppm = 500

# Set up GPIO and pull Alarm Low and Silent Warning High
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.output(2,GPIO.LOW)
GPIO.output(3,GPIO.HIGH)

# Begin the Loop!
while (1):

  # ADC121C_MQ9 address, 0x50(80)
  # Read data back from 0x00(00), 2 bytes
  data = bus.read_i2c_block_data(0x50, 0x00, 2)

  # Convert the data to 12-bits and then to ppm
  raw_adc = (data[0] & 0x0F) * 256 + data[1]
  ppm = (1000.0 / 4096.0) * raw_adc + 10
  # Testing: Output data to screen
  print "Carbon Monoxide Concentration : %.2f ppm" %ppm

  #Set up Alarm loop to pull Alarm high and Silent low, but only while PPM exceeds set limit
  if ppm > limit_ppm:
    GPIO.output(2,GPIO.HIGH)
    GPIO.output(3,GPIO.LOW)
    # Testing: Write alarm status
    print "Alarm is ON"
  else:
    GPIO.output(2,GPIO.LOW)
    GPIO.output(3,GPIO.HIGH)
    # Testing: Write alarm status
    print "Alarm is OFF"
  sleep(5)
