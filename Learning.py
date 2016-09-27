import serial
import sys
import glob
import time
from threading import Thread
from sklearn import svm

BLUETOOTH_NAME = "COM8"
capture = False
flag = True
learning = True

lock = False

def main():
    global capture
    global flag
    global Learning

    com = connect()
    clf = svm.SVC()
    X = []
    y = []


    while flag:
        if learning:
            com.write('y')
            if com.in_waiting > 0:
                data = com.read_until()
                if capture:
                    data = data[:-2]
                    data = data.split(',')
                    capture = False
                    X.append(data)
                    print data
                    number = raw_input("Number: ")
                    y.append(number)

        else:
            if not X == None:
                print y
                clf.fit(X, y)
                X = None

            com.write('y')
            if com.in_waiting > 0:
                data = com.read_until()
                data = data[:-2]
                data.split(',')
                if capture:
                    capture = False
                    print clf.predict(data)


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

def capture_thread(arg):
    global capture
    global flag
    global learning

    while flag:
        input = raw_input("Cmd: ")
        if input == 'c':
            capture = True
        if input == 's':
            learning = False
        if input == 'q':
            flag = False
        while capture:
            cnt = 0

if __name__ == '__main__':
    flag = True
    capture_thread = Thread(target = capture_thread, args = (None, ))
    capture_thread.start()
    main()
