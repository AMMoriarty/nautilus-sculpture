#Nautilus 2015-2016
#by Cassandra Phillips-Sears
#Runs lights, sounds, touch sensor for interactive nautilus sculpture 
#TY to Nick, Abe, David, FABLab & HATCH folks, TonyDiCola NeoPixel Library

import time
from neopixel import *
import RPi.GPIO as GPIO
import os, random

#NeoPixel LED Strip Config
LED_COUNT = 60 #number of LED pixels
LED_PIN = 18 #GPIO pin connected to pixels (must support PWM!)
LED_FREQ_HZ = 800000 #LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 #DMA channel to use for generating  signal (try 5)
LED_INVERT = False #True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest

#set BCM mode on GPIO
GPIO.setmode (GPIO.BCM)

#setup listening pin 23
padPin = 23
GPIO.setup(padPin, GPIO.IN)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

#define random sound player
def rndWav ():
   randomfile = random.choice(os.listdir("/home/pi/Music/nautilus"))
   file = '/home/pi/Music/nautilus'+ randomfile
   os.system ('omxplayer' + file)

# Main NeoPixel program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

#set initial state of touch sensor
alreadyPressed = False

while True:
	padPressed = GPIO.input(padPin)
	
	if padPressed and not alreadyPressed:
		#test
		print 'press Ctrl-C to quit.'
		
        while True:
		# Color wipe animations.
		colorWipe(strip, Color(144, 212, 195))  #Light blue wipe
		colorWipe(strip, Color(13, 77, 94))  #Dk Turquoise wipe
		colorWipe(strip, Color(53, 150, 62)) #Navyblue wipe
		colorWipe(strip, Color(53, 93, 150)) #Seafoam wipe
		colorWipe(strip, Color(43, 43, 179)) #Robinegg wipe
		colorWipe(strip, Color(0, 50, 50)) #Turquoise wipe
		colorWipe(strip, Color(71, 122, 20)) #Indigo wipe
		# Theater chase animations.
		#theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		#theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		#rainbow(strip)
		#rainbowCycle(strip)
		#theaterChaseRainbow(strip)

                #play random Wav file
		rndWav ()
	
	alreadyPressed = padPressed
	time.sleep(0.1)
