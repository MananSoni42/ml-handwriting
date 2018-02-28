#!/usr/bin/python3

import numpy,sys,os,openpyxl,pprint
import numpy as np
import copy

if(len(sys.argv)<3):
    print("Usage: ./neuralNetwork.py rate iterations lambda")
    sys.exit(1)

CYCLES=int(sys.argv[2])
ALPHA = float(sys.argv[1])
REGPARAM = float(sys.argv[3])

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
        cost = cost - Y[i,:].dot(H[:,i])-(1-Y[i,:]).dot(Hprime[:,i])

    for i in range(numLayers-1):
        cost = cost + regParam*(theta[i][:,1:].dot(theta[i][:,1:].T)).sum()
    return cost/numSamples

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

def backPropogation(theta,Y,a,numLayers=None,numSamples=None,numVars=None,regParam=None,der=None,delta=None):
    if(regParam == None):
        regParam = 0
    if(numLayers ==None):
        numLayers = len(a)
    if(numSamples==None):
        numSamples = Y.shape[1]
    if(numVars==None):
        numVars= Y.shape[0]
    if(der==None or delta==None):
        del der
        del delta
        der=[]
        delta = []
        delta.append(a[-1]-Y)
        for i in range(1,numLayers):
            delta.append(calcDelta(a[-i-1],delta[-1],theta[-i]))
            der.append(delta[-2].dot(a[-i-1].T))
            der[-1][:,1:]=der[-1][:,1:]+theta[-i][:,1:]*regParam
            der[-1]=der[-1]/numSamples
        delta=list(reversed(delta))
        der=list(reversed(der))
    else:
        delta[-1]=(a[-1]-Y)
        for i in range(1,numLayers):
            delta[-i-1]=calcDelta(a[-i-1],delta[-i],theta[-i])
            der[-i]=(delta[-i].dot(a[-i-1].T))
            der[-i][:,1:]=der[-i][:,1:]+theta[-i][:,1:]*regParam
            der[-i]=der[-i]/numSamples


    return der,delta

def updateTheta(theta,alpha,der,numLayers=None):
    if numLayers == None:
        numLayers = len(theta)+1
    for i in range(numLayers-1):
        theta[i]=theta[i]-alpha*der[i]

def gradCheck(theta,a,Y,eps,neurons):
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
inpNum = 4
testNum = 1
inpSize = 2
outSize = 2

X, Y,tx,ty = getData()
NUMSAMPLES=Y.shape[0]
NUMVARS =X.shape[1]
NUMOUTPUTS = Y.shape[1]
X=X.T
Y=Y.T
NEURONS = [NUMVARS,559,NUMOUTPUTS]
NUMLAYERS = len(NEURONS)
THETA = []

print(tx)

for i in range(NUMLAYERS-1):
    THETA.append(numpy.random.random((NEURONS[i+1],NEURONS[i]+1))*2-1)

A = forwardPropogation(X,NEURONS,THETA,NUMLAYERS)
DER , DELTA = backPropogation(THETA,Y,A,NUMLAYERS,NUMSAMPLES,NUMVARS,REGPARAM)

print("INITIAL THETA : "+str(THETA))

for i in range(CYCLES):
    print(str(i)+"/"+str(CYCLES)+"|"+str(i/CYCLES*100))
    forwardPropogation(X,NEURONS,THETA,NUMLAYERS,A)
    backPropogation(THETA,Y,A,NUMLAYERS,NUMSAMPLES,NUMVARS,REGPARAM,DER,DELTA)
    updateTheta(THETA,ALPHA,DER,NUMLAYERS)
    calcC(THETA,A[-1],Y)

print("FINAL THETA : "+str(THETA))

A = forwardPropogation(tx,NEURONS,THETA,prevA=A)
count =0
for i in range(ty.shape[0]):
    for j in range(tx.shape[1]):
        if(A[-1][i][j]>=0.5):
            A[-1][i][j]=1
            if(ty[i][j]==1):
                count+=1
        else:
            A[-1][i][j]=0
            if(ty[i][j]==0):
                count+=1

print("Testing accuracy: ",100*count/ty.shape[0]/tx.shape[1])
