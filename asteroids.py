import pygame, sys
from pygame.locals import *
from elements import * 
from screens import *   
'''
asteroids.py runs an asteroids game. The goal of the game is to gain a top score by surviving
the longest while asteroids fly by. The player is a triangle in space at the center of the
screen. Controlled by the left and right arrow keys, the player can rotate and press space
to shoot little 2x2 bullet squares at the asteroids. Each asteroid hit is +20 points,
each second lasted in space is +1 point. The player has three lives until the game is over. Final
score displayed on game over screen.
'''
class Game:
    '''
    Runs the game.
    '''
    def run(self):
        #attributes/initializations
        player = Player()
        scrn_width=800
        scrn_height=600

        #initialize pygame
        pygame.init()

        #sets the font
        font=pygame.font.SysFont('Helvetica Bold', 24)
        
        #sets background image
        background=pygame.image.load('star_bkgd.png')

        #set screen
        screen=pygame.display.set_mode((scrn_width,scrn_height))
        pygame.display.set_caption('XTRA JANK ASTEROIDS!')
        FPS=pygame.time.Clock()

        #initalizes the different groups of the different elements that will be used
        all_sprites=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        asteroids=pygame.sprite.Group()
        #adding player to the all group show it shows when game starts
        all_sprites.add(player)

        #initializes events that will happen continuously as the game runs
        enter_asteroid=pygame.USEREVENT
        pygame.time.set_timer(enter_asteroid,2500)
        time_score=pygame.USEREVENT+1
        pygame.time.set_timer(time_score, 1000)

        #sets the while loop to ensure the game will quit completely when game over
        play=True
        while play:
            #sets screen to black
            screen.fill((0,0,0))

            #initializes the different events and what will happen when triggered
            for event in pygame.event.get():
                if event.type==enter_asteroid:
                    new_asteroid=Asteroid() #initializes the asteroids
                    asteroids.add(new_asteroid) #adds asteroid to the total group of asteroids
                    all_sprites.add(new_asteroid) #adds asteroids to group of everything that will be interactive in the game
                if event.type==time_score:
                    player.score+=1 #adds one to player score as each second passes
                if event.type == KEYDOWN:
                    if event.key == K_SPACE: #if space key pressed bullet will be fired from player
                        player.shoot(all_sprites, bullets) 
                if event.type == QUIT: #ends game
                    pygame.quit()
                    play=False  
                    sys.exit()

            #sets the bkgd image and renders the fonts on the top left with updating score/life count
            screen.blit(background, (0,0))
            score=font.render(f'SCORE: {player.score}', True, (255,255,255))
            lives=font.render(f'LIVES: {player.lives}', True, (255,255,255))
            screen.blit(lives, (10,15))
            screen.blit(score, (90,15))

            #controls player movement. ensures projection of bullet is rotated with the player
            key=pygame.key.get_pressed()
            if key[pygame.K_LEFT]==True:
                player.rotate(1)
            elif key[pygame.K_RIGHT]==True:
                player.rotate(-1)

            all_sprites.update() #ensures elements are moving with each fram
        
            all_sprites.draw(screen) #draws everything to screen
            
            #controls all the individual bullets
            for bullet in bullets:
                if pygame.sprite.spritecollide(bullet, asteroids, True): #triggers event when asteroid is hit by bullet
                    player.up_score()  #adds 20 to player score when bullet hits asteroid
                    bullet.kill() #destroys the asteroid, erasing it from screen
                if bullet.rect.left > scrn_width or bullet.rect.right < 0 or bullet.rect.top > scrn_height or bullet.rect.bottom < 0:
                    bullet.kill() #ensures asteroids are erased when leaving screen perimeter
            
            #controls what happens to player when asteroid hits it
            if pygame.sprite.spritecollide(player, asteroids, True): #triggers event when asteroid hits player
                screen.fill('red') #fills screen with red
                pygame.time.wait(500) #red fill onlt for half a second, pauses game for the half a second
                pygame.display.update() #ensures frame is updated with event
                player.lose_life() #life score -1
            
            #triggers event when player lives reach 0
            if player.lives==0:
                screen.fill('red') #screen fills with red
                game_over_font=pygame.font.SysFont('Helvetica Bold', 60) #initializes new, bigger font
                game_over=game_over_font.render('GAME OVER', True, (255,255,255)) #text will read game over
                screen.blit(game_over, (265, 200)) #game over text displayed
                final_score=font.render(f'SCORE = {player.score}', True, (255,255,255)) #text will read score with players final score
                screen.blit(final_score, (350,400)) #text displayed
                pygame.display.update() #screen updated with information
                pygame.time.wait(3000) #game holds screen and pauses score for three seconds before quitting, player sees game over and their final score
                play=False #stops loop

            pygame.display.update() #ensures all events are triggered and shown
            FPS.tick(60) #sets the game at 60 frames a second

def main():
    '''Runs the game. Initializes the title screen and game screen and runs both.'''
    title_screen=MainScreen()
    title_screen.run()
    game=Game()
    game.run()

if __name__ == '__main__':
    main()