import pygame, math, random,time




start = time.time() # What in other posts is described is

pygame.init()

display = pygame.display.set_mode((700, 500))

clock = pygame.time.Clock()

WINDOW_SIZE = (600,400)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled

grass_img = pygame.image.load("Data/grass.png")
player_img = pygame.image.load("Data/grass.png")
star_img = pygame.image.load("Data/star.png")
star_img.set_colorkey((255, 255, 255))

puncher_imgs = [pygame.image.load("Data/puncher_1.png"), pygame.image.load("Data/puncher_3.png")]

player_walk_imgs = [pygame.image.load("Data/player_0.png"), pygame.image.load("Data/player_1.png")]

player_hit_img = pygame.image.load("Data/player_hit_state.png")

cloud = pygame.image.load('Data/cloud.png').convert()
cloud.set_colorkey((255,255,255))

star_animation_count = 20

moving_right = False
moving_left = False
hit = False

has_spawned = False

has_landed = False
has_spawned = False

player_rect = pygame.Rect(100,400,5,13)

vertical_momentum = 0
air_timer = 0

image = None

animation_count = 0

scroll = [0, 0]

jump_sound = pygame.mixer.Sound('Data/jump.wav')

class _particle_(object):
    def __init__(self, x, y, x_vel, y_vel, color, gravity_scale):
        self.x = x 
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.gravity = 1
        self.color = color
        self.lifetime = 100
        self.gravity_scale = gravity_scale

    def draw(self, display, scroll):
        self.lifetime -= 1
        self.gravity -= self.gravity_scale
        self.x += self.x_vel
        self.y += self.y_vel * self.gravity
        pygame.draw.rect(display, self.color, (int(self.x-scroll[0]), int(self.y-scroll[1]), 2, 2))



def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('Data/map')


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


class particle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.cooldown = 0
        self.width = 7
        self.height = 7
        self.transparency = 0
        self.radius = 4
    def draw(self, display, scroll):
        if cooldown <= 0:
            self.width -= 1
            self.height -= 1
            self.radius -= 1
            self.transparency -= 100
            self.cooldown = 10
        else:
            self.cooldown -= 1


        if self.radius > 0:
            pygame.draw.circle(display, (0, 0 ,0), (self.x-int(scroll[0]), self.y-int(scroll[1])), self.radius)

