from Avatar import Avatar

class Summary():

    def __init__(self, host=None):
        self.summary = []
        if host:
            self.host = host
        else:
            self.host = Avatar()

    def addSummary(self, word, attempts):
        entry = [word, attempts]
        self.summary.append(entry)

    def showSummary(self):
        if len(self.summary) <= 0:
            self.host.say("You have not attempted any words.  I cannot summarise your efforts")
        else:
            self.host.say(f"Ok. Here is a summary of your words and the number of attempts to spell each word")
            for entry in self.summary:
                [word, attempts] = entry
                self.host.say(f"You spelt '{word}' after {attempts} attempts")

    def getSummary(self):
        return self.summary

def main():
    gameSummary = Summary()
    gameSummary.addSummary("apple", 4)
    gameSummary.addSummary("pear", 2)

    gameSummary.showSummary()

if __name__=="__main__":
    main()