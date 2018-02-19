#!/usr/bin/python3
import sys
from PIL import Image

if len(sys.argv)!=2:
    print('Usage: ./detect.py imageName')
    sys.exit()

#set up gray,hor,ver images
im = Image.open(sys.argv[1])
gray = im.convert("L")
ver = Image.new('RGB',im.size,(255,255,255))
hor = Image.new('RGB',im.size,(255,255,255))

#create vertical boxes(filled,red) around words in ver.jpg
vcheck = [0 for i in range(im.size[0])]
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if gray.getpixel((i,j))<200:
            if vcheck[i]==0:
                vcheck[i]=1
                for k in range(im.size[1]):
                    ver.putpixel( (i,k) , (255,0,0) )

#create boundaries(black) in ver.jpg
vbound = [0 for i in range(im.size[0])]
for i in range(1,im.size[0]-1):
    if (ver.getpixel((i-1,100))==(255,0,0) and ver.getpixel((i,100))==(255,0,0) and ver.getpixel((i+1,100))==(255,255,255)):
        vbound[i] = 1
    if (ver.getpixel((i-1,100))==(255,255,255) and ver.getpixel((i,100))==(255,0,0) and ver.getpixel((i+1,100))==(255,0,0)):
        vbound[i] = 2
#border cases
#case 1 - touching left edge
if ver.getpixel((0,100))==(255,0,0):
    vbound[0]==2
#case 2 - touching right edge
if ver.getpixel((im.size[0]-1,100))==(255,0,0):
    vbound[im.size[0]-1]=1
#make changes to ver
for i in range(im.size[0]):
    if vbound[i]==0:
        for j in range(im.size[1]):
            ver.putpixel( (i,j) , (255,255,255) )
    if vbound[i]==1:
        for j in range(im.size[1]):
            ver.putpixel( (i,j) , (255,0,0) )
    if vbound[i]==2:
        for j in range(im.size[1]):
            ver.putpixel( (i,j) , (0,0,255) )

#create lists to identify start and end of words
start = []
end = []
for i in range(len(vbound)):
    if vbound[i]==1:
        end.append(i)
    if vbound[i]==2:
        start.append(i)
del vbound
if len(start)!=len(end):
    print('incorrect border cases')
    sys.exit()

#count number of words and print
words = len(start)
print('words:',words)

hor.save('hor.jpg')
ver.save('ver.jpg')
gray.save('gray.jpg')
