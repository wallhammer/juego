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
        self.time = 0
        self.frame = 0
        
        


    def get_keys(self):
        
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
            self.face = 3
            self.frame = (self.time % 8 < 16)
            return True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            self.face = 1
            self.frame = (self.time % 8 < 16)
            return True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
            self.face = 2
            self.frame = (self.time % 8 < 16)
            return True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            self.face = 0
            self.frame = (self.time % 8 < 16)
            return True
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

        if self.time >0:
            self.frame = (self.time % 16 < 8) 



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
        self.rect.y = self.y
        self.collide_with_walls('y')



    def draw(self, sourface, camara):
        '''self.image.blit(self.player,(0,0),(self.frame*0,self.face* 64,32,42))'''
        sourface.blit(self.player, camara.apply(self),(self.frame*32,self.face* 64,TILESIZE,PLAYERHIGHT))
        
class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, player):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.load = pg.image.load
        self.npc = self.load("assets/npc.png").convert_alpha()
        self.rect = self.npc.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.player = player
        self.face = 0
        self.image = pg.rect((TILESIZE, PLAYERHIGHT))

    def update(self):
        self.r = math.sqrt(math.pow((self.player.x - self.x),2)+math.pow((self.player.y - self.y),2))
        if self.player.y < self.y and self.r < 64:
            if self.player.x  < self.x + 12 and self.player.x > self.x - 10:
                self.faceRight = 2

        if self.player.x < self.x and self.r < 64:
            if self.player.y > self.y - 18 and self.player.y < self.y + 1:
                self.faceRight = 3

        if self.player.y > self.y and self.r < 64:
            if self.player.x  < self.x + 12 and self.player.x > self.x - 12:
                self.faceRight = 0    

        if self.r < 64 and self.player.x > self.x:
            if self.player.y > self.y - 18 and self.player.y < self.y + 3:
                self.faceRight = 1
        
            
    def draw(self, surface, camara):
        surface.blit(self.npc, camara.apply(self),(0,self.face* 64,TILESIZE,PLAYERHIGHT))

    


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