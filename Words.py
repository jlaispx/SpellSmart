import sqlite3
from random import choice

# Class Words manages a wordlist from a database

class Words:

    # Instance Variables
    __wordList = []
    __usedWords = []
    __conn = None
    __dbname = "wordList.db"

    # Constructor Method - called when creating an instance/object of this Class
    def __init__(self,dbname=None):
        if dbname:
            self.__dbname = dbname
        self.__getConnection()
        self.getWordList()

    # Destructor Method - called when destroying an Object/Instance of this Class
    def __del__(self):
        self.__conn = None

    # Create a Connection to the database to be used
    def __getConnection(self):
        try:
            self.__conn = sqlite3.connect(self.__dbname)
        except Exception as e:
            print(f"DB Error: Get Connection error: {e}")

    # Code to run a query
    # Pass in SQL and any parameters
    # SQL includes ? to be replaced by parameters in order.

    def __runQuery(self, sql, parms=None):
        if parms:
            parms=tuple([parms])
        #print(f"sql={sql} parms={parms}")

        self.__conn.row_factory = sqlite3.Row

        cur = self.__conn.cursor()
        if parms:
            cur.execute('PRAGMA case_sensitive_like = false')
            cur.execute(sql,parms)
        else:
            cur.execute(sql)

        rows = cur.fetchall()
        cur.close()
        return rows

    def getWordList(self):
        sql = "SELECT word FROM wordList"

        words = self.__runQuery(sql) #big table of words
        self.__wordList = []
        self.__usedWords = []

        for row in words:  # for each word in word tables
            self.__wordList.append(row['word'])
        #print(self.__wordList)

    def getNextWord(self):
        # get the next word not already used
        if len(self.__wordList)>0:
            word = choice(self.__wordList)  #choose a random word from list
            self.__usedWords.append(word)   #add to used list
            self.__wordList.remove(word)    # remove word to prevent re-use
            return word
        else:
            return None

    def showUsedWords(self):
        print(f"Used words so far are: {self.getUsedWords()}")

    def getUsedWords(self):
        return ', '.join(self.__usedWords)


# Test Harness for Words Class
def main():
    words = Words()

    word = words.getNextWord()
    while word:
        print(f"Next word is '{word}'")
        words.showUsedWords()
        word = words.getNextWord()

if __name__ == "__main__":
    main()
