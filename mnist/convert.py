#!/usr/bin/python3
from mnist import MNIST

data = MNIST('/home/manan/ml/digit_recognizer')
image,label = data.load_training()
new_label = []

for i in range(len(label)):
    new_label.append([])
    for j in range(9+1):
        if j == label[i]:
            new_label[i].append(1)
        else:
            new_label[i].append(0)
    for j in range(26):
        new_label[i].append(0)

for i in range(10):
    for j in range(len(image[i])):
        print(image[i][j],end=' ')
    for j in range(len(new_label[i])):
        print(new_label[i][j],end=' ')
    print('')
