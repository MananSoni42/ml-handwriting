#!/usr/bin/python3
import sys
from PIL import Image
import os

#open all neccessary files
if len(sys.argv)!=4:
    print('Usage: ./detect.py imageName OutImageAsTxt OutSentenceStucture')
    sys.exit()
im = Image.open(sys.argv[1])
out = open(sys.argv[2],'w')
sentenceOut = open(sys.argv[3],'w')
def convTo28x28(img):
    width,height = img.size
    final = Image.new('L',(28,28),255)
    #if image is big convert to small enough image
    factor = 1
    if width>height:
        if width > 24:
            factor = 24/width
        newWidth = int(round(factor*width,0))
        newHeight = int(round(factor*height,0))
    elif height>=width:
        if height > 24:
            factor = 24/height
        newWidth = int(round(factor*width,0))
        newHeight = int(round(factor*height,0))

    smallIm = img.resize((newWidth,newHeight))

    #find center wrt image
    centerX = int(round(14 - (newWidth/2),0)+1)
    centerY = int(round(14 - (newHeight/2),0))

    #paste cropped image (28x) or (x28) on white 28x28 image at it's center
    final.paste(smallIm,(centerX,centerY))

    return final

#set up gray,hor,ver images
gray = im.convert("L")
ver = Image.new('RGB',im.size,(255,255,255))

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
    if (ver.getpixel((i-1,14))==(255,0,0) and ver.getpixel((i,14))==(255,0,0) and ver.getpixel((i+1,14))==(255,255,255)):
        vbound[i] = 1
    if (ver.getpixel((i-1,14))==(255,255,255) and ver.getpixel((i,14))==(255,0,0) and ver.getpixel((i+1,14))==(255,0,0)):
        vbound[i] = 2
#border cases
#case 1 - touching left edge
if ver.getpixel((0,14))==(255,0,0):
    vbound[0]=2
#case 2 - touching right edge
if ver.getpixel((im.size[0]-1,14))==(255,0,0):
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
    print('incorrect border cases (start,end)')
    ver.show()
    sys.exit()

#count number of words
words = len(start)
#make array to store space distances
sdist=[]
fstart = False
fend = False
#border case-1: touching left edge
if start[0]!=0:
    sdist.append(start[0])
    fstart = True
#general case
for i in range(len(start)-1):
    sdist.append(start[i+1] - end[i])
#border case-2: touching right edge
if end[-1]!=im.size[0]-1:
    sdist.append(im.size[0]-1 - end[-1])
    fend = True

#make array to store difference between consecutive spaces
sdiff=[]
ssort = sorted(sdist,reverse=True)
for i in range(len(ssort)-1):
    sdiff.append(ssort[i] - ssort[i+1])
#find wall(index) for max space difference
m = max(sdiff)
for i in range(len(ssort)-1):
    if ssort[i]-ssort[i+1]==m:
        wall = i+1
        break
#count number of spaces through wall
spaces = 0
spPos=[]
for i in range(len(sdist)):
    if sdist[i] > ssort[wall]:
        spaces+=1

#disregerding cases where 0 spaces should be found
av1 = sum( [ssort[i] for i in range(wall)] ) / wall
av2 = sum( [ssort[i] for i in range(wall,len(ssort))] ) / (len(ssort)-wall)
av3 = sum(ssort)/len(ssort)
if av1 - av3 < 0.75*av3:
    spaces = 0

#sentence formation
sentence = []
if spaces == 0:
    for i in range(len(start)):
        sentence.append(None)
else:
    struct = []
    for i in range(len(sdist)):
        struct.append('w')
        struct.append(sdist[i])
    struct.append('w')
    if fstart == True:
        del struct[0]
    if fend == True:
        del struct[-1]
    for i in range(len(struct)):
        if struct[i]=='w':
            sentence.append(None)
        else:
            if struct[i] > ssort[wall]:
                sentence.append(' ')

#write sentence structure to file
for i in range(len(sentence)):
    if sentence[i]==None:
        sentenceOut.write('W ')
    if sentence[i]==' ':
        sentenceOut.write('S ')
sentenceOut.write('\n')

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

inp = []

#add cropped images to crop
for i in range(len(start)):
    #add temporary images
    temp = gray.crop((start[i],up[i],end[i]+1,down[i]+1))
    #add final images + create input array
    new = convTo28x28(temp)
    #create and add input
    inp.append([])
    for j in range(28):
        for k in range(28):
            if new.getpixel((k,j))>=255:
                inp[i].append(255)
            elif new.getpixel((k,j))<=0:
                inp[i].append(0)
            else:
                inp[i].append(new.getpixel((k,j)))
'''
    for j in range(28):
        for k in range(28):
            if new.getpixel((k,j))>=1:
                print(' ',end='')
            else:
                print('0',end='')
        print('')
'''

#save for viewing and debugging
name = 'final_' + sys.argv[1]
gray.save(name)
#input file
for i in range(len(inp)):
    for j in range(len(inp[i])):
        out.write(str(inp[i][j])+' ')
    out.write('\n')
