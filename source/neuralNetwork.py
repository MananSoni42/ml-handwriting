#!/usr/bin/python3

import numpy,sys,os,openpyxl,pprint
import numpy as np
import copy
import matplotlib.pyplot as plt
import shelve

if len(sys.argv) != 4+1:
    print("Usage: ./neuralNetwork.py File rate iterations lambda")
    sys.exit(1)

CYCLES=int(sys.argv[3])
ALPHA = float(sys.argv[2])
REGPARAM = float(sys.argv[4])
inFile = open(sys.argv[1],'r')

def getData(inFile):
    #extract data from txt file
    data =  []
    x = []
    y = []
    for i in range(inpNum):
        data = inFile.readline().split()
        for j in range(inpSize,len(data)):
            y.append(float(data[j]))
        for j in range(inpSize):
            x.append(float(data[j]))
        del data
    #extract test data
    data =  []
    tx = []
    ty = []
    for i in range(testNum):
        data = inFile.readline().split()
        for j in range(inpSize,len(data)):
            ty.append(float(data[j]))
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

    for i in range(predictedOutput.shape[0]):
        for j in range(predictedOutput.shape[1]):
            if predictedOutput[i][j]==1:
                predictedOutput[i][j] = 1 - 10**(-5)
            if predictedOutput[i][j]==0:
                predictedOutput[i][j] = 10**(-5)

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
inpNum =  8000
testNum = 2000
inpSize = 784
outSize = 36

##-- MAIN --##
print('Loading Data...')
X, Y,tx,ty = getData(inFile)

print('Done')
NUMSAMPLES=Y.shape[0]
NUMVARS =X.shape[1]
NUMOUTPUTS = Y.shape[1]
X=X.T
Y=Y.T
tx=tx.T
ty=ty.T
NEURONS = [NUMVARS,559,NUMOUTPUTS]
NUMLAYERS = len(NEURONS)
THETA = []

#shelve weights
db = shelve.open('weights')
try:
    THETA = db['theta']
    print('\nfound weights from shelve file - weights')
except KeyError:
    print('\ncould not find weights, generating random weights')
    for i in range(NUMLAYERS-1):
        THETA.append(numpy.random.random((NEURONS[i+1],NEURONS[i]+1))*2-1)
    db['theta'] = THETA

A = forwardPropogation(X,NEURONS,THETA,NUMLAYERS)
DER , DELTA = backPropogation(THETA,Y,A,NUMLAYERS,NUMSAMPLES,NUMVARS,REGPARAM)

cost=[]
print('\nTraining')
for i in range(CYCLES):
    print(str(i)+"/"+str(CYCLES))
    forwardPropogation(X,NEURONS,THETA,NUMLAYERS,A)
    backPropogation(THETA,Y,A,NUMLAYERS,NUMSAMPLES,NUMVARS,REGPARAM,DER,DELTA)
    updateTheta(THETA,ALPHA,DER,NUMLAYERS)
    cost.append(calcC(THETA,A[-1],Y))

#testing
print('\nTesting...')

A = forwardPropogation(X,NEURONS,THETA,prevA=None)
A[-1] = A[-1].T
Y = Y.T
count = 0
for i in range(A[-1].shape[0]):
    m = max(A[-1][i])
    m -= 0.01
    for j in range(A[-1].shape[1]):
        if A[-1][i][j] >= m and m>=0.5:
            A[-1][i][j] = 1
        else:
            A[-1][i][j] = 0
    if np.array_equal(Y[i],A[-1][i]):
        count+=1

A = forwardPropogation(tx,NEURONS,THETA,prevA=None)
count2 = 0
A[-1] = A[-1].T
ty = ty.T
for i in range(A[-1].shape[0]):
    m = max(A[-1][i])
    m -= 0.01
    for j in range(A[-1].shape[1]):
        if A[-1][i][j] >= m and m>=0.5:
            A[-1][i][j] = 1
        else:
            A[-1][i][j] = 0
    if np.array_equal(A[-1][i],ty[i]):
        count2+=1

print('Done')

print('\nSaving weights to shelve - weights')
db['theta'] = THETA

print('\nResults:')
print('cost:',cost[0],'->',cost[-1])
print("Testing accuracy: ",100*count2/(ty.shape[0]))
print("Training accuracy: ",100*count/(Y.shape[0]))

#plt.plot(cost)
#plt.show()
