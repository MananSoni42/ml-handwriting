#!/usr/bin/python3
import sys
from PIL import Image
import os

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
#            gray.putpixel( (i,j) , (0) )
    if vbound[i]==2:
        for j in range(im.size[1]):
            ver.putpixel( (i,j) , (0,0,255) )
#            gray.putpixel( (i,j) , (0) )

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
    print('incorrect border cases (start,end)')
    sys.exit()

#count number of words and print
words = len(start)
print('words:',words)

#make array to store space distances
sdist=[]
#border case-1: touching left edge
if start[0]!=0:
    sdist.append(start[0])
#general case
for i in range(len(start)-1):
    sdist.append(start[i+1] - end[i])
#border case-2: touching right edge
if end[-1]!=im.size[0]-1:
    sdist.append(im.size[0]-1 - end[-1])

#make array to store difference between consecutive spaces
sdiff=[]
ssort = sorted(sdist,reverse=True)
for i in range(len(ssort)-1):
    sdiff.append(ssort[i] - ssort[i+1])
m = max(sdiff)
avg = sum(sdist)/len(sdist)
#find wall(index) for max space difference
for i in range(len(ssort)-1):
    if ssort[i]-ssort[i+1]==m:
        wall = i+1
        break
#count number of spaces through wall
spaces = 0
for i in range(len(sdist)):
    if sdist[i] > ssort[wall]:
        spPos = i
        spaces+=1
if m - avg < 0.4*avg:
    spaces = 0
print('spaces:',spaces)

#sentence formation
sentence = []
for i in range(words+spaces):
    sentence.append(None)
sentence[spPos] = ' '
print(sentence)

#find horizontal lines per word
up=[]
down=[]
for i in range(len(start)):
    flagUp = False
    flagDown = False
    for k in range(im.size[1]):
        for j in range(start[i],end[i]+1):
            if gray.getpixel((j,k)) <= 200:
                flagUp = k
            if flagUp!=False:
                break
        if flagUp!=False:
            break
    for k in reversed(range(im.size[1])):
        for j in range(start[i],end[i]+1):
            if gray.getpixel((j,k)) <= 200:
                flagDown = k
            if flagDown!=False:
                break
        if flagDown!=False:
            break
    up.append(flagUp)
    down.append(flagDown)

#error checking
if len(up)!=len(down):
    print('border error (up,dow)')
    sys.exit()
if len(up)!=len(start):
    print('border error (up,start)')
    sys.exit()

#add horizontal and vertical bars to gray.jpg
#horizontal
for i in range(len(up)):
    for k in range(start[i],end[i]):
        gray.putpixel((k,up[i]),0)
        gray.putpixel((k,down[i]),0)
#vertical
for i in range(len(start)):
    for k in range(up[i],down[i]):
        gray.putpixel((start[i],k),0)
        gray.putpixel((end[i],k),0)

#create folder crop and change dir to crop
path = os.path.abspath('.')
newPath = path + '/crop'
if not os.path.exists(newPath):
    os.makedirs(newPath)
os.chdir(newPath)

#add cropped images to crop
for i in range(len(start)):
    temp = gray.crop((start[i],up[i],end[i]+1,down[i]+1))
    name = str(i) + '.jpg'
    temp.save(name)

#save for viewing and debugging
os.chdir(path)
im.save('test.jpg')
gray.save('gray.jpg')
