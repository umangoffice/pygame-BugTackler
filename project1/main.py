import pygame
from sys import exit
from random  import randint, choice
pygame.init()

# sprite class

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super().__init__()
        
        walk_1 = pygame.image.load('project1\sprite\player_walk_1.png')
        
        walk_2 = pygame.image.load('project1\sprite\player_walk_2.png')

        self.walk = [walk_1, walk_2]
        
        self.index = 0
        
        self.jump = pygame.image.load('project1\sprite\jump.png')
        
        self.image = self.walk[self.index]
        
        self.rect = self.image.get_rect(midbottom = (100,300))
        
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('project1\sprite\jaudio.mp3')
        
        self.jump_sound.set_volume(0.3)
        
    def player_input(self):
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            
            self.jump_sound.play()
            
            self.gravity = -20
            
    def apply_gravity(self):
        
        self.gravity += 1
        
        self.rect.y += self.gravity
        
        if self.rect.bottom >= 300:
            
            self.rect.bottom = 300
        
    def player_anime(self):
        
        if self.rect.bottom == 300:
            
            self.index += 0.1
            
            if self.index >= len(self.walk): self.index = 0
            
            self.image = self.walk[int(self.index)]
            
        else:
            
            self.image = self.jump
            
    def update(self):
        
        self.player_input()
        
        self.apply_gravity()
        
        self.player_anime()

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, type):
        
        super().__init__()
        
        if type == 'fly':
            
            fly1 = pygame.image.load('project1\sprite\efly.png')
            
            fly2 = pygame.image.load('project1\sprite\efly2.png')
            
            self.moves = [fly1, fly2]
            
            y_pos = 200
            
        else:
            
            snail1 = pygame.image.load('project1\sprite\snail1.png')
            
            snail2 = pygame.image.load('project1\sprite\snail2.png')
            
            self.moves = [snail1, snail2]
            
            y_pos = 300
        
        self.index  = 0
        
        self.image = self.moves[self.index]
        
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
        
    def anime(self):
        
        self.index += 0.1
        
        if self.index >= len(self.moves): self.index = 0
        
        self.image = self.moves[int(self.index)]
        
    def destroy(self):
        
        if self.rect.x < -100:
            
            self.kill()
            
    def update(self, type):
        
        self.anime()
        
        self.destroy()
        
        if type == 'fly':
        
            self.rect.x -= 6
            
        else:
            
            self.rect.x -= 4

def collision():
    
    if pygame.sprite.spritecollide(player.sprite, enemy, False):
  
        for each_enemy in enemy:
            
            each_enemy.kill()
        
        return False
    
    else:
        
        return True

def score():
    
    score = int(pygame.time.get_ticks()/1000) - current_score
    
    text = font.render('Score : ' + str(score), False, 'Black')
    
    text_r = text.get_rect(center = (400,100))
    
    screen.blit(text, text_r)
    
    return score

# declaring variables

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,400))

pygame.display.set_caption('Bug Tackler')

player = pygame.sprite.GroupSingle()

player.add(Player())

enemy = pygame.sprite.Group()

enemy_timer = pygame.USEREVENT + 1

pygame.time.set_timer(enemy_timer, 1500)

active = False

current_score = 0

track_score = 0

bg_music = pygame.mixer.Sound('project1\sprite\_bg.mp3')

bg_music.set_volume(0.5)

bg_music.play(loops = -1)

# assets

sky = pygame.image.load('project1\sprite\Sky.png')

ground = pygame.image.load('project1\sprite\ground.png')

font = pygame.font.Font('project1\sprite\pixeltype.ttf', 45)

player_stand = pygame.image.load('project1\sprite\player_stand.png')

player_stand = pygame.transform.scale2x(player_stand)

player_stand_r = player_stand.get_rect(center = (400, 200))

# game loop

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: 
            
            pygame.quit()
            
            exit()
            
        if active:
            
            if event.type == enemy_timer:
            
                enemy.add(Enemy(choice(['fly', 'snail', 'snail', 'snail'])))
                
        else:
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    
                    active = True
                    
                    current_score = int(pygame.time.get_ticks()/1000)
                
    if active:
        
        active = collision()
            
        screen.blit(ground, (0, 300))
            
        screen.blit(sky, (0,0))
        
        track_score = score()
            
        player.draw(screen)
    
        player.update()
    
        enemy.draw(screen)
    
        enemy.update(choice(['fly', 'snail', 'snail', 'snail']))
        
    else:
        
    # assets
        
        title = font.render('Maze Runner', False, (0, 255, 255))

        title_r = title.get_rect(center = (400, 50))

        prompt = font.render('Press SPACE to Start!', False, (0, 255, 255))

        prompt_r = prompt.get_rect(center = (400, 350))

        total = font.render('Total Score : ' + str(track_score), False, (0,255,255))
            
        total_r = total.get_rect(center = (400, 350))
        
    # assets
        
        screen.fill((94,129,162))
        
        screen.blit(title, title_r)
        
        screen.blit(player_stand, player_stand_r)
        
        if track_score == 0:
            
            screen.blit(prompt, prompt_r)
            
        else:
            
            screen.blit(total, total_r)
    
# update per frame
    
    pygame.display.flip()
    
    clock.tick(60)