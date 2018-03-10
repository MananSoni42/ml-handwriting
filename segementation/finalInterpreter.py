#!/usr/bin/python3

import shelve,os,sys,numpy

if len(sys.argv) != 4:
    print("Usage ./finalInterpreter.py inputImages sentenceStruct shelveFile")
    sys.exit()
images = open(sys.argv[1],"r")
sentenceStruct= open(sys.argv[2],"r")
IMAGESIZE = 28*28
db = shelve.open(str(sys.argv[3]))

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
except:
    print("couldn't find theta in shelve")
    sys.exit()

NEURONS = []
NEURONS.append(THETA[0].shape[1]-1)
for i in range(len(THETA)):
    NEURONS.append(THETA[i].shape[0])
A = forwardPropogation(X,NEURONS,THETA)
A[-1] = A[-1].T
#print(A[-1])
for i in range(A[-1].shape[0]):
    m = max(A[-1][i])
    print(m)
    m -= 0.01
    for j in range(A[-1].shape[1]):
        if A[-1][i][j] >= m:
            A[-1][i][j] = 1
        else:
            A[-1][i][j] = 0

wordNum=0
finalOut = []
for i in range(len(lines)):
    finalOut.append([])
    for j in range(len(lines[i])):
        if(lines[i][j]=='W'):

            for k in range(36):
                if(A[-1][wordNum][k]==1):
                    if k<10:
                        finalOut[i].append(chr(k+48))
                    else :
                        finalOut[i].append(chr(k-10+ord('A')))
                    break
                if k == 35:
                    finalOut[i].append('?')
            wordNum +=1
            '''
            for k in range(26):
                if(A[-1][wordNum][k]==1):
                    finalOut[i].append(chr(k+ord('A')))
                    break
                if k == 35:
                    finalOut[i].append('?')
            wordNum +=1
            '''
        elif(lines[i][j]=='\n'):
            finalOut[i].append('\n')
            continue
        elif(lines[i][j]=='S'):
            finalOut[i].append(' ')
del finalOut[0][-1]
print(finalOut)
