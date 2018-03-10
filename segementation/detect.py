#!/usr/bin/python3
import sys
from PIL import Image
import os

#open all neccessary files
if len(sys.argv)!=2:
    print('Usage: ./detect.py imageName')
    sys.exit()
im = Image.open(sys.argv[1])

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

#scan a single line, returns its sentence structure and appends image arrays to out
def scanLine(i,out,num):

    #set up gray,hor,ver images
    im = Image.open(i)
    gray = im.convert("L")
    ver = Image.new('RGB',im.size,(255,255,255))

    #create vertical boxes(filled,red) around words in ver.jpg
    vcheck = [0 for i in range(im.size[0])]
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if gray.getpixel((i,j))<225:
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

    #find horizontal lines per word
    up=[]
    down=[]
    for i in range(len(start)):
        flagUp = False
        flagDown = False
        for k in range(im.size[1]):
            for j in range(start[i],end[i]+1):
                if gray.getpixel((j,k)) <= 225:
                    flagUp = k
                if flagUp!=False:
                    break
            if flagUp!=False:
                break
        for k in reversed(range(im.size[1])):
            for j in range(start[i],end[i]+1):
                if gray.getpixel((j,k)) <= 225:
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
                inp[i].append(new.getpixel((k,j)))
        '''
        for j in range(28):
            for k in range(28):
                if new.getpixel((k,j))>=150/255:
                    print(' ',end='')
                else:
                    print('0',end='')
            print('')
        '''

    #save for viewing and debugging
    #name = 'final_' + str(num) + '_' + sys.argv[1]
    #gray.save(name)

    #input file
    for i in range(len(inp)):
        for j in range(len(inp[i])):
            out.write(str(inp[i][j])+' ')
        out.write('\n')
    return sentence

##-- MAIN --##

#open all neccessary files
im = Image.open(sys.argv[1])
g = im.convert("L")
hor = Image.new('RGB',im.size,(255,255,255))

#detect rotation in image
#TODO

#create red blocks (red,horizontal)
for i in range(g.size[1]):
    check = False
    for j in range(g.size[0]):
        if g.getpixel((j,i)) < 225:
            check = True
            break
    if check == True:
        for k in range(g.size[0]):
            hor.putpixel((k,i),(255,0,0))

#create boundaries(red) in hor.jpg
hbound = [0 for i in range(im.size[1])]
for i in range(1,im.size[1]-1):
    if hor.getpixel((14,i-1))==(255,0,0) and hor.getpixel((14,i))==(255,0,0) and hor.getpixel((14,i+1))==(255,255,255):
        hbound[i] = 1
    if hor.getpixel((14,i-1))==(255,255,255) and hor.getpixel((14,i))==(255,0,0) and hor.getpixel((14,i+1))==(255,0,0):
        hbound[i] = 2

#border cases
#case 1 - touching top edge
if hor.getpixel((14,0))==(255,0,0):
    hbound[0] = 2
#case 2 - touching bottom edge
if hor.getpixel((14,im.size[1]-1))==(255,0,0):
    hbound[im.size[1]-1] = 1

#make changes to hor
for i in range(im.size[1]):
    if hbound[i]==0:
        for j in range(im.size[0]):
            hor.putpixel( (j,i) , (255,255,255) )
    if hbound[i]==1:
        for j in range(im.size[0]):
            hor.putpixel( (j,i) , (255,0,0) )
    if hbound[i]==2:
        for j in range(im.size[0]):
            hor.putpixel( (j,i) , (0,0,255) )

#create lists to identify start and end of words
top = []
bottom = []
for i in range(len(hbound)):
    if hbound[i]==1:
        bottom.append(i)
    if hbound[i]==2:
        top.append(i)
del hbound

if len(top)!=len(bottom):
    print('incorrect border cases(lines) (start,end)')
    hor.show()
    sys.exit()

numLines = len(top)

'''
#add a directory with name of image and change to it
name = sys.argv[1].rstrip('.jpg') + '_temp'
path = os.getcwd()
newPath = path + '/' + name
if not os.path.exists(newPath):
    os.makedirs(newPath)
os.chdir(newPath)
'''

#open files to write text
out = open(sys.argv[1].rstrip('.jpg')+'_t.txt','a')
out1 = open(sys.argv[1].rstrip('.jpg')+'_s.txt','a')

#store final images
for i in range(len(top)):
    im_temp = im.crop((0,top[i],im.size[0],bottom[i]))
    nm = str(i) + '.jpg'
    im_temp.save(nm)

#store individual letters along with sentence
sentence = []
for i in range(len(top)):
    nm = str(i) + '.jpg'
    sentence.append(scanLine(nm,out,i))

for i in range(len(top)):
    os.remove(str(i)+'.jpg')

#save sentence structure
for i in range(len(sentence)):
    for j in range(len(sentence[i])):
        if sentence[i][j]==None:
            out1.write('W')
        if sentence[i][j]==' ':
            out1.write('S')
    out1.write('\n')

out.close()
out1.close()

#g.save('gray.jpg')
#hor.save("hor.jpg")
