University of Pennsylvania, ESE 5190: Intro to Embedded Systems, Lab 1

    sudong wang
    sudong@seas.upenn.edu
    Tested on: DELL XPS13 9360 

# 5190 LAB1
# overview
The main object of the first lab is to get familiar with the microcontroller RP2040 which is designed and released by the team behind Rasberry Pi. In this lab, I learned to use the sensor to detect the distance, the environment light, and motion. With the help of python, we can directly test the sensor with the flashing LED on the main board. Next, I learned how to use RP2040 to emulate a mouse and keyboard through the 'HID' interface. 

# 3.2 make a light sensor to a firefly
The basic logic is to let the sensor detect the change of the brightness of the environmental light source. To accomplish that goal, I first import the sensor, and enable it to sense color where c in the r g b c represent the brightness of the light source. Then I set the variable Clast which is firstly define to be 0. After the sensor detect the light source, it will report a c (brightness value ) to be compared with clast which is equal to the last c detected. If c (current brightness) is bigger than clast, we can claim that the light source become brighter, so the LED light on the main board will blink. 
![b7a381d05b4f9ab62ebb1c810403bca2](https://user-images.githubusercontent.com/113209201/192015355-bbc4f5b2-f31a-44f5-9a19-beaaebc7c643.gif)

```
#section3
import board
import busio
import adafruit_apds9960.apds9960
import time
import neopixel
import digitalio
import usb_hid
import analogio
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
clast=0
while True:
    r, g, b, c = sensor.color_data
    print(c)
    
    if c > (clast+100):
        pixels.fill((255, 255, 255))
        
    if c < (clast-100):
        pixels.fill((255, 255, 255))
        
    else:
        pixels.fill((0, 0, 0))
        
    clast=c
    time.sleep(0.01)
```

# 4.4 make a custom real-time visualizer
The basic logic is to make a visualizer that can read and write down what you do through a sensor. We used a light sensor and a motion sensor to detect the motion and light source, and 'HID' interface to writing down the result through direct keyboard input. The program will firstly write down: test guesture first, and start a while loop to test the gesture. We expect the user to detect the gestures equal to 1,2,3, and 4 which represent up down left right. The keyboard will output the result of gesture detection such as going up if the gesture is 1. Once the four gesture detection is completed, it will continue to test the brightness of the lightsource. The logic is same as 3.2, if the c is bigger than clast,the keyboard will type going bright, and if c is smaller than clast, it will type going dark. After four light detection, the program is sleeped with typing done on the screen. 
![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/113209201/192026257-d1908270-a030-4e4b-9374-305aed74b280.gif)


```
import board
import busio
import time
import adafruit_apds9960.apds9960
import neopixel

import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#i2c = board.STEMMA_I2C()
i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True
sensor.enable_gesture = True
sensor.color_integration_time = 10

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

mouse = Mouse(usb_hid.devices)

keys_pressed = [Keycode.O, Keycode.BACKSPACE]
control_key = Keycode.SHIFT
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

c_last = 0
while True:
    time.sleep(2)
    info = keyboard_layout.write("Test gesture first!\n")
    i = 0
    while i <= 3:
        gesture = sensor.gesture()
        if gesture == 1:
            info = keyboard_layout.write("Going up!\n")
            time.sleep(0.1)
            i += 1
        if gesture == 2:
            info = keyboard_layout.write("Going down!\n")
            time.sleep(0.1)
            i += 1
        if gesture == 3:
            info = keyboard_layout.write("Going left!\n")
            time.sleep(0.1)
            i += 1
        if gesture == 4:
            info = keyboard_layout.write("Going right!\n")
            time.sleep(0.1)
            i += 1
    time.sleep(1)
    info = keyboard_layout.write("Then test brightness!\n")
    i = 0
    while i <= 3:
        r, g, b, c = sensor.color_data
        print(c)
        if c >= (c_last+200):
            info = keyboard_layout.write("Going bright!\n")
            time.sleep(.5)
            i += 1
        elif c <= (c_last-100):
            info = keyboard_layout.write("Going dark!\n")
            time.sleep(.5)
            i += 1
        c_last = c
    info =keyboard_layout.write("Done\n")
    break
   ```
   here is the graph of my embedded system from 4.4 and the raw signal include change of light and gestures, and the processed signal also include the keyboard typing. 
   
show how the components interact:
    ![e00f6acf933ff34fb779e203cb21e12](https://user-images.githubusercontent.com/113209201/192077685-969014e3-36d8-43ff-90ad-818e5939694f.jpg)

