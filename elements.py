import pygame, math, random
'''
elements.py creates the different interacting elements of the game.
'''
class Player(pygame.sprite.Sprite):
    '''a triangle in the middle of the screen controlled by the user. if hit by asteroid, will lose life.
    rotatable. inheriting sprite class from pygame to make the image interactive'''
    def __init__(self):
        super().__init__()
        self.score=0 #initial score 0
        self.lives=3 #lives 3
        self.angle=0 #angle pointing straight up starts at 0

        #initial triangle surface
        self.original_image = pygame.image.load('triangle.png')  #load the original image
        self.image = self.original_image.copy() #makes copy of triangle to be used when rotating
        self.rect=self.image.get_rect() #sets boundary area of triangle
        self.rect.center=(400,300) #places it in center

    def up_score(self):
        '''increases score by 20'''
        self.score+=20

    def lose_life(self):
        '''decreases lives by 1'''
        self.lives-=1

    def draw(self, screen):
        '''draws updated, rotated triangles. screen parameter to know where to display'''
        rotated_triangle = pygame.transform.rotate(self.image, self.angle) #rotates triangle
        rotated_triangle_surf = rotated_triangle.get_rect() #gets new area of rotated triangle position
        rotated_triangle_surf.center = (400, 300) #ensures it is centered to screen
        screen.blit(rotated_triangle, rotated_triangle_surf) #displays the rotated triangle
    
    def rotate(self, angle_change):
        '''controls how fast rotation is'''
        self.angle += angle_change
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, add_single, add_grp):
        '''adds a bullet to the player, uses the players angle to calculate trajectory'''
        bullet = Bullet(self.angle+90)
        add_single.add(bullet)
        add_grp.add(bullet)

class Bullet(pygame.sprite.Sprite):
    '''a 2x2 square that will emit from center of player when space bar pressed, trajectory calculated
    by players angle. thus, player angle must will be parameter. sprite class inherited from pygame
    to make the square interactive'''
    def __init__(self, angle):
        super().__init__()
        self.x, self.y = (400,300) #bullet will always start at center
        self.image = pygame.Surface((5, 5)) #creates square
        self.image.fill((255, 255, 255)) #makes square white
        self.rect = self.image.get_rect(center=(self.x, self.y)) #sets boundary
        self.angle = angle #angle from initialization

    def update(self):
        '''Update the bullet's position'''
        #calculate the movement based on the angle
        dx = 1 * math.cos(math.radians(self.angle))
        dy = -1 * math.sin(math.radians(self.angle))
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        '''displays bullet to screen'''
        screen.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
    '''a image created by me, when image crosses into the players image area, player will lose life.
    inherits pygame.sprite class to make asteroid interactive'''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('asteroid_img.png') #gets the asteroid image 
        self.rect=self.image.get_rect() #sets its area

        #randomly spawn points
        side=random.choice(['left', 'right', 'top', 'bottom'])
        if side =='left':
            self.rect.center=(-50, random.randint(0,600))
        elif side =='right':
            self.rect.center=(50, random.randint(0,600))
        elif side =='top':
            self.rect.center=(random.randint(0,600), 50)
        elif side =='bottom':
            self.rect.center=(random.randint(0,600), -50)
        
        #calculates the angle it needs to head towards center
        center_x, center_y = 400, 300 #sets center
        dx = center_x - self.rect.centerx
        dy = center_y - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))

    def update(self):
        '''moves the asteroid and update its position so it can display there'''
        self.speed = 1.2 
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        '''displays asteroid to screen'''
        screen.blit(self.image, self.rect)
