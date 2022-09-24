'''
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
'''
'''
#section1
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    pixels.fill((255, 0, 0))
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    time.sleep(0.5)
'''

'''
#section 2
i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True
sensor.enable_gesture = True

while True:
    r, g, b, c = sensor.color_data
    print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))

gesture = sensor.gesture()

while gesture == 0:
    gesture = sensor.gesture()
    print('Saw gesture: {0}'.format(gesture))


print(dir(sensor))
'''


#section3
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


'''
#section 4
mouse = Mouse(usb_hid.devices)

i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True


clast=0
while True:
    r, g, b, c = sensor.color_data
    print(c)

    if c > (clast):
        mouse.move(x=20)


    if c < (clast):
        mouse.move(x=-20)

    else:
        mouse.move(x=0)


    clast=c
    time.sleep(0.1)


keyboard = Keyboard(usb_hid.devices)
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

i2c = busio.I2C(board.SCL1, board.SDA1)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_proximity = True
sensor.enable_color = True



clast=0
while True:
    r, g, b, c = sensor.color_data


    if c > (clast):
        key = key_pressed[0]
        keyboard.press


    if c < (clast):
        key





    clast=c
    time.sleep(0.1)
'''

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

