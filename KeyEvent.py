from threading import Thread

capture = False
def capture_thread(arg):
    global capture
    while not capture:
        if arg == raw_input():
            print "In if"
            capture = True

def logging_thread(arg):
    global list
    while not capture:
        cnt = 0
    print "Capture"

if __name__ == "__main__":
    capture_thread = Thread(target = capture_thread, args = ('c', ))
    logging_thread = Thread(target = logging_thread, args = (None, ))
    capture_thread.start()
    logging_thread.start()
    logging_thread.join()