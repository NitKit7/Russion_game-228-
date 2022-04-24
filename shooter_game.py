from pygame import *
from random import randint
from time import time as timer

bullets = sprite.Group()
lastFire = timer()
firet = timer()
fireCooldown = 0.2

mixer.init() 
mixer.music.load('space.ogg') 
mixer.music.play() 
fire_sound = mixer.Sound('fire.ogg')


class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_y, size_x, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_y, size_x)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()


class Hero(GameSprite): 
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_a] and self.rect.x > 5: 
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < win_width - 80: 
            self.rect.x += self.speed 
        if keys[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.x + 22, self.rect.y, 15, 20, 4)
            bullets.add(bullet)
            fire_sound.play()

    def fireS(self):
        global lastFire
        firet = timer()

        if firet - lastFire >= fireCooldown :
            lastFire = firet
            bullets.add(Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 25, 4))
            fire.play()


class Enemy(GameSprite): 
    direction = 'down' 
    def update(self):
        global lost 
        global killed
        global finish
        global finish_lose
        global finish_win
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
        sprite_list = sprite.groupcollide(
            monsters, bullets, False, True
        )
        if len(sprite_list) != 0:
            killed += len(sprite_list)
            if killed >= 10 :
                finish = True
                finish_win = True
            
            for i in sprite_list:
                i.rect.x = randint(80, win_width - 80)
                i.rect.y = 0
        if len(sprite.groupcollide(gg, monsters, False, False)) > 0 or lost >= 3:
            finish = True
            finish_lose = True


win_width = 700 
win_height = 500 
window = display.set_mode((win_width, win_height)) 
display.set_caption('Шутер за 1,7 рубля') 
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height)) 
 
rocket = Hero("rocket.png", 300, 430, 60, 60, 4)

monsters = sprite.Group()
monsters.add(Enemy('ufo.png', 100, 0, 80, 50, 2))
monsters.add(Enemy('ufo.png', 200, 0, 80, 50, 1))
monsters.add(Enemy('ufo.png', 300, 0, 80, 50, 2))
monsters.add(Enemy('ufo.png', 400, 0, 80, 50, 1))
monsters.add(Enemy('ufo.png', 500, 0, 80, 50, 2))

gg = sprite.Group()
gg.add(rocket)

clock = time.Clock()
FPS = 60 
 
font.init()
font = font.Font(None, 36)

lost = 0
killed = 0

game = True 
finish = False 
finish_lose = False
finish_win = False
win = font.render('YOU VIN!', True, (255, 225, 225)) 
lose = font.render('YOU LOX!', True, (255, 225, 225)) 

while game: 
    clock.tick(FPS) 
    if finish != True: 
        window.blit(background,(0, 0)) 
        
         
        rocket.update() 
        rocket.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_win = font.render("Счёт:" + str(killed), 1, (255, 255, 255))
        

        window.blit(text_lose,(25, 25))
        window.blit(text_win,(25, 55))
    elif finish_win:
        window.blit(win,(250, 250))
    elif finish_lose:
        window.blit(lose,(250, 250))
        

    for e in event.get(): 
        if e.type == QUIT: 
            game = False

    
    display.update()