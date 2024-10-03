import pygame
from pygame.locals import *
'''
screens.py creates the main screen class that will run and be displayed when game is ran.
exits screen and quits when space bar is pressed.
'''
class MainScreen:    
    def run(self):
        #initializes game, sets screen size and initilazes the clock that controls frame rate
        pygame.init()
        screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption('XTRA JANK ASTEROIDS!')
        FPS=pygame.time.Clock()

        #loop to make sure screen closes when space bar is pressed
        running=True
        while running:
            screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running=False 
            
            #places the title text
            title=pygame.image.load('title.png')
            screen.blit(title, (125,150))

            #places instruction text
            start_font=pygame.font.SysFont('Helvetica Bold', 32)
            start=start_font.render('PRESS \'SPACE\' TO START', True, (255,255,255))
            screen.blit(start, (250,400))

            #instruction to press space to start the game
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE]==True:
                running=False

            #ensures events triggered will display
            pygame.display.update()
            FPS.tick(60) #frame rate 60 per second