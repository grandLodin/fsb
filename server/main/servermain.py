import sys

class ServerMain():
    """ Class Main for server """

    if __name__=='__main__':
        sys.path.append('././')

    from server.main.fight import Fight
    
    fight = Fight()
    fight.mGameLogger.writeLog()
    input("Press the any key to continue...")
    