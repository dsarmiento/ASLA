import serial
import sys
import glob
from datetime import datetime

BluetoothName = "Test"

def main():
    com = None
    results = serial_ports()
    for port, name in results:
        if name == BluetoothName:
            com = serial.Serial(port)
    if com is None:
        print 'No bluetooth found'
        return

    # Start logging
    filename = str(datetime.now().strftime('%m-%d-%Y %I%M%p'))
    filename += '.csv'
    log = open(filename, 'w')
    flag = True
    while flag:
        if com.in_waiting > 0:
            buf = com.read_all()
            log.write(buf)
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
            name = s.name
            s.close()
            result.append((port, name))
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    main()