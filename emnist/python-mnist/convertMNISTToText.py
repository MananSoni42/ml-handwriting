from mnist import MNIST
DATABASE ="./ml/ml-handwriting/emnist/python-mnist/emnist_data"
PATH_TO_FILE =""
file= open(PATH_TO_FILE,"w")
mndata = MNIST(DATABASE)
mndata.select_emnist('digits')
images, labels = mndata.load_training()
for i in range(len(images)):
    print(i)
    for j in range(36):
        if labels[i]==j:
            file.write('1',end=' ')
        else:
            file.write('0',end=' ')
    file.write(images[i])

mndata.select_emnist('letters')
images, labels = mndata.load_training()
for i in range(len(images)):
    print(i)
    for j in range(36):
        if labels[i]+9==j:
            file.write('1',end=' ')
        else:
            file.write('0',end=' ')
    file.write(images[i])
