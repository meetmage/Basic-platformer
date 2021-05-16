import pygame, sys #import pygame and sys

clock = pygame.time.Clock() # set up fps clock


from pygame.locals import * #import pygame module
pygame.init() #initiates pygame

pygame.display.set_caption('Call of Duty: Cold War') # set window name

window_size = (600,400) #set window size

screen = pygame.display.set_mode(window_size,0,32) #initiates window

display = pygame.Surface((380,260))

player_image = pygame.image.load('sams head.png')
player_image.set_colorkey((255,255,255))
grass_image = pygame.image.load('Grass.png')
ground_image = pygame.image.load('Ground.png')
grass_size_x = grass_image.get_width()
grass_size_y = grass_image.get_height()
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','1','0','0','0','0','0','0','2','2','2','2','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]




def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
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
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False
scroll = [0,0]
player_x_momentum = 0
player_y_momentum = 0
player_rect = pygame.Rect(0,0,player_image.get_width(), player_image.get_height())

air_timer = 0
wall_timer = 0

while True: #game loop
    display.fill((146,244,255))




    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(ground_image, (x*grass_size_x, y * grass_size_y))
            if tile == '2':
                display.blit(grass_image, (x * grass_size_x, y * grass_size_y))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * grass_size_x, y * grass_size_y,grass_size_x, grass_size_y))
            x += 1
        y += 1
    player_movement = [0,0]
    if moving_right:
        player_movement[0] += 5
    if moving_left:
        player_movement[0] -= 5
    player_movement[1] += player_y_momentum
    player_y_momentum += 2
    if player_y_momentum > 20:
        player_y_momentum = 20

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif collisions['top']:
        air_timer += 1
        wall_timer = 0
    if collisions['left']:
        player_y_momentum = 1
        air_timer += 1
        wall_timer += 1
    elif collisions['right']:
        player_y_momentum = 1
        air_timer += 1
        wall_timer += 1
    else:
        air_timer += 1
        wall_timer = 0
    display.blit(player_image, (player_rect.x, player_rect.y))



    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if wall_timer > 10:
                    wall_timer = 0
                    player_y_momentum = -18
                elif air_timer < 5:
                    player_y_momentum = -16


        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False





    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0,0))
    pygame.display.update() #update display
    clock.tick(40) # maintain 60 fps