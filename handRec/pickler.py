#!/usr/bin/python3

import os,pickle,shelve

db = shelve.open("./weights")
theta = db['theta']
db2 = shelve.open("./weights1")
theta1 = db2['theta']
db3 = shelve.open("./weights2")
theta2 = db3['theta']

with open('pickledW1','wb') as f:
    pickle.dump(theta,f)


with open('pickledW2','wb') as f:
    pickle.dump(theta1,f)

with open('pickledW3','wb') as f:
    pickle.dump(theta2,f)

