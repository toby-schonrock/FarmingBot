import cv2
import os

#print(image.shape)
#print(image[594, 2318])

startY = 500
height = 1440
startX = 2200
width = 2560

scanwidth = 115
scanheight = 13

data = list(map(int, open("YourIsland.txt", "r").read().split(','))) # plase fix and make int

def find_first(image):
    for y in range(startY, height):
        for x in range(startX, width):
            pixel = image[y, x]
            if pixel[0] == 85 and pixel [1] == 255 and pixel[2] == 85:
                return x, y

def process(name):
    image = cv2.imread("./tests/" + name)
    rows, cols, channels = image.shape
    start = find_first(image)
    for x in range(scanwidth):
        for y in range(scanheight):
            pixel = image[y + start[1], x + start[0]]
            if int(pixel[0] == 85 and pixel[1] == 255 and pixel[2] == 85) != data[x + y * scanwidth]:
                print("no dumbass")
                return False
    return True

files = os.listdir("./tests/")
for f in files:
    process(f)
    print()

cv2.destroyAllWindows()
