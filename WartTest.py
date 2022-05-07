from pynput import keyboard, mouse
import time

keyboard_ = keyboard.Controller()
key = keyboard.Key
mouse_ = mouse.Controller()
button = mouse.Button

def farm():
    keyboard_.press("w")
    time.sleep(1.5)
    keyboard_.release("w")
    mouse_.press(button.left)
    keyboard_.press("d")
    time.sleep(41.8)
    keyboard_.release("d")
    mouse_.release(button.left)
    keyboard_.press("w")
    time.sleep(1.5)
    keyboard_.release("w")
    mouse_.press(button.left)
    keyboard_.press("a")
    time.sleep(41.8)
    keyboard_.release("a")
    mouse_.release(button.left)

time.sleep(2)
while True:
    farm()
