import serial
import sys
import glob
import time
from sklearn import svm

import DataGenerator


def main():
    clf = svm.NuSVC()

    flag = True
    X = []
    y = []

    while flag:
        print "1. Translate"
        print "2. Learn"
        print "3. Quit"
        choice = raw_input("Choose an option: ")
        print

        if choice == '1':
            choice = raw_input("Letter?")
            if choice == 'A':
                print clf.predict(DataGenerator.genA())
            if choice == 'B':
                print clf.predict(DataGenerator.genB())
            if choice == 'C':
                print clf.predict(DataGenerator.genC())
            if choice == 'D':
                print clf.predict(DataGenerator.genD())
            if choice == 'E':
                print clf.predict(DataGenerator.genE())
        elif choice == '2':
            X, y = DataGenerator.genLearning()
            clf.fit(X, y)
        elif choice == '3':
            flag = False


if __name__ == '__main__':
    flag = True
    main()