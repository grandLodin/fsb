import sys
sys.path.append('././')
from client.main.modeselector import ModeSelector

class Main():
    """ Class Main for the application """

    if __name__ == '__main__':
        loop = True
        while loop:
            loop = ModeSelector().mLoop

