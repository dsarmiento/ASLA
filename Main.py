import serial
import sys
import glob
import time
from sklearn import svm
import numpy as np


BLUETOOTH_NAME = "COM4"
flag = True


def main():
    global flag
    file = open("Test.txt", 'r')

    com = connect()
    clf = svm.NuSVC(kernel='poly', degree=5)
    X = []
    y = []

    while flag:
        print "1. Translate"
        print "2. Learn"
        print "3. Quit"
        choice = raw_input("Choose an option: ")
        print

        if choice == '1':
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
            data = data[:5]
            print data
            data = np.array(data)
            data = data.reshape(1, -1)
            print clf.predict(data)

        if choice == '2':
            for i in range(4):
                if i == 0:
                    result = 'A'
                if i == 1:
                    result = 'B'
                if i == 2:
                    result = 'C'
                if i == 3:
                    result = 'D'
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
                    data = data[:5]
                    print data
                    X.append(data)
                    y.append(result)

            print y
            X = np.array(X)
            y = np.array(y)
            clf.fit(X, y)
        if choice == '3':
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