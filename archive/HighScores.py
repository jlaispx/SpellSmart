import pygame
from Summary import Summary

class HighScores:

    BLACK = (0,0, 0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    def __init__(self):
        try:
            with open('scores.txt','r') as inf:
                self.scores = {}
                for score in inf:
                    [player, score] = score.strip().split(' ')
                    print(player,score)
                    if player not in self.scores:
                        self.scores[player] = int(score)
        except Exception as e:
            self.scores = {}
        self.pgInit()

    def pgInit(self):
        pygame.init()
        # set initial screen resolution
        self.w = 1024
        self.h = 768
        pygame.font.init()
        self.header_font = pygame.font.SysFont('freesandbold.ttf', 48)
        self.txt_font = pygame.font.SysFont('freesandbold.ttf', 32)

        main_surface = pygame.Surface((self.w, self.h))
        self.win = pygame.display.set_mode((self.w,self.h),pygame.RESIZABLE)
        pygame.display.set_caption("High Scores")

    # Builds a Header object with different font and color
    def header_objects(self, text):
        textSurface = self.header_font.render(text, True, self.RED)
        return textSurface, textSurface.get_rect()

    def displayHeader(self):
        '''
        Inputs: None
        Process: Displays the header
        Output: Blit to window
        '''
        text = "- High Score - "
        TextSurf, TextRect = self.header_objects(text)
        # position the result on page
        TextRect.center = (self.w/2,self.h/3)
        self.win.blit(TextSurf, TextRect)

    # Builds text object with different font and color
    def text_objects(self, text):
        textSurface = self.txt_font.render(text, True, self.WHITE)
        return textSurface, textSurface.get_rect()

    def displayScores(self):
        start_h = self.h / 3 + 60  # start y co-ord for scores on page - relative to window height

        # enumerate just returns the index number of list item - store in variable i
        print("HERE",sorted(self.scores))
        print(sorted(self.scores, key=self.scores.get, reverse=True))
        for i, player in enumerate(sorted(self.scores, key=self.scores.get, reverse=True)):
            text = f"{i+1:2d} - {player:20s} - {self.scores[player]:3d}"
            self.displayScore(i,text, start_h)
            if i >= 9 :
                break

    def displayScore(self,i,text, start_h):
        gap = 20
        TextSurf, TextRect = self.text_objects(text)
        h = start_h + ((TextRect.height+gap)*i)
        TextRect.center = (self.w/2,h)
        self.win.blit(TextSurf, TextRect)

    def drawScreen(self):
        pygame.display.update()


    def display(self):
        self.displayHeader()
        self.displayScores()

        # Now wait for user input
        run = True
        quit = False

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit = True
                    break
                elif event.type == pygame.VIDEORESIZE:
                    self.w = event.w
                    self.h = event.h
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        run = False
                        break
                    if event.key in range(pygame.K_a, pygame.K_z + 1):

                        key = event.unicode.upper()
                        guess += self.key

            pygame.display.flip()

        pygame.quit()

def main():
    hs = HighScores()
    hs.display()

if __name__=="__main__":
    main()