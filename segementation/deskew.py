#!/usr/bin/python3
from PIL import Image,ImageDraw
import math

im = Image.open('skew.jpg')
gray = im.convert('L')

corners = []

#LB
for i in range(im.size[0]):
    flag = False
    for j in range(im.size[1]):
        if gray.getpixel((i,j))<10:
            corners.append((i,j))
            flag = True
            break
    if flag==True:
        break
#LU
for j in range(im.size[1]):
    flag = False
    for i in range(im.size[0]):
        if gray.getpixel((i,j))<10:
            corners.append((i,j))
            flag = True
            break
    if flag==True:
        break
#RU
for i in reversed(range(im.size[0])):
    flag = False
    for j in range(im.size[1]):
        if gray.getpixel((i,j))<10:
            corners.append((i,j))
            flag = True
            break
    if flag==True:
        break
#RB
for j in reversed(range(im.size[1])):
    flag = False
    for i in reversed(range(im.size[0])):
        if gray.getpixel((i,j))<10:
            corners.append((i,j))
            flag = True
            break
    if flag==True:
        break

print(corners)

new = Image.new('RGB',im.size,(255,255,255))
draw = ImageDraw.Draw(new)
draw.line((corners[0][0],corners[0][1],corners[1][0],corners[1][1]),fill=128)
draw.line((corners[0][0],corners[0][1],corners[3][0],corners[3][1]),fill=128)
draw.line((corners[2][0],corners[2][1],corners[3][0],corners[3][1]),fill=128)
draw.line((corners[2][0],corners[2][1],corners[1][0],corners[1][1]),fill=128)
new.show()

#create image with alpha channel
im1 = Image.new('RGBA',im.size,(255,255,255,255))
im1.paste(im,(0,0))
# converted to have an alpha layer
im2 = im1.convert('RGBA')
# rotated image
rot = im1.rotate(15, expand=1)
# a white image same size as rotated image
fff = Image.new('RGBA', rot.size, (255,)*4)
# create a composite image using the alpha layer of rot as a mask
out = Image.composite(rot, fff, rot)
# save your work (converting back to mode='1' or whatever..)
#out.convert(img.mode).save('test2.bmp')
out1 = Image.new('RGB',out.size,(255,255,255,255))
out1.paste(out,(0,0))
out1.save('out.jpg')
