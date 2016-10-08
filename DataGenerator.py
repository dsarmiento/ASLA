import random

def genLearning():
    X = []
    y = []
    for i in range(5):
        data = []
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        X.append(data)
        y.append('A')
    for i in range(5):
        data = []
        data.append(random.randrange(425, 475))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        X.append(data)
        y.append('B')
    for i in range(5):
        data = []
        data.append(random.randrange(425, 475))
        data.append(random.randrange(425, 475))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        X.append(data)
        y.append('C')
    for i in range(5):
        data = []
        data.append(random.randrange(575, 650))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        X.append(data)
        y.append('D')
    for i in range(5):
        data = []
        data.append(random.randrange(425, 475))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        data.append(random.randrange(575, 650))
        data.append(random.randrange(425, 475))
        X.append(data)
        y.append('E')
    return X, y


def genA():
    data = []
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    return data

def genB():
    data = []
    data.append(random.randrange(425, 475))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    return data

def genC():
    data = []
    data.append(random.randrange(425, 475))
    data.append(random.randrange(425, 475))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    return data

def genD():
    data = []
    data.append(random.randrange(575, 650))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    return data


def genE():
    data = []
    data.append(random.randrange(425, 475))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    data.append(random.randrange(575, 650))
    data.append(random.randrange(425, 475))
    print data
    return data