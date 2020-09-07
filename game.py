import pygame, sys
from pygame.locals import * # this is so the KEYDOWN, KEYUP etc will work

def load_map():
    f = open('map.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
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

def main():
    pygame.init() # initiates all the modules required for pygame

    pygame.display.set_caption("Pygame from Scratch") # title for pygame window

    WINDOW_SIZE = (600, 400)
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((300,200)) # used as the surface for rendering, 

    moving_left = False # player movement to the left
    moving_right = False # player movement to the right

    vertical_momentum = 0
    air_timer = 0
    true_scroll = [0,0]

    # Loading images

    dirt_img = pygame.image.load("images/wall.png")
    grass_img = pygame.image.load("images/wood.png")
    spring_img = pygame.image.load("images/spring.png")
    slip_img = pygame.image.load("images/slip.png")
    player_img = pygame.image.load("images/player.png").convert()
    enemy_img = pygame.image.load("images/enemy.png").convert()
    

    player_rect = pygame.Rect(100,100,5,13)
    #enemy_rect = pygame.Rect(90,100,5,13)

    # Map for game
    game_map = load_map()

    gameover = False
    
    while not gameover:
        display.fill((250,193,6)) # background colour
        
        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20 # a number lower than 20 speeds up the parallax
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20 # a number higher than 20 slows down the parallax
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        
        tile_rects = []

        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '3':
                    display.blit(spring_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '4':
                    display.blit(slip_img,(x*16-scroll[0],y*16-scroll[1]))    
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                x += 1
            y += 1
        
        player_movement = [0,0]

        if moving_left == True:
            player_movement[0] -= 2
        if moving_right == True:
            player_movement[0] += 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        player_rect,collisions = move(player_rect,player_movement,tile_rects)
        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        #display.blit(enemy_img,(enemy_rect.x-scroll[0],enemy_rect.y-scroll[1]))

        for event in pygame.event.get(): # wait for event
            if event.type == pygame.QUIT: # If the 'x' on the top right of the window is clicked, close the window
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a: # If left (or w) key is pressed down
                    moving_left = True
                if event.key == K_RIGHT or event.key == K_d: # If right key (or d) is pressed down
                    moving_right = True
                if event.key == K_UP or event.key == K_w:
                    if air_timer < 6:
                        vertical_momentum = -5
            
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a: # If left key (or a) is released
                    moving_left = False
                if event.key == K_RIGHT or event.key == K_d: # If right key (or d) is released
                    moving_right = False

        # If the player is falling (y>200), reset player position.
        if(player_rect.y>200):
            player_rect.x = 100
            player_rect.y = 100

        # Hit the first spring located between (235, 99) and (256, 99)
        if(player_rect.y == 99 and player_rect.x < 256 and player_rect.x >235):
            if air_timer < 6:
                vertical_momentum = -5

        # Temporary boost
        if(player_rect.y == 115 and player_rect.x < 350 and player_rect.x > 316):
            if(moving_left):
                player_rect.x -= 5
            if(moving_right):
                player_rect.x += 5

        """
        if(enemy_rect.x < player_rect.x):
            enemy_rect.x += 1
        if(enemy_rect.x > player_rect.x):
            enemy_rect.x -= 1
        if(enemy_rect.y < player_rect.y):
            enemy_rect.y += 1
        if(enemy_rect.y > player_rect.y):
            enemy_rect.y -= 1
        """
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

# Global constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


clock = pygame.time.Clock()

main()