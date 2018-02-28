#!/usr/bin/python3
from PIL import Image,ImageDraw,ImageFilter
import math

#return rotated image
def rotate(angle):
    #create image with alpha channel
    im1 = Image.new('RGBA',im.size,(255,255,255,255))
    im1.paste(im,(0,0))
    # converted to have an alpha layer
    im2 = im1.convert('RGBA')
    # rotated image
    rot = im1.rotate(angle, expand=1)
    # a white image same size as rotated image
    fff = Image.new('RGBA', rot.size, (255,)*4)
    # create a composite image using the alpha layer of rot as a mask
    out = Image.composite(rot, fff, rot)
    # save your work (converting back to mode='1' or whatever..)
    #out.convert(img.mode).save('test2.bmp')
    out1 = Image.new('RGB',out.size,(255,255,255,255))
    out1.paste(out,(0,0))
    return out1

im = Image.open('skew.jpg')
gray = im.convert('L')

corners = []

for i in range(im.size[0]):
    flag = False
    for j in range(im.size[1]):
        if gray.getpixel((i,j))<30:
            corners.append([i,j])
            flag = True
            break
    if flag==True:
        break
for j in range(im.size[1]):
    flag = False
    for i in range(im.size[0]):
        if gray.getpixel((i,j))<30:
            corners.append([i,j])
            flag = True
            break
    if flag==True:
        break
for i in reversed(range(im.size[0])):
    flag = False
    for j in range(im.size[1]):
        if gray.getpixel((i,j))<30:
            corners.append([i,j])
            flag = True
            break
    if flag==True:
        break
for j in reversed(range(im.size[1])):
    flag = False
    for i in reversed(range(im.size[0])):
        if gray.getpixel((i,j))<30:
            corners.append([i,j])
            flag = True
            break
    if flag==True:
        break

#convert corners to cartesian system and identify correct corners
# LU LB RU RB
for i in range(len(corners)):
    corners[i][1] = im.size[1]-1-corners[i][1]
corners = sorted(corners,key=lambda x:x[0])
if corners[0][1] > corners[1][1]:
    corners[0],corners[1] = corners[1],corners[0]
if corners[2][1] > corners[3][1]:
    corners[2],corners[3] = corners[3],corners[2]

#find angle of roatation from corners
m1 = (corners[2][1]-corners[0][1]) / (corners[2][0]-corners[0][0])
th1 = math.degrees(math.atan(m1))
m2 = (corners[3][1]-corners[1][1]) / (corners[3][0]-corners[1][0])
th2 = math.degrees(math.atan(m2))
m3 = (corners[1][1]-corners[0][1]) / (corners[1][0]-corners[0][0])
th3 = math.degrees(math.atan(m3)) - 90
m4 = (corners[3][1]-corners[2][1]) / (corners[3][0]-corners[2][0])
th4 = math.degrees(math.atan(m4)) - 90
th = -(th1+th2+th3+th4)/4

#rotate image
out = rotate(th)
gout = out.convert("L")

'''
#remove black boundary from image
for i in range(out.size[0]):
    for j in range(out.size[1]):
        if gout.getpixel((i,j)) < 30:
            out.putpixel((i,j),(255,255,255))
'''
'''
rcorners=[]

for i in range(out.size[0]):
    rflag = False
    for j in range(out.size[1]):
        if gout.getpixel((i,j))<30:
            rcorners.append([i,j])
            rflag = True
            break
    if rflag==True:
        break

for i in reversed(range(out.size[0])):
    rflag = False
    for j in range(out.size[1]):
        if gout.getpixel((i,j))<30:
            rcorners.append([i,j])
            rflag = True
            break
    if rflag==True:
        break

c = int(corners[0][0]/2 + corners[1][0]/2)

for i in range(min(corners[0][1],corners[1][1]),gout.size[1]):
    if gout.getpixel((c,i)) > 100:
        rcorners.append([c,i])
        break

draw = ImageDraw.Draw(out)
draw.line((0,corners[0][1],im.size[0],corners[0][1]),fill=128)
draw.line((0,corners[1][1],im.size[0],corners[1][1]),fill=128)
draw.line((0,corners[2][1],im.size[0],corners[2][1]),fill=128)
out.show()
'''
findwidth = []
new = out.filter(ImageFilter.FIND_EDGES)
newg = new.convert('L')
newg.show()
#out.show()
out.save('skew_no.jpg')
