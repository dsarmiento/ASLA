import serial
import sys
import glob
import time
from sklearn import svm
from threading import Thread
from threading import Lock


BLUETOOTH_NAME = "COM4"
lock = Lock()

def main():
    clf = svm.SVC()
    global com

    com = connect()
    flag = True
    X = []
    y = []

    if com == 0:
        return

    while flag:
        print "1. Translate"
        print "2. Learn"
        print "3. Quit"
        choice = raw_input("Choose an option: ")
        print

        LOG = False
        if choice == '1':
            while choice != 'n':
                com.flushOutput()
                com.flushInput()
                com.write('y')
                time.sleep(.2)
                if com.in_waiting > 0:
                    data = com.read_until()
                    data = data[:-2]
                    data = data.split(',')
                    data = data[:5]
                    print data
                    responce = clf.predict(data)
                    print responce
                    choice = raw_input("Continue? y/n")
        if choice == '2':
            while choice != 'qq':
                com.flushOutput()
                com.flushInput()
                com.write('y')
                time.sleep(.2)
                if com.in_waiting > 0:
                    data = com.read_until()
                    data = data[:-2]
                    data = data.split(',')
                    data = data[:5]
                    print data
                    choice = raw_input("Letter?")
                    print choice
                    if choice != 'qq':
                        X.append(data)
                        y.append(choice)
            print y
            clf.fit(X, y)
        if choice == '3':
            flag = False
            com.close()


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
        print 'No glove found'
        return 0


if __name__ == '__main__':
    flag = True
    main()