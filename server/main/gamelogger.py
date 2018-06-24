import os
import datetime

class GameLogger:
    """This Class loggs the game"""

    def __init__(self):
        self.mLogString = "" 

    # # remove or rename
    # def setGameLog(self, pGameLogger):
    #     """Setter for self.mLogString."""
    #     self.mLogString = pGameLogger

    # # remove or rename
    # def getGameLog(self):
    #     """Getter for self.mLogString. returns string"""
    #     return self.mLogString 

    def addString(self, pString):
        """adds a String to the logstring"""
        self.mLogString += "\n"+ pString
        print("\n"+ pString)

    def clear(self):
        """clears the log by setting it to empty string """
        self.mLogString = ""
    
    def writeLog(self):
        """opens a text file"""
                       
        now = datetime.datetime.now()
        path = '././gamelogs/'
        timestamp = '{}-{}-{}-{}{}{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        prefixFilename = str(path+timestamp)
        filename = prefixFilename + ".txt"

        with open(filename, "w") as textfile:
            textfile.write(self.mLogString)
    
        decksyspath = os.path.abspath(path)
        print("Game log saved in directory \"" + decksyspath + "\" as " + timestamp +".txt")