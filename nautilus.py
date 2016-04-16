#Nautilus 2015-2016
#by Cassandra Phillips-Sears
#Runs lights, sounds, touch sensor for interactive nautilus sculpture 
#TY to Nick, Abe, David, Kelly, FABLab & HATCH folks, TonyDiCola NeoPixel Library

import time
from neopixel import *
import RPi.GPIO as GPIO
import os, random
import subprocess

#set BCM mode on GPIO
GPIO.setmode (GPIO.BCM)

#setup listening pin 23
GPIO.setup(23, GPIO.IN)

soundprocess = None

#NeoPixel LED Strip Config
LED_COUNT = 60 #number of LED pixels
LED_PIN = 18 #GPIO pin connected to pixels (must support PWM!)
LED_FREQ_HZ = 800000 #LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 #DMA channel to use for generating  signal (try 5)
LED_INVERT = False #True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def pixelsOff (strip, color, wait_ms=50):
	"""Turn off NeoPixels."""
	for i in range(strip.numPixels()):
      		strip.setPixelColor(i, color)
   		strip.show()
		time.sleep(wait_ms/1000.0)

#define random sound player w subprocess
def callback_first(channel):   #Sound Playback Open
	global soundprocess
	randomfile = random.choice(os.listdir("/home/pi/Music/nautilus/"))
	file = '/home/pi/Music/nautilus/'+ randomfile
	print ("sound starting soon")
	soundprocess = subprocess.Popen(['omxplayer','-o','hdmi',file],stdin=subprocess.PIPE)
	time.sleep(10)
	global soundprocess
	print("Sound Terminate")
	if soundprocess:
		soundprocess.stdin.write('q')
	soundprocess = None
    	#sys.exit("System Exiting")

def main():
	#set initial state of touch sensor
	alreadyPressed = False
		
	while True:
        	padPressed = GPIO.input(23)
        		
        	if padPressed and not alreadyPressed:
            		
            		#miniprompt for user
            		print ('press Ctrl-C to quit.')
            	
            		#play random wav file and lights when pin on, not when pin off
            		try:    
    				GPIO.add_event_detect(23, GPIO.BOTH, callback=callback_first, bouncetime=400)
    				time.sleep(0.1)
    				#starting lights
    				#main NeoPixel Program logic follows
    				# Create NeoPixel object with appropriate configuration.
    				strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    				# Intialize the library (must be called once before other functions).
    				strip.begin()
    				#colors for lights
    				colorWipe(strip, Color(13, 77, 94))  #Dk Turquoise wipe
    				colorWipe(strip, Color(53, 150, 62)) #Navyblue wipe
    				colorWipe(strip, Color(53, 93, 150)) #Seafoam wipe
    				colorWipe(strip, Color(43, 43, 179)) #Robinegg wipe
    				colorWipe(strip, Color(71, 122, 20)) #Indigo wipe
    				#turn off NeoPixels when done
    				pixelsOff(strip, Color(0,0,0)) #all color vals to 0
    			finally:
    				GPIO.cleanup()
    				print('thank you!')
    			#end play wav and lights
    		#end while
    	#end if
	alreadyPressed = padPressed
	print('please touch!')
    #end while
    
#end main

if __name__ == '__main__':
    main()
#end if
