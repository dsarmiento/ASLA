import serial
import sys
import glob
import time
import os.path
import pickle
from sklearn import svm
import numpy as np


BLUETOOTH_NAME = "COM4"
flag = True

def main():
    global flag

    com = connect()
    clf = svm.NuSVC(kernel = 'poly', degree = 3)
    X = []
    y = []

    while flag:
        print "1. Learn"
        print "2. Translate"
        print "3. Quit"
        choice = raw_input("Choose an option: ")
        print
        if choice == '1':
            filename = "letters.sav"
            if os.path.exists(filename):
                print "A previously saved library was found,",
                print "would you like to use it? Y/N"
                useFile = raw_input()
            else:
                useFile = 'N'
            if useFile == 'N' or useFile == 'n':
                for result in range(26):
                    result = chr(ord('A') + result)
                    print "Learning ", result
                    raw_input("Ready?")
                    for j in range(5):
                        com.flushOutput()
                        com.flushInput()
                        com.write('y')
                        time.sleep(.2)
                        temp = com.read_until()
                        temp = temp[:-2]
                        temp = temp.split(',')
                        data = []
                        for item in temp:
                            data.append(float(item))
                        print data
                        X.append(data)
                        y.append(result)
                        time.sleep(.2)

                X = np.array(X)
                y = np.array(y)
                clf.fit(X, y)
                pickle.dump(clf, open(filename, 'wb'))
            elif useFile == 'Y' or useFile == 'y':
                clf = pickle.load(open(filename, 'rb'))

        elif choice == '2':
            print "Press enter to translate"
            print "Q to quit"
            translate = raw_input()
            while translate != 'Q' or translate != 'q':
                com.flushOutput()
                com.flushInput()
                com.write('y')
                time.sleep(.2)
                temp = com.read_until()
                temp = temp[:-2]
                temp = temp.split(',')
                data = []
                for item in temp:
                    data.append(float(item))
                print data
                data = np.array(data)
                data = data.reshape(1, -1)
                print clf.predict(data)
                translate = raw_input()
        elif choice == '3':
            flag = False
            com.close()

    return

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

def connect():
    # Open the right COM port
    com = None
    results = serial_ports()
    for port in results:
        if port == BLUETOOTH_NAME:
            com = serial.Serial(port, 115200)
            return com
    if com is None:
        print 'No bluetooth found'
        return 0


if __name__ == '__main__':
    flag = True
    main()