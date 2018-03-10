#!/usr/bin/python3

import shelve,os,sys,numpy

if len(sys.argv) != 5:
    print("Usage ./finalInterpreter.py inputImages sentenceStruct shelveFile shelveFile2")
    sys.exit()
images = open(sys.argv[1],"r")
sentenceStruct= open(sys.argv[2],"r")
IMAGESIZE = 28*28
db = [shelve.open(str(sys.argv[3])),shelve.open(str(sys.argv[4]))]
        
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
THETA1 = []
THETA2 = []
try:
    THETA1 = db[0]['theta']
    THETA2 = db[1]['theta']
except:
    print("couldn't find theta in shelve")
    sys.exit()


NEURONS1 = [THETA1[0].shape[1]-1]
NEURONS2 = [THETA2[0].shape[1]-1]

for i in range(len(THETA1)):
    NEURONS1.append(THETA1[i].shape[0])
for i in range(len(THETA2)):
    NEURONS2.append(THETA2[i].shape[0])

A1 = forwardPropogation(X,NEURONS1,THETA1)
A2 = forwardPropogation(X,NEURONS2,THETA2)

A1[-1] = A1[-1].T
A2[-1] = A2[-1].T

#print(A[-1])
m1=[]
m2=[]
finalOut = []
for i in range(A1[-1].shape[0]):
    m1=max(A1[-1][i])
    m2=max(A2[-1][i])
    m1 -= 0.01
    m2 -= 0.01
    if m1 > m2:
        for j in range(A1[-1].shape[1]):
            if A1[-1][i][j] >= m1:
                A1[-1][i][j] = 1
                finalOut.append(chr(j+ord('A')))
            else:
                A1[-1][i][j] = 0
    else:
        for j in range(A2[-1].shape[1]):
            if A2[-1][i][j] >= m2:
                A2[-1][i][j] = 1
                finalOut.append(chr(j+ord('0')))
            else:
                A2[-1][i][j] = 0

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
