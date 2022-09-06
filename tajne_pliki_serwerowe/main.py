import math
import sys
import pygame
import math
from time import sleep

pygame.init()
clock = pygame.time.Clock()
screen_w, screen_h = 1024, 512
screen = pygame.display.set_mode((screen_w, screen_h))

mapx, mapy, mapS = 8, 8, 64
px = screen_h/2
py = screen_h/2
fov = math.pi/3
halffov =fov/2
player_angle = math.pi
casted_rays = 60
step_angle = fov/casted_rays
MAX_DEPTH = int(mapS*mapx)



map = [
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 0, 0, 1, 0, 0, 1,
    1, 1, 1, 0, 1, 0, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1
]
def drawmap():
    for y in range(mapy):
        for x in range(mapx):
            if map[y*mapx+x] == 1:
                tile_color = (220, 220, 220)
            else:
                tile_color = (80, 80, 80)
            xo, yo = x*mapS, y*mapS
            pygame.draw.rect(screen, tile_color, (xo,yo,mapS-2,mapS-2))


def drawplayer():
    pygame.draw.circle(screen,(255,255,0),(px,py),5)

    #pygame.draw.line(screen,(0,255,255),(px,py),(px+math.sin(player_angle)*50,py+math.cos(player_angle)*50),3)

    #pygame.draw.line(screen, (0, 255, 255), (px, py),
    #                 (px - math.sin(player_angle-halffov) * 50, py + math.cos(player_angle+halffov) * 50), 3)
    #pygame.draw.line(screen, (0, 255, 255), (px, py),
    #                 (px + math.sin(player_angle+halffov) * 50, py + math.cos(player_angle+halffov) * 50), 3)

#raycast algorithm
def raycast():
    start_angle = player_angle-halffov
    for ray in range(casted_rays):

        for depth in range(MAX_DEPTH):
            target_x = px - math.sin(start_angle)*depth
            target_y = py + math.cos(start_angle)*depth
            pygame.draw.line(screen,(0,255,255),(px,py),(target_x,target_y),1)
            col = int(target_x/mapS)
            row = int(target_y/mapS)
            square = row*mapy+col
            if map[square] == 1:
                checkbox = pygame.draw.rect(screen,(25,255,25),(col*mapS,row*mapS,mapS,mapS))
                if abs((checkbox.right - target_x)) <= 1 or abs((checkbox.left - target_x)) <=1:
                    dist = math.hypot(px - target_x, py - target_y) + 0.000001
                    fish = player_angle-start_angle
                    dist=dist*math.cos(fish)
                    wall_h = (mapS*320)/dist
                    color = (200, 0, 0)
                    render3d(ray,wall_h,color)
                elif abs((checkbox.top - target_y)) <= 1 or abs((checkbox.bottom - target_y)) <= 1:
                    dist = math.hypot(px - target_x, py - target_y) + 0.000001
                    fish = player_angle - start_angle
                    dist*=math.cos(fish)
                    wall_h = (mapS*320)/dist
                    color = (255,0,0)
                    render3d(ray,wall_h,color)
                #depth = depth*math.cos(player_angle-start_angle)
                #line_h =screen_h*50/(depth + 0.000001)
                #render3d(ray,line_h,(255,255,0))
                break

        start_angle+=step_angle


def render3d(i,line_h,color):
    ile_lini = casted_rays
    l= i+1
    a=(screen_w/2)/ile_lini
    offset = screen_w/2
    yoffset = screen_h/2 - line_h/2
    pygame.draw.line(screen, color, ((a*l-a/2)+offset, yoffset), ((a*l-a/2)+offset, line_h+yoffset), int(a+1))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((30, 30, 30))
    drawmap()
    drawplayer()
    raycast()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -=0.05
    if keys[pygame.K_RIGHT]: player_angle += 0.05
    if keys[pygame.K_UP]:
        px += -math.sin(player_angle) *2
        py += math.cos(player_angle) *2
    if keys[pygame.K_DOWN]:
        px -= -math.sin(player_angle) *2
        py -= math.cos(player_angle) *2
    pygame.display.flip()
    clock.tick(60)