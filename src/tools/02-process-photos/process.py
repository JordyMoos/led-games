
import time
import numpy as np
import imutils
import cv2
from wand.image import Image
import os

# directory of the photos
# for example: "../01-recoding/pi-camera/photos-1576942306/"
PHOTO_DIR = "../01-recoding/gopro/photos-1576942306"

# the pair conclusion file
# the `pair` file holds all the found led indices and their pixel position
# the `view` file holds all the leds available for a viewport in the game engine
# here we put all the leds into in the the "main" view
timestamp = round(time.time())
PAIR_FILE = "./pair-%d.csv" % timestamp
VIEW_FILE = "./view-%d-1.csv" % timestamp

# leds to pair
START_LED = 0
TOTAL_LEDS = 5

# dimensions of the images
ROTATE = -90
CROP_LEFT = 0
CROP_TOP = 0
CROP_RIGHT = 0
CROP_BOTTOM = 0

# directory to store images produced by the calculations
# this can be handy to debug and see what this concluded
# DEBUG_DIR = None
DEBUG_DIR = "./debug-%d" % round(time.time())

# mask image
# for example: "./mask.png"
MASK_IMAGE_FILE = None

'''

    End of configuration

'''

if DEBUG_DIR:
    os.mkdir(DEBUG_DIR)

pair_file = open(PAIR_FILE, 'a')
view_file = open(VIEW_FILE, 'a')

mask_input = None
if MASK_IMAGE_FILE:
    mask_input = Image(filename=MASK_IMAGE_FILE)
    mask_input.crop(CROP_LEFT, CROP_TOP, mask_input.width - CROP_RIGHT, mask_input.height - CROP_BOTTOM)
    mask_input.rotate(ROTATE)

background = None
background_cv = None

for led_index in range(START_LED, TOTAL_LEDS):
    # resolve background
    potential_background = "%s/%05d-background.jpg" % (PHOTO_DIR, led_index)
    if os.path.isfile(potential_background):
        background = Image(filename=potential_background)
        background.crop(CROP_LEFT, CROP_TOP, background.width-CROP_RIGHT, background.height-CROP_BOTTOM)
        background.rotate(ROTATE)
        if mask_input:
            background.composite(mask_input)

        background_buffer = np.asarray(bytearray(background.make_blob()), dtype=np.uint8)
        background_cv = cv2.imdecode(background_buffer, cv2.IMREAD_UNCHANGED)

    # if we do not have a background by now then we can not continue
    # therefor we have to skip this led
    if not background:
        print("Sadly we have no background and need to skip led %d" % led_index)
        continue

    # get the leds image
    led_image_name = "%s/%05d-led.jpg" % (PHOTO_DIR, led_index)
    led_image = Image(filename=led_image_name)
    led_image.crop(CROP_LEFT, CROP_TOP, led_image.width-CROP_RIGHT, led_image.height-CROP_BOTTOM)
    led_image.rotate(ROTATE)
    if mask_input:
        led_image.composite(mask_input)

    # let opencv compare the images
    led_buffer = np.asarray(bytearray(led_image.make_blob()), dtype=np.uint8)
    led_cv = cv2.imdecode(led_buffer, cv2.IMREAD_UNCHANGED)

    mog = cv2.bgsegm.createBackgroundSubtractorMOG()
    _ = mog.apply(background_cv)
    mask = mog.apply(led_cv)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if not cnts:
        print("Led %d not found" % led_index)
        continue

    c = max(cnts, key=cv2.contourArea)
    # compute the center of the contour
    m = cv2.moments(c)
    if m["m00"] != 0:
        cX = int(m["m10"] / m["m00"])
        cY = int(m["m01"] / m["m00"])
    else:
        cX, cY = 0, 0

    marked = led_cv.copy()
    cv2.circle(marked, (cX, cY), 30, (255, 0, 0), -1)
    cv2.drawContours(marked, [c], -1, (0, 255, 0), 2)

    if DEBUG_DIR:
        cv2.imwrite('%s/%05d-led.png' % (DEBUG_DIR, led_index), led_cv)
        cv2.imwrite('%s/%05d-mask.png' % (DEBUG_DIR, led_index), mask)
        cv2.imwrite('%s/%05d-mark.png' % (DEBUG_DIR, led_index), marked)

    print((led_index, cX, cY))
    pair_file.write("%d,%d,%d\n" % (led_index, cX, cY))
    view_file.write("%d\n" % led_index)


# close the file handles
pair_file.close()
view_file.close()

# print information we need for the game engine
print("")
print("Pair file path:")
print(os.path.abspath(PAIR_FILE))
print("")
print("View file path:")
print(os.path.abspathVIEW_FILE))
print("")

# caclulate the mins and maxes
lines = [
    list(map(int, line.rstrip('\n').split(',', 3)))
    for line in open(PAIR_FILE)
]

xs = list(map(lambda line: line[1], lines))
ys = list(map(lambda line: line[2], lines))

# and print those to
print('x min = %d' % min(xs))
print('x max = %d' % max(xs))
print('')
print('y min %d' % min(ys))
print('y max %d' % max(ys))

print("")
print("")

print("Done!")
