# ml-handwriting
A simple handwriting recognizing tool that works on multi-line images

## Overview
  * We run a basic (self-made) edge detection on the image to identify the bounding boxes of each letter/number
  * Each bounding box is then converted to a grayscale 28*28 image
  * (The aspect ratio is approximately conserved and the bounding box is centered in the 28*28 image)
  * We generate 2 text files image_t.txt ( contains 28*28 image as pixels(0-255) ) and image_s.txt (contains the sentence structure)
  * all this is done by running:
  ```handRec/source/detect.py <Path to image>```
  * Then image_t.txt is given as an input to a neural network with 2 hidden layers 
  * Net 1 - [784,500,300,36] - trained on 120000 digits and 120000 letters from the EMNIST database
  * this is done by running:
  ```handRec/source/finalInterpreter.py image_t.txt image_s.txt weights```
  * (weights are the trained weights of the neural net stored as python shelve files)

## Installation  
  * Install pip on your system
     * Debian/Ubuntu - ```sudo apt-get update && apt install python3-pip```
     * CentOs/RHEL   - ```sudo yum install epl-release && yum install python3-pip```
     * Fedora        - ```sudo yum install python3-pip```
     * Arch          - ```pacman -S python3-pip```
     * openSUSE      - ```zypper install python3-pip``` 
  * To install the required dependancies run ```./setup```  
  * a New directory named handRec will be created in your home directory
  * You can safely remove ml-handwriting directory 
  * To uninstall, run ```./uninstall.py```
  
## Supported OS 
   GNU/Linux

## Usage
  * Navigate to your handRec directory
  * Run ```./recognize <Path to Image>```  

## Authors
  - **Manan Soni** - [MananSoni42](https://github.com/MananSoni42/)
  - **Siddharth Singh** - [coolSidd](https://github.com/coolsidd)  
  
## Acknowledgements
  - EMNIST parser - [sorki](https://github.com/sorki)
  - Machine Learning Theory - [Cousera](https://www.coursera.org/learn/machine-learning)