class puncher(object):
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.animation_count = 0
            self.rect = pygame.Rect(self.x, self.y, 16, 16)
            self.isAddingForce = False
            self.cooldown = 0
      def draw(self, display, scroll, player_rect):
            self.rect = pygame.Rect(self.x-int(scroll[0]), self.y-int(scroll[1]), 16, 16)

            if self.rect.colliderect(player_rect.x-int(scroll[0]), player_rect.y-int(scroll[1]), 16, 16):
                  if player_rect[0] < self.x:
                        self.cooldown = 50
                        self.isAddingForce = True

            if self.cooldown > 0:
                  self.cooldown -= 1

            if self.cooldown <= 0:
                  self.isAddingForce = False

            if self.isAddingForce:
                  player_rect[0] -= 3
                  

                  
            if self.animation_count >= 8:
                  self.animation_count = 0
            self.animation_count += 1
            display.blit(puncher_imgs[self.animation_count//8], (self.rect.x, self.rect.y))

class puncher_up(object):
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.animation_count = 0
            self.rect = pygame.Rect(self.x, self.y, 16, 16)
            self.isAddingForce = False
            self.cooldown = 0
      def draw(self, display, scroll, player_rect):
            self.rect = pygame.Rect(self.x-int(scroll[0]), self.y-int(scroll[1]), 16, 16)

            if self.rect.colliderect(player_rect.x-int(scroll[0]), player_rect.y-int(scroll[1]), 16, 16):
                  self.cooldown = 50
                  self.isAddingForce = True

            if self.cooldown > 0:
                  self.cooldown -= 1

            if self.cooldown <= 0:
                self.isAddingForce = False

            if self.isAddingForce:
                  has_landed = False
                  player_rect[1] -= 5
                  
            if self.animation_count >= 8:
                  self.animation_count = 0
            self.animation_count += 1
            display.blit(pygame.transform.rotate(puncher_imgs[self.animation_count//8], -90), (self.rect.x, self.rect.y))

class puncher_right(object):
      def __init__(self, x, y):
            self.x = x
            self.y = y
            self.animation_count = 0
            self.rect = pygame.Rect(self.x, self.y, 16, 16)
            self.isAddingForce = False
            self.cooldown = 0
      def draw(self, display, scroll, player_rect):
            self.rect = pygame.Rect(self.x-int(scroll[0]), self.y-int(scroll[1]), 16, 16)

            if self.rect.colliderect(player_rect.x-int(scroll[0]), player_rect.y-int(scroll[1]), 16, 16):
                  self.cooldown = 50
                  self.isAddingForce = True

            if self.cooldown > 0:
                  self.cooldown -= 1

            if self.cooldown <= 0:
                  self.isAddingForce = False

            if self.isAddingForce:
                  player_rect[0] += 3
                  
            if self.animation_count >= 8:
                  self.animation_count = 0
            self.animation_count += 1
            display.blit(pygame.transform.rotate(puncher_imgs[self.animation_count//8], 180), (self.rect.x, self.rect.y))


puncher_left_points = []
puncher_up_points = []
puncher_right_points = []

particles = []


cooldown = 0

End_rect = None

finished = False

font_small = pygame.font.Font('Data/editundo.ttf', 20)
you_win_text = font_small.render("You WIN! R to restart!", False, (0,0,0))

def update_game():
    
      global player_rect, air_timer, vertical_momentum, has_spawned, animation_count, image, hit,cooldown, star_animation_count, End_rect, finished, has_landed
      display.fill((153, 217, 234))
      clock.tick(60)

      if animation_count >= 15:
            animation_count = 0

      for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0], background_object[1][1]-scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
            display.blit(pygame.transform.scale(cloud, (32,32)), (obj_rect.x, obj_rect.y))


      animation_count += 1


       

      tile_rects = []
      special_rects = []
      y = 0
      for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(grass_img,(x*16-int(scroll[0]),y*16-scroll[1]))
            if tile == '2':
                  puncher_left_points.append([x*16, y*16])
            if tile == '3':
                  puncher_up_points.append([x*16, y*16])
            if tile == '6':
                  puncher_right_points.append([x*16, y*16])
            if tile == '5':
                  display.blit(star_img,(x*16-int(scroll[0]),y*16-int(scroll[1])-star_animation_count))
                  End_rect = pygame.Rect(x*16,y*16-star_animation_count, 16, 16)
            if tile != '0' and tile != '2' and tile != '3' and tile != "5" and tile != "6":
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
        
            x += 1
        y += 1


      #collision_test(tile_rects, player.rect)

      player_rect,collisions = move(player_rect,player_movement,tile_rects)

      if collisions['bottom'] == True:
        has_landed = True
        air_timer = 0
        vertical_momentum = 0
      else:
        air_timer += 1

      if player_rect.colliderect(End_rect):
              #display.blit(you_win_text, (100, 100))
              finished = True 

      if finished == True:
         display.blit(you_win_text, (35, 100))


      if collisions['top'] == True:
            air_timer = 0
            vertical_momentum = 0

      if hit:
          image = player_hit_img

      elif moving_right and not hit:
            image = pygame.transform.rotate(player_walk_imgs[animation_count//10], 0)
            if cooldown <= 0:
              particles.append(particle(player_rect.x-5, player_rect.y+5))
              cooldown = 5
            else:
              cooldown -= 1

      elif moving_left and not hit:
            image = pygame.transform.rotate(pygame.transform.flip(player_walk_imgs[animation_count//10], True, False), 0)
            if cooldown <= 0:
              particles.append(particle(player_rect.x+30, player_rect.y+5))
              cooldown = 5
            else:
              cooldown -= 1

      elif not moving_right and not hit or not moving_left and not hit:
            image = player_walk_imgs[0]
            if cooldown <= 0:
              particles.append(particle(player_rect.x+10, player_rect.y+5))
              cooldown = 1
            else:
              cooldown -= 1



      display.blit(image,(player_rect.x-int(scroll[0])+10,player_rect.y-int(scroll[1])))

      for pun in punchers:
            pun.draw(display, scroll, player_rect)

      for p in particles:
          p.draw(display, scroll)

      for _p in __particles:
          _p.draw(display, scroll)


      if not has_spawned:
            for p in puncher_left_points:
                  punchers.append(puncher(p[0], p[1]))
            for p in puncher_up_points:
                  punchers.append(puncher_up(p[0], p[1]))
                  
            for p in puncher_right_points:
                  punchers.append(puncher_right(p[0], p[1]))
                  

            has_spawned = True


      screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
      pygame.display.update()

punchers = []

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.25,[30,40,40,400]],[0.25,[130,90,100,400]],[0.25,[300,200,120,400]], [0.25,[200,130,90,100]],
                      [0.25,[10,300,70,400]], [0.25,[400,30,70,400]]]

__particles = []

run = True
while run:

      scroll[0] += (player_rect.x-scroll[0]-152)/5
      scroll[1] += (player_rect.y-scroll[1]-106)/5
      
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  quit()


      keys = pygame.key.get_pressed()

      player_movement = [0,0]
      if keys[pygame.K_a]:
         player_movement[0] -= 3
         moving_right = False
         moving_left = True
      elif keys[pygame.K_d]:
         player_movement[0] += 3
         moving_right = True
         moving_left = False
      else:
         moving_right = False
         moving_left = False 
      if keys[pygame.K_SPACE]:
            if air_timer < 6:
                    for i in range(1):
                        __particles.append(_particle_(player_rect.x, player_rect.y, random.randrange(-5, 5), random.randrange(-2, 0), (0, 100, 0), 0.2))
                    vertical_momentum = -5
                    has_landed = False
                    jump_sound.play()

      if keys[pygame.K_r] and finished == True:
         player_rect = pygame.Rect(100,400,5,13)
         finished = False

      if player_rect.y > 500:
         
         player_rect = pygame.Rect(100,400,5,13)

      player_movement[1] += vertical_momentum
      vertical_momentum += 0.3
      if vertical_momentum > 3:
        vertical_momentum = 3

      update_game()

                  
