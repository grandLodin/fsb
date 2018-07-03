import sys


class ServerMain:
    """ Class Main for server """

    if __name__ == '__main__':
        sys.path.append('././')

    from server.main.arena import Arena
    
    fight = Arena()
    fight.mGameLogger.writeLog()
    input("Press the any key to continue...")
