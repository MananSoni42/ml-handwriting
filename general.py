#!/usr/bin/python3
import numpy as np
import math
import random
import matplotlib.pyplot as plt

#metaparameters
size=[2,3,1]
iterations = 10000
rate = 0.001
l = 0.00
inpNum = 20
testNum = 10

#secondary metaparameters
numLayers=len(size)
inpSize = size[0]
outSize = size[-1]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def dsigmoid(x):
    return x*(1-x)

def getData():
    #extract data from txt file
    data =  []
    x = []
    y = []
    for i in range(inpNum):
        data = input().split()
        for j in range(outSize):
            y.append(float(data[-j-1]))
        for j in range(inpSize-outSize+1):
            x.append(float(data[j]))
        del data
    #extract test data
    data =  []
    tx = []
    ty = []
    for i in range(testNum):
        data = input().split()
        for j in range(outSize):
            ty.append(float(data[-j-1]))
        for j in range(inpSize-outSize+1):
            tx.append(float(data[j]))
        del data
    #convert to np arrays
    x = np.array(x)
    x = x.reshape(inpNum,inpSize)
    y = np.array(y)
    y = y.reshape(inpNum,outSize)
    #convert test data
    tx = np.array(tx)
    tx = tx.reshape(testNum,inpSize)
    ty = np.array(ty)
    ty = ty.reshape(testNum,outSize)
    #scale the data
    x = x / np.max(x)
    y = y / np.max(y)
    #scale test data
    tx = tx / np.max(tx)
    ty = ty / np.max(ty)
    return x,y,tx,ty

def initNet():
    b=[]
    w=[]
    b.append(0)
    w.append(0)
    for i in range(numLayers-1):
        temp=[]
        for j in range(size[i]*size[i+1]):
            temp.append(float(random.randint(-5,5)))
        w.append(np.array(temp).reshape(size[i],size[i+1]))
        b.append(float(random.randint(-5,5)))
        del temp
    return w,b

def train(x,y,w,b):

    #forward prop
    a=[]
    a.append(0)
    for i in range(numLayers):
        a.append(0)

    a[1] = np.array(x)
    for i in range(1,numLayers):
        a[i+1] = np.array(sigmoid(a[i].dot(w[i])+b[i]))

    #backward prop
    delta = []
    delta.append(0)
    for i in range(numLayers-1):
        delta.append(0)
    delta[-1] = np.array(a[-1] - y)
    for i in range(numLayers-2,0,-1):
        delta[i] = np.array( delta[i+1].dot(w[i+1].T)*dsigmoid(a[i+1]) )

    #regularization
    s = []
    s.append(0)
    for i in range(1,numLayers):
        s.append(0)
        temp = w[i].flatten()
        for j in range(len(temp)):
            s[i] += l*abs(temp[j])

    #update weights
    for i in range(1,numLayers):
        w[i] -= rate * ( a[i].T.dot(delta[i]) + s[i] )
        b[i] -= rate * (delta[i]).sum(axis=0)

    return a[-1]

#test on the sample
def test(x,w,b):
    a=[]
    a.append(0)
    for i in range(numLayers):
        a.append(0)

    a[1] = np.array(x)
    for i in range(1,numLayers):
        a[i+1] = np.array(sigmoid(a[i].dot(w[i])+b[i]))

    h = a[-1]

    for i in range(len(h)):
        for j in range(len(h[i])):
            if h[i][j]>=0.5:
                h[i][j]=1
            else:
                h[i][j]=0
    return h

def getCost(x,y,a3):
    cost = 0
    h = a3
    for i in range(inpNum):
        for j in range(len(y[i])):
            if h[i][j]==1:
                h[i][j] = 1 - 10**(-5)
            if h[i][j]==0:
                h[i][j] = 10**(-5)
            cost += ( y[i][j]*math.log(h[i][j]) + (1-y[i][j])*math.log(1-h[i][j]) )
    cost = cost*(-1/inpNum)
    return cost

##--MAIN--##

x,y,testX,testY=getData()
w,b = initNet()

cost=[]
for i in range(iterations):
    a=train(x,y,w,b)
    cost.append(getCost(x,y,a))
print(cost[0],'->',cost[-1])

#testing
h = test(testX,w,b)
count=0
for i in range(len(h)):
    if np.array_equal(h[i],testY[i]):
        count+=1
print('test accuracy:',100*count/testNum,'%')

#testing
h1 = test(x,w,b)
count1=0
for i in range(len(h1)):
    if np.array_equal(h1[i],y[i]):
        count1+=1
print('train accuracy:',100*count1/inpNum,'%')

#plot cost
plt.plot(cost)
plt.show()
