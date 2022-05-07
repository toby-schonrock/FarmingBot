import discord
import os
from discord.utils import get
import asyncio
from datetime import datetime
from pynput import keyboard, mouse
import time
import cv2

path = "C:/Users/tobia/AppData/Roaming/.minecraft/Skyblock/screenshots/"

farming = False

# key control stuff
keyboard_ = keyboard.Controller()
key = keyboard.Key
mouse_ = mouse.Controller()
button = mouse.Button

class avg:
    def __init__(self):
        self.recents = [0.5, 0.5, 0.5, 0.5]
        self.pos = 0

    def new(self, result):
        self.recents[self.pos] = result
        self.pos = (self.pos + 1) % 4
        # print(str(self.recents) + str(sum(self.recents) / 3))
        return sum(self.recents) / 4

async def screenshot(message, user):
    keyboard_.press(key.f2)
    keyboard_.release(key.f2)
    await asyncio.sleep(2)
    files = os.listdir(path)
    if len(files) == 0:
        await message.send("Screenshot failed. Farming disabled")
        farming = False
    elif len(files) == 1:
        await user.send("Got one!")
        os.replace(path + files[0], "./screen.png")
        await user.send(file=discord.File("./screen.png"))
    else:
        await user.send("Err have all this") # should never happen just for security n shit
        for x in range(len(files)):
            os.replace(path + files[x], "./screen.png")
            await user.send(file=discord.File("./screen.png"))

async def farm():
    global farming
    while farming:
        mouse_.press(button.left)
        keyboard_.press("a")
        keyboard_.press("w")
        await asyncio.sleep(17)
        keyboard_.release("w")
        mouse_.release(button.left)
        keyboard_.press("s")
        await asyncio.sleep(0.5)
        keyboard_.release("a")
        mouse_.press(button.left)
        keyboard_.press("d")
        await asyncio.sleep(17)
        keyboard_.release("d")
        mouse_.release(button.left)
        keyboard_.press("a")
        await asyncio.sleep(0.5)
        keyboard_.release("s")
        keyboard_.release("a")

def farmCheck():
    image = cv2.imread("./last.png")
    rows, cols, channels = image.shape
    count = 0

    for x in range(rows):
        for y in range(cols):
            pixel = image[x, y]
            count += int(pixel[1] > pixel[0] and pixel[1] > pixel[2])

    return count / (rows * cols)

client = discord.Client()
clientID = 858513869484064768
userID = 441352696495341579
user = None

@client.event
async def on_ready():
    global farming
    global user
    user = await client.fetch_user(userID) #735624840387493948
    farmAVG = avg()

    while True:
        if farming:
            keyboard_.press(key.f2)
            keyboard_.release(key.f2)
            await asyncio.sleep(2)
            files = os.listdir(path)
            if len(files) == 0:
                await user.send("Screenshot failed. Farming disabled")
                farming = False
            else:
                os.replace(path + files[0], "./last.png")
                farmstat = farmAVG.new(farmCheck())
                if farmstat < 0.4:
                    farming = False
                    await user.send("farmAVG = " + str(farmstat))
                    await user.send(file=discord.File("./last.png"))
                    await user.send("Big no no, farming has stopped")
        await asyncio.sleep(10)

@client.event
async def on_message(message):
    global farming
    global user

    if message.author.id == clientID:
        return

    if "go" in message.content.lower():
        if farming:
            await user.send("Farming is already True")
        else:
            await user.send("Farming has begun :)")
            await user.send("https://tenor.com/9fNX.gif") # dancing gorl happy times
            farming = True
            await farm()
        return

    if "stop" in message.content.lower():
        await user.send("Farming has been halted")
        farming = False
        return

    if "screen" in message.content.lower():
        if farming:
            await user.send("Last image (because farming)")
            await user.send(file=discord.File("./last.png"))
        else:
            await screenshot(message, user)
        return

client.run("ODU4NTEzODY5NDg0MDY0NzY4.YNfPWA.JwM-ECE3OWyCFo8ptXIgHBpzVSM")
