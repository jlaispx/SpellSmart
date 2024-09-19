# Person Class - handles attributes and methods for a Person

# may extend Avatar to get the say and listen features

# needs Natural Language Processing (NLP) - using Spacy and Medium size English Model
import spacy
import en_core_web_sm
from Avatar import Avatar

class Person(Avatar):

    def __init__(self,name=None,vix=1): #Default Male voice
        super().__init__(None,True,vix)  # use Avatar parent to speak and listen
        self.loadSpacy()
        if name:
            self.setName(name)
        else:
            self.askName()

    def loadSpacy(self):
        self.__nlp = spacy.load("en_core_web_sm")  # en_core_web_md.load()

    def getName(self):
        return self.personName

    def setName(self,name=None):
        self.personName = title(name)

    def askName(self):
        self.personName = None
        while self.personName==None:
            speech = self.say("Please tell me your name? ",show=False)
            speech = self.listen(">",useSR=True, show=False)
            self.personName = self.extractName(speech)
            if self.personName == "Unknown":
                self.personName = None
                self.say("Sorry, I did not get your name. ",show=False)

    def extractName(self, speech):
        name = []
        doc = self.__nlp(speech.title()+" And")
        # Parts of Speech (POS) Tagging
        for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.tag_,
            #          token.dep_, token.shape_, token.is_alpha, token.is_stop)
            if token.pos_ in ["PROPN"]:
                #print("found one")
                name.append(token.text)
        if len(name) > 0:
            name = " ".join(name).strip()
        else:
            name = "unknown"
        #print(f" 2: {name}")
        return name.title()

    def introduce(self,otherPerson=None):
        if otherPerson:
            self.say(f"Hi {otherPerson.getName()}. My name is {self.getName()}.")
        else:
            self.say(f"Hi there, my name is {self.getName()}")

    def greet(self):
        self.say(f"Hi {self.getName()}. Welcome on board")

def main():
    george = Person()
    george.greet()
    peter = Person("Peter")
    peter.greet()
    peter.introduce(george)

if __name__ == "__main__":
    main()
