import serial
import sys
import glob
import time

BLUETOOTH_NAME = "Test"
DATA_RATE = 100
SIGN_LENGTH = 3
SAMPLE_LENGTH = 20
SLOPE_THRESHOLD = 50

def main():
    # Open the right COM port
    com = None
    results = serial_ports()
    for port, name in results:
        if name == BLUETOOTH_NAME:
            com = serial.Serial(port)
    if com is None:
        print 'No bluetooth found'
        return

    # Start logging
    filename = str(time.strftime('%m-%d-%Y %I%M%p'))
    filename += '.csv'
    log = open(filename, 'w')
    flag = True
    dataBuf = []
    while flag:
        if com.in_waiting > 0:
            temp = com.read_until()
            temp = temp.split(',')
            dataBuf.append(temp)
            if dataBuf.__sizeof__() > DATA_RATE * SIGN_LENGTH:
                dataBuf = dataBuf[1:]

            movement(dataBuf)
            log.write(temp)

    # Close everything we opened
    com.close()
    log.close()
    return

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
            name = s.name
            s.close()
            result.append((port, name))
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    main()