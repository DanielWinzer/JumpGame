import pygame
import random
from pygame.locals import *
import time
import os.path

pygame.init()
vec=pygame.math.Vector2

dis_width=450
dis_height=450
acc=0.5
fric=-0.12
fps=60
plats=dis_width/75

clock=pygame.time.Clock()
dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("platform")

game=True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect=self.surf.get_rect(center=(10,420))

        self.pos=vec((10,360))
        self.vel=vec((0,0))
        self.acc=vec(0,0)

        self.jumping=False
        self.score=0
    def move(self):
        self.acc=vec(0,0.5)
        pressed_keys=pygame.key.get_pressed()
        if pressed_keys[K_LEFT]: self.acc.x=-acc
        if pressed_keys[K_RIGHT]: self.acc.x=acc
        self.acc.x+=self.vel.x*fric
        self.vel+=self.acc
        self.pos+=self.vel+0.5*self.acc
        if self.pos.x>dis_width: self.pos.x=0
        if self.pos.x<0: self.pos.x=dis_width
        self.rect.midbottom=self.pos
    def jump(self):
        hits=pygame.sprite.spritecollide(self,platforms,False)
        if hits and not self.jumping:
            self.jumping=True
            self.vel.y=-15
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y<-3:
                self.vel.y=-3
    def update(self):
        hits=pygame.sprite.spritecollide(P1,platforms,False)
        if P1.vel.y>0:
            if hits:
                if self.pos.y<hits[0].rect.bottom:
                    """
                    if hits[0].point==True:
                        hits[0].point==False
                        self.score+=1
                    """    
                    self.pos.y=hits[0].rect.top+1
                    self.vel.y=0
                    self.jumping=False              

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf=pygame.Surface((random.randint(50,100),12))
        self.surf.fill((255,0,0))
        self.rect=self.surf.get_rect(center = (random.randint(0,dis_width-10),random.randint(0, dis_height-30)))
        self.moving=True
        self.point=True
        self.speed=random.randint(-1,1)
    def move(self):
        if self.moving==True:
            self.rect.move_ip(self.speed,0)
            if self.speed>0 and self.rect.left>dis_width: self.rect.right=0
            if self.speed<0 and self.rect.right<0: self.rect.left=dis_width

def check(platform,groupies):
    if pygame.sprite.spritecollideany(platform,groupies): return True
    else:
        for entity in groupies:
            if entity==platform: continue
            if (abs(platform.rect.top-entity.rect.bottom)<50)and(abs(platform.rect.bottom-entity.rect.top)<50): return True
        C=False

def plat_gen(platforms,all_sprites):
    global plats
    platforms=platforms
    all_sprites=all_sprites
    while len(platforms)<plats:
        width=random.randrange(50,100)
        p=Platform()      
        C=True         
        while C:           
            p=Platform()
            p.rect.center=(random.randrange(0,dis_width-width),random.randrange(-50,0))
            C=check(p,platforms)
        platforms.add(p)
        all_sprites.add(p)


PT1=Platform()
P1=Player()

PT1.moving=False
PT1.point=True

PT1.surf=pygame.Surface((dis_width,20))
PT1.surf.fill((255,0,0))
PT1.rect=PT1.surf.get_rect(center=(dis_width/2,dis_height-10))

all_sprites=pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms=pygame.sprite.Group()
platforms.add(PT1)

for x in range(random.randint(5,plats)):
    C=True
    pl=Platform()
    while C:
        pl=Platform()
        C=check(pl,platforms)
    platforms.add(pl)
    all_sprites.add(pl)

while game:
    P1.update()
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                quit()
            if event.key==pygame.K_SPACE:
                P1.jump()
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_SPACE:
                P1.cancel_jump()
        if event.type==QUIT:
            pygame.quit()
            exit()

    if P1.rect.top<=dis_height/3:
        P1.pos.y+=abs(P1.vel.y)
        P1.score+=1
        for plat in platforms:
            plat.rect.y+=abs(P1.vel.y)
            if plat.rect.top>=dis_height:
                plat.kill()

    if P1.rect.top>dis_height:
        for entity in all_sprites: 
            entity.kill()
            dis.fill((255,0,0))
            f=pygame.font.SysFont("Verdana",20)
            g=f.render("Score: "+str(P1.score),True,(123,255,0))
            dis.blit(g,(dis_width/2.5,dis_height/2))
            pygame.display.update()
            time.sleep(2)
            quit()
                        
    dis.fill((0,0,0))
    f=pygame.font.SysFont("Verdana",20)
    g=f.render(str(P1.score),True,(123,255,0))
    dis.blit(g,(dis_width/2,10))

    plat_gen(platforms,all_sprites)
    for  entity in all_sprites:
        dis.blit(entity.surf,entity.rect)
        entity.move()
    pygame.display.update()   
    clock.tick(fps)