import serial
import sys
import glob
import time

BLUETOOTH_NAME = "COM7"
DATA_RATE = 100
SIGN_LENGTH = 3
SAMPLE_LENGTH = 20
SLOPE_THRESHOLD = 50

def main():
    print "1. Connect"
    print "2. Translate"
    print "3. Learn/Log"
    print "4. Quit"
    choice = input("Choose an option: ")
    print

    if choice == 1:
        com = connect()
    if choice == 2:
        print "Not supported"
    if choice == 3:
        print "Logging started"

        # Start logging
        filename = str(time.strftime('%m-%d-%Y %I%M%p'))
        filename += '.csv'
        print filename

        log = open(filename, 'w')
        flag = True
        dataBuf = []
        cnt = 0
        while flag:
            if com.in_waiting > 0:
                temp = com.read_until()
                cnt += 1
                log.write(temp)
                temp = temp.split(',')
                dataBuf.append(temp)
                if dataBuf.__sizeof__() > DATA_RATE * SIGN_LENGTH:
                    dataBuf = dataBuf[1:]
                if cnt > 999 :
                    flag = False

        # Close everything we opened
        com.close()
        log.close()

    if choice == 4:
        return False
    return True

def movement(data):
    for i in range(0, DATA_RATE):
        slope = float(data[i+SAMPLE_LENGTH] - data[i]) / float(SAMPLE_LENGTH)
        if abs(slope) > SLOPE_THRESHOLD:
            return True
    return False


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
            com = serial.Serial(port)
            return com
    if com is None:
        print 'No bluetooth found'
        return 0


if __name__ == '__main__':
    flag = True
    while flag:
        flag = main()
        print