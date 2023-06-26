import pygame as pg
import time, random, math
from settings import *
from tilemap import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.player = pg.image.load("assets/player.png").convert_alpha()
        self.image = pg.Surface((TILESIZE, PLAYERHIGHT))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.player_rect = self.player.get_rect()
        self.vx, self.vy = 0, 0
        self.face = 4
        self.clock = pg.time.Clock()
        self.frame = 0
        self.live = [4,4,4,4,1]
        
    def Live(self):
        return self.live       


    def get_keys(self):
        self.time = self.clock.tick(FPS) 
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
            self.face = 3
            self.frame += 0.1
            return True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.face = 1
            self.frame += 0.1
            return True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
            self.face = 2
            self.frame += 0.1
            return True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.face = 0
            self.frame += 0.1
            return True
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_npcs(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.npc, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width +5
                if self.vx < 0:
                    self.x = hits[0].rect.right -5
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.npc, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom 
                self.vy = 0
                self.rect.y = self.y

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.collide_with_npcs('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_npcs('y')
       
        if self.frame >4:
            self.frame = 0


    def draw(self, sourface, camara):
        '''self.image.blit(self.player,(0,0),(self.frame*0,self.face* 64,32,42))'''
        sourface.blit(self.player, camara.apply(self),(int(self.frame)*32,self.face* 64,TILESIZE,PLAYERHIGHT))
        
class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.npc = pg.image.load("assets/npc.png").convert_alpha()
        self.npc_rect = self.npc.get_rect()
        self.vx, self.vy = 0, 0
        self.face = 4
        self.frame = 0
        self.image = pg.Surface((TILESIZE, PLAYERHIGHT))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x 
        self.y = y  
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
    def look(self):
        self.r = math.sqrt(math.pow((self.game.player.x - self.rect.x),2)+math.pow((self.game.player.y - self.rect.y),2))
        pass
            

    def update(self):
       pass
          
    def draw(self, surface, camara):
        surface.blit(self.npc, camara.apply(self),(int(self.frame)*32, 0,TILESIZE,PLAYERHIGHT))

    


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def draw(self, sourface, camara):
        sourface.blit(self.image, camara.apply(self))