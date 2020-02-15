from PIL import Image, ImageChops
import os
import cv2
import numpy as np

home = os.path.dirname(os.path.abspath(__file__)) +"\\"

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def crop(img):
  crop_img = img[:, 0:32]
  return crop_img

def getPolygon(width, height):
  pts = []
  pts.append([0,  32])
  pts.append([32, 32+16])
  pts.append([64, 32])

  pts.append([64, 64])
  pts.append([0, 64])

  pts = np.array([pts])
  return pts


filename_in  = home+'blocks/wall.png'
filename_out = home+'blocks/wall.png'
img = Image.open(filename_in)
img = trim(img)

img = np.array(img) 
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# img = img[:, :, ::-1].copy() 

img = cv2.resize(img, (64, 64), interpolation = cv2.INTER_AREA)

points = getPolygon(64, 64) #np.array([[910, 641], [206, 632], [696, 488], [458, 485]])
# points.dtype => 'int64'
# cv2.polylines(img, np.int32([points]), 5, (255,255,255))
cv2.fillPoly(img, np.int32([points]), (0,0,0))

size = img.shape
print(size)

# cv2.imshow("Image", img)
# cv2.waitKey(0)

cv2.imwrite(filename_out, img)
