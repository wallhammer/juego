import pygame as pg
import time, random, math
from settings import *
from tilemap import *

class HUB:
    def __init__(self, player) -> None:
        self.player =player
        self.image = pg.Rect((64, 32*20), (TILESIZE*self.player.Live(), TILESIZE/2))
        self.live = pg.image.load("assets/live.png").convert_alpha()
        self.live_rect = self.live.get_rect()
        self.rect = [self.live,
                     self.live,
                     self.live,
                     self.live,
                     self.live,]
        
         

    def update(self):
        pass
        


    def draw(self, surface):
        cont=0
        for x in self.rect:
            cont+=1
            surface.blit(x, (32*cont, 32*20),(TILESIZE*0,0,TILESIZE,TILESIZE))
        '''pg.draw.rect(surface,(255,0,0),self.live)'''


    
