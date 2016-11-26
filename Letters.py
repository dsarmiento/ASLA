import serial
import sys
import glob
import time
import os.path
import pickle
import pyttsx
from sklearn import svm
import numpy as np


GLOVE_PORT = "COM4"
GLOVE_BAUD = 115200
TTS = pyttsx.init()

def main():
    flag = True
    com = connect()
    clf = svm.NuSVC(kernel = 'poly', degree = 5)
    dataFileName = "letters.csv"
    modelFileName = "letters.sav"
    X = []
    y = []

    while flag and com != None:
        print "1. Learn"
        print "2. Translate"
        print "3. Quit"
        choice = raw_input("Choose an option: ")
        print

        # Learn the letters
        if choice == '1':
            # Find if a library exists
            if os.path.exists(modelFileName):
                print "A previously saved library was found, would you like to use it",
                print "(this will overwrite your previous library)? Y/N"
                useFile = raw_input()
            else:
                useFile = 'N'

            # Didn't find one or chose to remake one
            if useFile == 'N' or useFile == 'n':
                # Create the empty file
                open(dataFileName, 'w').close()

                # Learn all of the letters at once
                for result in range(26):
                    result = chr(ord('A') + result)
                    print "Learning ", result
                    raw_input("Ready?")
                    for j in range(5):
                        data = grabGloveData(com, dataFileName, result)
                        X.append(data)
                        y.append(result)
                        time.sleep(.2)

                # Close the file and create a model
                X = np.array(X)
                y = np.array(y)
                clf.fit(X, y)
                pickle.dump(clf, open(modelFileName, 'wb'))

            # Found one and we are using it
            elif useFile == 'Y' or useFile == 'y':
                addLib = raw_input("Would you like to add to the library? (Y/N)")

                # Adding to the library
                if addLib == 'Y' or addLib == 'y':
                    trainingData = open(dataFileName, 'r')
                    stillReading = True

                    # Read everything we have learned so far
                    while stillReading:
                        temp = trainingData.readline()
                        if temp != "":
                            temp = temp.split(',')
                            result = temp[len(temp) - 1]
                            temp.remove(result)
                            result = result[0]
                            data = []
                            for item in temp:
                                data.append(float(item))
                            X.append(data)
                            y.append(result)
                        else:
                            stillReading = False
                    trainingData.close()

                    # Done reading, time to add letters
                    print "Ready? Type 'q-' as an input to quit."
                    result = raw_input("Input?")
                    while result != 'q-':
                        for j in range(5):
                            data = grabGloveData(com, dataFileName, result)
                            X.append(data)
                            y.append(result)
                            time.sleep(.2)
                        result = raw_input("Input?")

                    # Close the file and create a model
                    trainingData.close()
                    X = np.array(X)
                    y = np.array(y)
                    clf.fit(X, y)
                    pickle.dump(clf, open(modelFileName, 'wb'))

                # Load the model
                elif addLib == 'N' or addLib == 'n':
                    clf = pickle.load(open(modelFileName, 'rb'))


        # Start translating
        elif choice == '2':
            print "Press enter to translate"
            print "Q to quit"
            translate = raw_input()

            while translate != 'Q' and translate != 'q':
                data = grabGloveData(com, None, None)
                data = np.array(data)
                data = data.reshape(1, -1)
                result = clf.predict(data)
                print result
                TTS.say(result)
                TTS.runAndWait()
                translate = raw_input()

        # Terminate Program
        elif choice == '3':
            flag = False
            com.close()

    return


# Grab glove data, save it if we are learning
def grabGloveData(com, dataFileName, result):
    com.flushOutput()
    com.flushInput()
    com.write('y')
    time.sleep(.2)

    temp = com.read_until()
    temp = temp[:-2]

    if dataFileName != None:
        trainingData = open(dataFileName, 'a')
        trainingData.write(temp)
        trainingData.write(',')
        trainingData.write(result)
        trainingData.write('\n')
        trainingData.close()

    temp = temp.split(',')
    data = []
    for item in temp:
        data.append(float(item))

    print data
    return data


# List all connected serial ports and names
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Find the right COM port and open it
def connect():
    com = None
    results = serial_ports()
    for port in results:
        if port == GLOVE_PORT:
            com = serial.Serial(port, GLOVE_BAUD)
    if com is None:
        print "No glove found terminating program"
        print "Press enter to continue"
        raw_input()
    return com


if __name__ == '__main__':
    flag = True
    main()