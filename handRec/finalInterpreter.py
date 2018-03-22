#!/usr/bin/python3

import shelve,os,sys,numpy

if len(sys.argv) != 3:
    print("Usage ./finalInterpreter.py inputImages sentenceStruct")
    sys.exit()
images = open(sys.argv[1],"r")
sentenceStruct= open(sys.argv[2],"r")
IMAGESIZE = 28*28
db = shelve.open("weights")
db2= shelve.open("weights1")
db3= shelve.open("weights2")
def getImages(inFile,inpNum,inpSize):
    #extract data from txt file
    data =  []
    x = []
    for i in range(inpNum):
        data = inFile.readline().split()
        for j in range(inpSize):
            x.append(float(data[j]))
        del data
    #convert to np arrays
    x = numpy.array(x)
    x = x.reshape(inpNum,inpSize)
    x = x / numpy.max(x)
    return x

def calcG(theta,x):
    z = theta.dot(x)
    sig = 1/(1+numpy.exp(-z))
    del z
    return sig

def forwardPropogation(X,neurons,theta,numLayers=None,prevA=None):
    if(numLayers==None):
        numLayers=len(neurons)
    if(prevA==None):
        prevA = [X]
        for i in range(numLayers-1):
            prevA[i]=numpy.insert(prevA[i],0,1,axis=0)
            prevA.append(calcG(theta[i],prevA[i]))
    else:
        prevA[1]=calcG(theta[0],prevA[0])
        for i in range(1,numLayers-1):
            prevA[i]=numpy.insert(prevA[i],0,1,axis=0)
            prevA[i+1]=calcG(theta[i],prevA[i])
    return prevA


lines = sentenceStruct.readlines() #Entire text file is copied into lines as a list
numImages = 0
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if(lines[i][j]=='W'):
            numImages+=1
print(numImages)
X = getImages(images,numImages,IMAGESIZE)
X=X.T

'''
X = X.T
new=[]

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        if j%28 !=0:
            if X[i][j]>=150/255:
                print(' ',end='')
            else:
                print('0',end='')
        else:
            if X[i][j]>=150/255:
                print(' ')
            else:
                print('0')
X=X.T
'''
THETA = []
try:
    THETA = db['theta']
    print("SUCCESS")
    THETA2 = db2['theta']
    print("SUCCESS")
    THETA3 = db3['theta']
except:
    print("couldn't find theta in shelve")
    sys.exit()


NEURONS = [THETA[0].shape[1]-1]
NEURONS2 = [THETA2[0].shape[1]-1]
NEURONS3 = [THETA3[0].shape[1]-1]

for i in range(len(THETA)):
    NEURONS.append(THETA[i].shape[0])
    NEURONS2.append(THETA2[i].shape[0])
    NEURONS3.append(THETA3[i].shape[0])

A = forwardPropogation(X,NEURONS,THETA)
A2 = forwardPropogation(X,NEURONS2,THETA2)
A3 = forwardPropogation(X,NEURONS3,THETA3)

matFinal = numpy.concatenate((A[-1]*0.8,A2[-1]*0.90,A3[-1]),axis=0)
matFinal = matFinal.T

print(matFinal)
m=0
finalOut = []
for i in range(matFinal.shape[0]):
    m=max(matFinal[i])
    m -= 2**(-5)
    for j in range(matFinal.shape[1]):
        if matFinal[i][j] >= m:
            matFinal[i][j] = 1
            if j<10:
                finalOut.append(chr(j+ord('0')))
            elif j<36:
                finalOut.append(chr(j-10+ord('A')))
            else:
                finalOut.append(chr(j-36+ord('a')))
            break
        else:
            matFinal[i][j] = 0

for i in range(len(lines)):
    lines[i]=list(lines[i])

#print(finalOut)
#print(lines)
wordNum=0
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if(lines[i][j]=='W'):
            lines[i][j]=finalOut[wordNum]
            wordNum+=1
        elif(lines[i][j]=='S'):
            lines[i][j]=" "

print(lines)
