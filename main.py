import discord
import os
from discord.utils import get
import asyncio
from datetime import datetime
from pynput import keyboard, mouse
import cv2

path = "C:/Users/tobia/AppData/Roaming/.minecraft/Skyblock/screenshots/"

farming = False

# key control stuff
keyboard_ = keyboard.Controller()
key = keyboard.Key
mouse_ = mouse.Controller()
button = mouse.Button

## screenshot reading shit

startY = 500
height = 1440
startX = 2200
width = 2560

scanwidth = 115
scanheight = 13

data = list(map(int, open("YourIsland.txt", "r").read().split(',')))
clientKey = open("Bot.txt", "r").read()

def find_first(image):
    for y in range(startY, height):
        for x in range(startX, width):
            pixel = image[y, x]
            if pixel[0] == 85 and pixel [1] == 255 and pixel[2] == 85:
                return x, y

def process():
    image = cv2.imread("last.png")
    rows, cols, channels = image.shape
    start = find_first(image)
    for x in range(scanwidth):
        for y in range(scanheight):
            pixel = image[y + start[1], x + start[0]]
            if int(pixel[0] == 85 and pixel[1] == 255 and pixel[2] == 85) != data[x + y * scanwidth]:
                return False
    return True

async def farmcheck(user):
    keyboard_.press(key.f2)
    keyboard_.release(key.f2)
    await asyncio.sleep(2)
    files = os.listdir(path)
    if len(files) == 0:
        await user.send("Screenshot failed. Farming disabled")
        return False
    else:
        os.replace(path + files[0], "./last.png")
        if not process():
            await user.send(file=discord.File("./last.png"))
            await user.send("Big no no, farming has stopped")
            return False
    return True

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

async def farmWart(user):
    global farming
    mouse_.press(button.left)
    while farming:
        # mouse_.press(button.left)
        keyboard_.press("d")
        await asyncio.sleep(41.8)
        keyboard_.release("d")
        # mouse_.release(button.left)
        keyboard_.press("w")
        await asyncio.sleep(1.5)
        keyboard_.release("w")
        # mouse_.press(button.left)
        keyboard_.press("a")
        await asyncio.sleep(41.8)
        keyboard_.release("a")
        # mouse_.release(button.left)
        keyboard_.press("w")
        await asyncio.sleep(1.5)
        keyboard_.release("w")
    mouse_.release(button.left)


async def farmSugar(user):
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

client = discord.Client()
clientID = 858513869484064768
userID = 441352696495341579
user = None

@client.event
async def on_ready():
    global user
    global farming
    user = await client.fetch_user(userID) #735624840387493948

    while True:
        while farming:
            try:
                farming = await farmcheck(user)
            except Exception as e:
                farming = False
                await user.send("Try except failure" + str(e))
                await user.send(file=discord.File("./last.png"))
            await asyncio.sleep(15)
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
            if "sug" in message.content.lower():
                await farmSugar(user)
            else:
                await farmWart(user)
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

client.run(clientKey)
