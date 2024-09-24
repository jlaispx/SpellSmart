from Avatar import Avatar
from Person import Person
from Words import Words
from rapidfuzz import fuzz
import pygame
# from time import Clock, wait
from Summary import Summary

class SpellSmart:

    BLACK = (0,0, 0)
    WHITE = (255,255,255)


    class Teacher(Avatar):

        def __init__(self, win):
            super().__init__("Missus Aberneezer",useSR=False,vix=2) # Female voice
            self.win = win
            self.sw = self.win.get_width()
            self.sh = self.win.get_height()
            self.win = win
            self.img = pygame.image.load("teacher.png") #.convert()
            self.iw = self.img.get_width()
            self.ih = self.img.get_height()
            print("Teacher: screen res", self.sw,self.sh, " teacher img res: ", self.iw, self.ih)
            width = self.iw /2.5
            height = self.ih / 2.5
            print("Teacher: screen res", self.sw,self.sh, " teacher img res: old w&h", self.iw, self.ih,", new w&h: ",width, height)
            self.img = pygame.transform.scale(self.img,(width, height))

        def draw(self, win=None):
            if win:
                self.win = win
            self.win.blit(self.img, (self.sw/2,self.sh/2))

        def say(self,text, show=False):
            super().say(text, show)

    class Student(Person):

        def __init__(self, win):
            super().__init__(vix=2)
            self.win = win

    def __init__(self):  # Constructor - called when creating a new Game
        self.pginit()
        self.clock =pygame.time.Clock()
        self.teacher = self.Teacher(self.win)
        self.drawScreen()

        intro = f"Hello, my name is {self.teacher.getName()}! Welcome to Spell Smart!"
        self.showTeacherText(intro)
        self.teacher.say(intro,False)

        self.words = Words()
        self.showTeacherText("Please introduce yourself.")
        self.student = self.Student(self.win)
        greeting = f"Hello {self.student.getName()}.  Today we are going through your spelling list."

        self.showTeacherText(greeting)
        self.teacher.say(greeting,False)
        self.summary = Summary() #{"word": 4}
        self.maxWords = 5


    def pginit(self):
        ''' This function initialises the pygame screen
        '''
        pygame.init()
        # set initial screen resolution
        info = pygame.display.Info()
        self.w = info.current_w #1600
        self.h = info.current_h #900
        pygame.font.init()
        self.txt_font = pygame.font.SysFont('freesandbold.ttf', 32)

        main_surface = pygame.Surface((self.w, self.h))
        self.win = pygame.display.set_mode((self.w,self.h),pygame.RESIZABLE)
        pygame.display.set_caption("Spell Smart")

        # Add a background image and Stretch it to fit the Surface
        self.background = pygame.image.load("background.jpeg").convert()
        self.background = pygame.transform.scale(self.background,(self.w,self.h))

    def text_objects(self, text):
        textSurface = self.txt_font.render(text, True, self.WHITE)
        return textSurface, textSurface.get_rect()

    def showTeacherText(self,text):
        self.drawScreen()
        TextSurf, TextRect = self.text_objects(text)
        TextRect.center = (self.w/2,self.h/3)
        self.win.blit(TextSurf, TextRect)
        pygame.display.update()
        pygame.time.wait(30)

    def teacherSays(self,text):
        self.showTeacherText(text)
        self.teacher.say(text, False)

    def play(self):
        '''
        Method: Play
        1. Get the first word - this checks if there are any words to spell today
        2. While there are Words to spell...
            2.1 Ask student to spell the word
            2.2 While spelling incorrect and not quit requested
                2.2.1 Loop and Wait for Student to
                    2.2.1.1 ESC key or 'X' the window to Quit - give up
                    2.2.1.2 Space - Repeat the word
                    2.2.1.3 Backspace - remove one char from guess
                    2.2.1.4 Key a-z - add char to guess
        '''
        word = self.words.getNextWord().upper()
        numWords = 1
        while word:
            self.teacherSays("Please spell this next word")
            self.showTeacherText("Please type in your spelling. ENTER to finish, SPACE to repeat Word, ESC to exit.")
            self.teacher.say(word,False)
            guess = ""
            run = True
            quit = False
            attempts = 0
            correct = False


            while  not (correct or quit):  # LOOP FOR EACH WORD
                # Get the correct spell
                while run:                 # LOOP ENTER LETTERS / QUIT / ENTER
                    # GET INPUT FROM SCREEN
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            quit = True
                            break
                        elif event.type == pygame.VIDEORESIZE:
                            self.w = event.w
                            self.h = event.h
                        elif event.type == pygame.KEYDOWN:

                            if event.key == pygame.K_ESCAPE: # ESC quits too
                                run = False
                                quit = True
                                break
                            if event.key == pygame.K_RETURN: # finish entering the word
                                run = False
                                attempts +=1
                                break
                            if event.key == pygame.K_BACKSPACE:
                                letter = guess[-1]
                                guess = guess[:-1]
                                self.teacher.say(f"Removing: {letter}",False)
                                self.showTeacherText(f"Spelling: {guess} (SPACE to repeat Word, ESC to exit)")

                            if event.key == pygame.K_SPACE:
                                self.teacher.say(f"Repeating word again: {word}",False)

                            if event.key in range(pygame.K_a, pygame.K_z + 1):
                                key = event.unicode.upper()
                                guess += key
                                self.showTeacherText(f"Spelling: {guess}   (SPACE to repeat Word, ESC to exit)")
                                self.teacher.say(key,False)
                    # self.drawScreen()

                # OPTION = QUIT, CHECK SPELLING
                if quit:
                    self.teacherSays(f"Oh dear {self.student.getName()}. You are quitting. ")
                    break
                if not run:
                    self.teacherSays(f"Ok , let's check your spelling. ")
                    #self.teacher.say(f"You spelt {word} as")
                    #for letter in guess:
                    #    self.teacherSays(f"{letter}")
                    confidence = fuzz.ratio(guess,word)
                    if confidence < 100:
                        comment = "Well done"
                        if confidence < 80:
                            comment = "Good effort"
                        if confidence < 50:
                            comment = "You could do better"
                        if confidence < 20:
                            comment = "O.M.G. Really!"
                        if confidence < 10:
                            comment = "Horrible. Horrible. Horrible. "
                        self.teacherSays(f"{comment} {self.student.getName()}, you were {confidence:.2f}% correct. Try again.")
                        guess = ""
                        run = True
                    else:
                        self.teacherSays(f"Well done {self.student.getName()}, you got it right!")
                        self.summary.addSummary(word, attempts)
                        correct = True


            word = self.words.getNextWord().upper()
            numWords += 1

            if numWords > self.maxWords:
                break
            if quit:
                break
        self.printSummary()
        pygame.quit()

    def drawScreen(self):
        self.win.blit(self.background, (0,0))
        self.teacher.draw(self.win)

        pygame.display.update()

    def printSummary(self):
        summary = self.summary.getSummary()
        numWordsAttempted = len(summary)
        if numWordsAttempted <= 0:
            self.teacherSays(f"You have not attempted any words.  Please try again next time.")
            self.teacherSays(f"Goodbye {self.student.getName()}")
        else:
            wordCount = (f"{self.student.getName()}, you spelt {numWordsAttempted} ")
            wordCount += "word." if numWordsAttempted==1 else "words."
            self.teacherSays(wordCount)
            self.teacherSays(f"Here is a summary of the number of attempts you made to spell each word")
            for [word,attempts] in summary:
                text = f"You spelt '{word}' correctly after {attempts} "
                text += "attempt." if attempts==1 else "attempts."
                self.teacherSays(text)
            self.teacherSays(f"Congratulations on your efforts {self.student.getName()}.")
            self.teacherSays(f"Let's do this again tomorrow. Bye for now.")

def main():
    game = SpellSmart()
    game.play()


if __name__=="__main__":
    main()
