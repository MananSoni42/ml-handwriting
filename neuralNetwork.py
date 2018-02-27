#!/usr/bin/python3

import numpy,sys,os,openpyxl,pprint
import numpy as np
import copy

if(len(sys.argv)<3):
    print("Usage: ./neuralNetwork.py fileName rate cycles")
    sys.exit(1)

cycles=int(sys.argv[3])
alpha = float(sys.argv[2])
filename = os.path.join(".",str(sys.argv[1]))

def getData():
    #extract data from txt file
    data =  []
    x = []
    y = []
    for i in range(inpNum):
        data = input().split()
        for j in range(outSize):
            y.append(float(data[-j-1]))
        for j in range(inpSize):
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
        for j in range(inpSize):
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

def calcG(theta,x):
    z = theta.dot(x)
    sig = 1/(1+numpy.exp(-z))
    del z
    return sig

def calcGPrime(a):
    return a*(1-a)

def calcDelta(a,prevdelta,thetaMatrix):
    #return thetaMatrix.T.dot(prevdelta[1:,:])*(calcGPrime(a[:,:]))
    return  (thetaMatrix.T.dot(prevdelta)*(calcGPrime(a)))[1:]

def calcC(theta,predictedOutput,Y,numSamples=None,numLayers=None,regParam=None):
    if regParam == None:
        regParam = 0
    if numSamples == None:
        numSamples = Y.shape[1]
    if numLayers == None:
        numLayers = len(theta)+1
    cost = 0
    Y= Y.T
    H = numpy.log(predictedOutput)
    Hprime = numpy.log(1-predictedOutput)
    for i in range(numSamples):
        cost = cost + Y[i,:].dot(H[:,i])+(1-Y[i,:]).dot(Hprime[:,i])

    for i in range(numLayers-1):
        cost = cost + regParam*(theta[i][:,1:].dot(theta[i][:,1:].T)).sum()
    return cost/numSamples

def forwardPropogation(X,neurons,theta,numLayers=None):
    if(numLayers==None):
        numLayers=len(neurons)
    a = [X]
    for i in range(numLayers-1):
        a[i]=numpy.insert(a[i],0,1,axis=0)
        a.append(calcG(theta[i],a[i]))
    return a

def backPropogation(theta,Y,a,numLayers=None,numSamples=None,numVars=None,regParam=None):
    if(regParam == None):
        regParam = 0
    if(numLayers ==None):
        numLayers = len(a)
    if(numSamples==None):
        numSamples = Y.shape[1]
    if(numVars==None):
        numVars= Y.shape[0]
    delta = []
    delta.append(Y-a[-1])
    der = []
    for i in range(1,numLayers):
        delta.append(calcDelta(a[-i-1],delta[-1],theta[-i]))
        der.append(delta[-2].dot(a[-i-1].T))
        der[-1][:,1:]=der[-1][:,1:]+theta[-i][:,1:]*regParam
        der[-1]=der[-1]/numSamples
    der=list(reversed(der))
    return der

def updateTheta(theta,alpha,der,numLayers=None):
    if numLayers == None:
        numLayers = len(theta)+1
    for i in range(numLayers-1):
        theta[i]=theta[i]-alpha*der

def gradCheck(theta,a,Y,eps,neurons):
    der=backPropogation(theta,Y,a)
    derEst=[]
    print(der)
    print("Estimate")
    for i in range(len(theta)):
        derEst.append(numpy.zeros((theta[i].shape)))
        for k in range(theta[i].shape[0]):
            for l in range(theta[i].shape[1]):
                theta1 , theta2 = copy.deepcopy(theta), copy.deepcopy(theta)
                theta1[i][k][l]=theta[i][k][l]+eps
                a1=forwardPropogation(X,neurons,theta1)
                theta2[i][k][l]=theta[i][k][l]-eps
                a2=forwardPropogation(X,neurons,theta2)
                derEst[i][k][l]=(calcC(theta1,a1[-1],Y)-calcC(theta2,a2[-1],Y))/(2*eps)
    print(derEst)

#metaparameters
inpNum = 900
testNum = 100
inpSize = 784
outSize = 10

X, Y,tx,ty = getData()
numSamples=Y.shape[0]
numVars =X.shape[1]
numOutputs = Y.shape[1]
X=X.T
Y=Y.T
NEURONS = [numVars,559,numOutputs]
NUMLAYERS = len(NEURONS)
THETA = []

for i in range(NUMLAYERS-1):
    THETA.append(numpy.random.random((NEURONS[i+1],NEURONS[i]+1))*2-1)
A = forwardPropogation(X,NEURONS,THETA)
A = forwardPropogation(X,NEURONS,THETA)
A = forwardPropogation(X,NEURONS,THETA)
#gradCheck(THETA,A,Y,0.001,NEURONS)
