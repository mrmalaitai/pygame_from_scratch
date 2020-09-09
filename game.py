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

def game_over():
    

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

def check_distance(player_rect, enemy_rect, player_health):
    if player_rect.x < enemy_rect.x +15:
        enemy_rect.x -= 1

    if player_rect.x > enemy_rect.x +15:
        enemy_rect.x += 1

    if player_rect.y < enemy_rect.y +15:
        enemy_rect.y -= 1

    if player_rect.y > enemy_rect.y +15:
        enemy_rect.y += 1
    
    #if(player_rect.x >= enemy_rect.x and player_rect.x + 5 <= enemy_rect.x) and (player_rect.y >= enemy_rect.y and player_rect.y + 13 < enemy_rect.y + 30):
    #    player_rect.x = 100
    #    player_rect.y = 100
    
    # player_rect.x + 3 >= enemy_rect.x
    # player_rect.x <= enemy_rect.x + 30
    # player_rect.y + 15 >= player_rect.y
    # player_rect.y <= player_rect.y + 30
    
    #print("Top Left: ", (player_rect.x + 5 >= enemy_rect.x and player_rect.y + 13 >= enemy_rect.y)) Correct
    #print("Top Right: ", (player_rect.x <= enemy_rect.x + 30 and player_rect.y + 13 >= enemy_rect.y)) Correct
    #print("Bottom Left: ", (player_rect.x + 3 >= enemy_rect.x and player_rect.y <= enemy_rect.y + 30)) Correct
    #print("Bottom Right: ", (player_rect.x <= enemy_rect.x + 30 and player_rect.y <= enemy_rect.y + 30)) Correct


    # If the enemy (width = 30, height = 30) interacts with player (width = 5, height = 13)
    if((player_rect.x + 5 >= enemy_rect.x and player_rect.y + 13 >= enemy_rect.y) and (player_rect.x <= enemy_rect.x + 30 and player_rect.y + 13 >= enemy_rect.y) and (player_rect.x + 3 >= enemy_rect.x and player_rect.y <= enemy_rect.y + 30) and (player_rect.x <= enemy_rect.x + 30 and player_rect.y <= enemy_rect.y + 30)):
        player_rect.x = 100
        player_rect.y = 100

    #print((player_rect.x + 3 >= enemy_rect.x and player_rect.y + 15 >= enemy_rect.y) and (player_rect.x + 3 >= enemy_rect.x and player_rect.y <= enemy_rect.y + 30))
    #print(player_rect.x + 5 >= enemy_rect.x and player_rect.y + 13 <= enemy_rect.y )

    return()

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
    finish_img = pygame.image.load("images/finish.png")
    player_img = pygame.image.load("images/player.png").convert_alpha()
    player_img_flip = pygame.transform.flip(player_img, True, False)
    enemy_img = pygame.image.load("images/enemy.png").convert_alpha()
    #run_animation = [pygame.image.load("images/run/run_0.png"),pygame.image.load("images/run/run_1.png")]

    # Audio files
    jump_sound = pygame.mixer.Sound('audio/jump.wav')
    
    # Play music
    #pygame.mixer.music.load('audio/music.wav')
    #pygame.mixer.music.play(-1) # Repeat

    player_rect = pygame.Rect(100,100,5,13) # Player object
    enemy_rect = pygame.Rect(64,195,30,30) # Enemey object
        
    game_map = load_map() # Map for game

    gameover = False
    player_health = 100
    
    while not gameover:
        display.fill((250,193,6)) # background        colour
        
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
                if tile == '5':
                    display.blit(finish_img,(x*16-scroll[0],y*16-scroll[1]))   
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                x += 1
            y += 1
        
        player_movement = [0,0] # player_movement[0] represents the x direction, player_movement[1] represents the y direction
        enemy_movement = [0,0]

        if moving_left == True:
            player_movement[0] -= 2 # if player_movement[0] = -2 then the player is moving to the left


        if moving_right == True:
            player_movement[0] += 2 # if player_movement[0] = 2 then the player is moving to the right

        player_movement[1] += vertical_momentum
        enemy_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        player_rect,collisions = move(player_rect,player_movement,tile_rects)
        #enemy_rect,collisions = move(enemy_rect,enemy_movement,tile_rects)
        
        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        direction = 0

        if(moving_left == True):
            direction = 1
        if(moving_right == True):
            direction = 0
        
        

        if(direction == 0):
            display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        if(direction == 1):
            display.blit(player_img_flip,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        display.blit(enemy_img,(enemy_rect.x-scroll[0],enemy_rect.y-scroll[1]))

        for event in pygame.event.get(): # wait for event
            if event.type == QUIT: # If the 'x' on the top right of the window is clicked, close the window
                #gameover = True
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a: # If left (or w) key is pressed down
                    moving_left = True
                if event.key == K_RIGHT or event.key == K_d: # If right key (or d) is pressed down
                    moving_right = True
                if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                    jump_sound.play()
                    if air_timer < 6:
                        vertical_momentum = -5
            
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a: # If left key (or a) is released
                    moving_left = False
                if event.key == K_RIGHT or event.key == K_d: # If right key (or d) is released
                    moving_right = False

        # If the player is falling (y>200), reset player position.
        if(player_rect.y > 200):
            player_rect.x = 100
            player_rect.y = 100

        # Hit the first spring located between (235, 99) and (256, 99)
        if(player_rect.y == 179 and player_rect.x < 256 and player_rect.x > 235):
            jump_sound.play()
            if air_timer < 6:
                vertical_momentum = -7

        # Hit the second spring located between (587, 99) and (608, 99)
        if(player_rect.y == 131 and player_rect.x < 608 and player_rect.x > 587):
            jump_sound.play()
            if air_timer < 6:
                vertical_momentum = -7
        
        # Hit the third spring located between (524, 99) and (543, 99)
        if(player_rect.y == 35 and player_rect.x < 543 and player_rect.x > 524):
            jump_sound.play()
            if air_timer < 6:
                vertical_momentum = -7

        # Temporary boost 1
        if(player_rect.y == 195 and player_rect.x < 350 and player_rect.x > 316):
            if(moving_left):
                player_rect.x -= 5
            if(moving_right):
                player_rect.x += 5

        # Temporary boost 2
        if(player_rect.y == 147 and player_rect.x < 544 and player_rect.x > 507):
            if(moving_left):
                player_rect.x -= 5
            if(moving_right):
                player_rect.x += 5

        #player_health = (check_distance(player_rect, enemy_rect, player_health)) # Closes the distance for player from enemy
        
        #if(player_health == 0):
        #    game_over = True
        
        #print(player_health)

        #print(player_rect.x, player_rect.y)
        if(player_rect.y==19 and player_rect.x <= 123 and player_rect.x >= 93):
            player_rect.x = 100
            player_rect.y = 100            

        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

# Global constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
clock = pygame.time.Clock()

main()