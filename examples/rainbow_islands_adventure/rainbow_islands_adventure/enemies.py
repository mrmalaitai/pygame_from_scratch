import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
YELLOW=pygame.color.THECOLORS["yellow"]




class Template():
    image = pygame.Surface((40,40))
    image.fill(RED)
    pygame.draw.line(image, BLACK, (5,7), (15,12), 4)
    pygame.draw.line(image, BLACK, (25,12), (35,7), 4)
    pygame.draw.line(image, WHITE, (12,15), (12,25), 4)
    pygame.draw.line(image, WHITE, (28,15),(28,25), 4)
    pygame.draw.line(image, WHITE, (15,33),(25,33), 4)
    
    def __init__(self,pos):
        self.sprite=Template.image.convert()
        self.width=self.sprite.get_width()
        self.height=self.sprite.get_height()
        self.bounding_box=self.sprite.get_rect()
        self.pos=pos
        self.move_speed=3
        self.xvel=3
        self.yvel=0
        self.extra_yvel=0
        self.direction="right"
        self.dead=False
    
    def update(self,level,total_level_width):
        self.pos[0]+=self.xvel
        if self.direction=="right":
           level_x=int((self.pos[0]+self.width)/32)
           level_y=int((self.pos[1]+self.height+1)/32)
           if level[level_y][level_x]!= "P"  \
           or self.pos[0]+self.width>total_level_width-32:
              self.pos[0]=(level_x*32)-self.width
              self.direction="left"
              self.xvel=-self.move_speed        
        elif self.direction=="left":
           level_x=int(self.pos[0]/32)
           level_y=int((self.pos[1]+self.height+1)/32)
           if level[level_y][level_x] != "P" or self.pos[0]<32:
              self.pos[0]=(level_x+1)*32
              self.direction="right"
              self.xvel=self.move_speed
              
    def death(self,gravity):
        self.pos[0]+=self.xvel
        self.extra_yvel+=1+gravity
        if self.extra_yvel>50:
            self.extra_yvel=50
        self.pos[1]+=self.extra_yvel

def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("rainbow islands")
    #font
    font=pygame.font.SysFont('Arial', 30)

    enemy=Template([400,300])
       
    pygame.key.set_repeat(400, 30)

    while True:
        #loop speed limitation
        #30 frames per second is enought
        pygame.time.Clock().tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  
            #keyboard movement commands    
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                   pass
                if event.key == K_RIGHT:
                   pass
                if event.key == K_UP:
                   pass

                   
            
        #blit things and refresh screen
        screen.fill(BLACK)
        screen.blit(enemy.sprite,enemy.pos)
        pygame.display.flip()

if __name__ == "__main__":
    main()
