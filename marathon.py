import pygame
from pygame.locals import *
import random
import math

pygame.init()


game_width = 1920
game_height = 1080
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption('Marathon')


# game variables
score = 0
speed = 3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.height = game_height/1.5
        self.x = 300
        self.y = game_height - self.height
        self.action = 'running'
        self.health = 1
        
        # Load running sprites
        self.running_sprites = []
        self.running_sprite_index = 0
        for i in range(10):
            running_sprite = pygame.image.load(f'images/running/run{i}.png').convert_alpha()
            scale = self.height / running_sprite.get_height()
            new_width = running_sprite.get_width() * scale
            new_height = running_sprite.get_height() * scale
            running_sprite = pygame.transform.scale(running_sprite, (new_width, new_height))
            self.running_sprites.append(running_sprite)
            
        # Load jumping sprites
        self.jumping_sprites = []
        self.jumping_sprite_index = 0
        
        jumping_sprite = pygame.image.load(f'images/jumping/jump9.png').convert_alpha()
        scale = self.height / jumping_sprite.get_height()
        new_width = jumping_sprite.get_width() * scale
        new_height = jumping_sprite.get_height() * scale
        jumping_sprite = pygame.transform.scale(jumping_sprite, (new_width, new_height))
        self.jumping_sprites.append(jumping_sprite)
            
        # Set the initial sprite rect
        self.rect = self.running_sprites[self.running_sprite_index].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Number of frames player is invincible after getting hurt
        self.invincibility_frame = 0
        
    def draw(self):
        ''' draw the sprite based on the character action and index '''
        if self.action == 'running':
            running_sprite = self.running_sprites[int(self.running_sprite_index)]
            
            # Add invincibility effect when hurt
            if self.invincibility_frame > 0:
                self.invincibility_frame -= 1
            if self.invincibility_frame % 10 == 0:
                game.blit(running_sprite, (self.x, self.y))
            
        elif self.action == 'jumping' or self.action == 'landing':
            jumping_sprite = self.jumping_sprites[int(self.jumping_sprite_index)]
            
            # Add invincibility effect when hurt
            if self.invincibility_frame > 0:
                self.invincibility_frame -= 1
            if self.invincibility_frame % 10 == 0:
                game.blit(jumping_sprite, (self.x, self.y))
            
    def update(self):
        ''' update the sprite index so the next sprite image is drawn '''
        ''' also update the y position when jumping or landing '''
        if self.action == 'running':
            self.running_sprite_index += 0.2
            if self.running_sprite_index >= len(self.running_sprites):
                self.running_sprite_index = 0
            self.rect = self.running_sprites[int(self.running_sprite_index)].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.mask = pygame.mask.from_surface(self.running_sprites[int(self.running_sprite_index)])
            
        elif self.action == 'jumping' or self.action == 'landing':
            self.jumping_sprite_index += 0.2
            if self.jumping_sprite_index >= len(self.jumping_sprites):
                self.jumping_sprite_index = 0
            if self.action == 'jumping':
                self.y -= 2.5
                if self.y <= game_height - self.height * 1.5:
                    self.action = 'landing'
            elif self.action == 'landing':
                self.y += 2.5
                if self.y == game_height - self.height:
                    self.action = 'running'
            self.rect = self.jumping_sprites[int(self.jumping_sprite_index)].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.mask = pygame.mask.from_surface(self.jumping_sprites[int(self.jumping_sprite_index)])
            
    def jump(self):
        ''' make the player go to jumping action when not already jumping or landing '''
        if self.action not in ['jumping', 'landing']:
            self.action = 'jumping'

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Load images used for the obstacles
        self.obstacle_images = []
        image = pygame.image.load(f'images/obstacles/bush.png').convert_alpha()
        scale = 380 / image.get_width()
        new_width = image.get_width() * scale
        new_height = image.get_height() * scale
        image = pygame.transform.scale(image, (new_width, new_height))
        self.obstacle_images.append(image)
            
        self.image = random.choice(self.obstacle_images)
        self.x = game_width
        self.y = game_height - self.image.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self):
        game.blit(self.image, (self.x, self.y))
        
    def update(self):
        self.x -= speed
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.image)
        
    def reset(self):
        self.image = random.choice(self.obstacle_images)
        self.x = game_width
        self.y = game_height - self.image.get_height()

# Set the image for the sky and scale it for the full screen
sky = pygame.image.load('images/bg/sky.png').convert_alpha()
sky = pygame.transform.scale(sky, (game_width, sky.get_height()))

# Create the player
player = Player()

# Create the obstacle
obstacles_group = pygame.sprite.Group()
obstacle = Obstacle()
obstacles_group.add(obstacle)

# Load the heart images for representing health
heart_sprites = []
heart_sprite_index = 0


# Game loop
clock = pygame.time.Clock()
fps = 90
quit = False
while not quit:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        if event.type == KEYDOWN and event.key == K_SPACE:
            player.jump()
        
    # Draw the sky
    game.blit(sky, (0, 0))
    
   
            
    # Draw the player
    player.draw()
    player.update()
    
    # Draw and update the obstacle
    obstacle.draw()
    obstacle.update()
    
    # Increase the score and reset the obstacle when it goes off-screen
    if obstacle.x < obstacle.image.get_width() * -1:
        score += 1
        obstacle.reset()
        if score % 2 == 0 and speed < 10:
            speed += 1
            
    # Check for collision with the obstacle
    if pygame.sprite.spritecollide(player, obstacles_group, True, pygame.sprite.collide_mask):
        player.health -= 1
        player.invincibility_frame = 30
        obstacles_group.remove(obstacle)
        obstacle = Obstacle()
        obstacles_group.add(obstacle)
        
 
    # Display the score
    black = (0, 0, 0)
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {score}', True, black)
    text_rect = text.get_rect()
    text_rect.center = (game_width - 50, 20)
    game.blit(text, text_rect)
    
    pygame.display.update()
    
    # Game over logic
    if player.health == 0:
        gameover = True
        while gameover and not quit:
            
            pygame.draw.rect(game, black, (0, 50, game_width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)
            text = font.render('Game over. Play again? (Esc or Enter)', True, "#ffffff")
            text_rect = text.get_rect()
            text_rect.center = (game_width / 2, 100)
            game.blit(text, text_rect)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        gameover = False
                        score = 0
                        speed = 3
                        player = Player()
                        obstacle = Obstacle()
                        obstacles_group.empty()
                        obstacles_group.add(obstacle)
                    elif event.key == K_ESCAPE:
                        quit = True
                    
            pygame.display.update()
            

pygame.quit()
