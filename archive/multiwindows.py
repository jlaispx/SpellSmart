import pygame

class Multi:
    def __init__(self):
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

