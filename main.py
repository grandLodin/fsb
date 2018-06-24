import sys
sys.path.append('././')
from client.main.modeselector import ModeSelector

if __name__ == '__main__':
    loop = True
    while loop:
        loop = ModeSelector().mLoop
        