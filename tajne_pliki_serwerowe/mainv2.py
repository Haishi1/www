import sys
import pygame
import math
import brick
from pygame import gfxdraw
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
player_angle = 0.0000001
casted_rays = 60
step_angle = fov/casted_rays
MAX_DEPTH = int(mapS*mapx)
PI2 = math.pi/2
PI3 = 3*math.pi/2
DR = 0.0174532925


map = [
    1, 1, 1, 3, 1, 1, 1, 1,
    2, 0, 0, 0, 1, 0, 0, 1,
    1, 2, 1, 0, 1, 0, 1, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1,
    1, 3, 1, 0, 0, 0, 0, 1,
    1, 0, 3, 0, 0, 2, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1
]
def drawmap():
    for y in range(mapy):
        for x in range(mapx):
            if map[y*mapx+x] >0:
                tile_color = (220, 220, 220)
            else:
                tile_color = (80, 80, 80)
            xo, yo = x*mapS, y*mapS
            pygame.draw.rect(screen, tile_color, (xo,yo,mapS-2,mapS-2))


def drawplayer():
    pygame.draw.circle(screen,(255,255,0),(px,py),5)
    pygame.draw.line(screen,(255,255,0),(px,py),
                     (px+math.cos(player_angle)*30,py+math.sin(player_angle)*30)
                    )

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

                # checkbox = pygame.draw.rect(screen,(25,255,25),(col*mapS,row*mapS,mapS,mapS))
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
def raycastv2():
    r, mx, my, mp, dof = (int(0),int(0),int(0),int(0),int(0))
    rx, ry, ra, xo, yo,distf = (float(0),float(0),float(0),float(0),float(0),float(0))
    ra=player_angle - DR*30
    if(ra<0): ra+= 2*math.pi
    if(ra>2*math.pi): ra-=2*math.pi
    ## CHECK HORIZONTAL
    for r in range(120):
        distH = float(1000000)
        hx,hy = px,py
        dof=0
        aTan =-1/math.tan(ra)
        if(ra>math.pi): ##up
            ry= int((int(py)>>6)<<6)-0.0001
            rx=(py-ry)*aTan+px
            yo=-64
            xo=-yo*aTan
        if(ra<math.pi): ##down
            ry= int((int(py)>>6)<<6)+64
            rx=(py-ry)*aTan+px
            yo= 64
            xo=-yo*aTan
        if ra==0 or ra==math.pi:
            rx=px
            ry=py
            dof=8
        while(dof<8):
            mx = int(rx)>>6
            my = int(ry)>>6
            mp=my*mapx+mx
            if mp>0 and mp<mapx*mapy and map[mp]>0:
                dof=8
                hx,hy = rx,ry
                distH=dist(px,py,hx,hy,ra)
                mpH=mp
            else:
                rx+=xo
                ry+=yo
                dof+=1
        distV = float(1000000)
        vx, vy = px, py
        dof=0
        nTan =-math.tan(ra)
        if(ra>PI2 and ra<PI3): ##up
            rx= int((int(px)>>6)<<6)-0.0001
            ry=(px-rx)*nTan+py
            xo=-64
            yo=-xo*nTan
        if(ra<PI2 or ra>PI3): ##down
            rx= int((int(px)>>6)<<6)+64
            ry=(px-rx)*nTan+py
            xo= 64
            yo=-xo*nTan
        if ra==0 or ra==math.pi:
            rx=px
            ry=py
            dof=8
        while(dof<8):
            mx = int(rx)>>6
            my = int(ry)>>6
            mp=my*mapx+mx
            if mp>0 and mp<mapx*mapy and map[mp]>0:
                dof=8
                vx,vy = rx,ry
                distV= dist(px,py,vx,vy,ra)
                mpV=mp
            else:
                rx+=xo
                ry+=yo
                dof+=1
        if (distH>distV): rx,ry,distf,mp,shade = vx,vy,distV,mpV,0.7
        if (distV>distH): rx,ry,distf,mp,shade = hx,hy,distH,mpH,1
        tText=[]
        if map[mp]==1:
            tText = brick.brickText
        if map[mp]==2:
            tText = brick.someText
        if map[mp]==3:
            tText = brick.soText

        ###pygame.draw.line(screen, (255,255,0), (px, py), (rx, ry))
        ca = player_angle -ra
        if ca >0: ca+=2*math.pi
        if ca <2*math.pi: ca-=2*math.pi
        distf=distf*math.cos(ca)
        lineH = (64*512)/distf
        ty_step=float(32/lineH)
        ty_offset=float(0)
        if(lineH>512): lineH,ty_offset=512,(lineH-512)/2.0
        lineO = 256-lineH/2
        ty=ty_offset*ty_step
        if shade ==1:
            tx=int(rx/2.0)%32
            if ra>180*DR: tx=31-tx
        else:
            tx=int(ry/2.0)%32
            if ra>90*DR and ra<270*DR: tx=31-tx
        y=0
        while(y<lineH):
            c=tText[int(ty)*32+int(tx)]*255
            y+=1
            ##gfxdraw.rectangle(screen,(int(r*4.5+516.5)-3,int(y+lineO),5,1),(c,c,c))
            gfxdraw.rectangle(screen,(int(r*4.5+516.5)-2,int(y+lineO)-2,5,1),(int(c*shade),int(c*shade),int(c*shade),))
            #gfxdraw.pixel(screen,int(r*4.5+516.5),int(y+lineO),(int(c*shade),int(c*shade),int(c*shade)))
            #gfxdraw.line(screen,int(r*4.5+516.5)-2,int(y+lineO),int(r*4.5+516.5)+2,int(y+lineO),(int(c*shade),int(c*shade),int(c*shade)))
            #gfxdraw.circle(screen,int(r*4.5+516.5)-2,int(y+lineO),3,(c,c,c))
            ty=ty+ty_step

        ra+=DR*0.5
        if (ra < 0): ra += 2 * math.pi
        if (ra > 2 * math.pi): ra -= 2 * math.pi

def dist(ax,ay,bx,by,ang):
    return (math.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay)))

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
    pygame.draw.rect(screen,(150,150,150),(512,0,512,256))
    pygame.draw.rect(screen, (100,100,100), (512, 256, 512, 256))
    raycastv2()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -=0.05
        if player_angle<0:
            player_angle+=2*math.pi
    if keys[pygame.K_RIGHT]:
        player_angle += 0.05
        if player_angle>2*math.pi:
            player_angle-=2*math.pi
    print(map[int((py+math.sin(player_angle) *5)/64)*mapy+int((px+math.cos(player_angle) *5)/64)])
    if keys[pygame.K_UP] and map[int((py+math.sin(player_angle) *20)/64)*mapy+int((px+math.cos(player_angle) *20)/64)]==0:
        px += +math.cos(player_angle) *2
        py += math.sin(player_angle) *2
    if keys[pygame.K_DOWN]:
        px -= math.cos(player_angle) *2
        py -= math.sin(player_angle) *2
    if keys[pygame.K_e] and map[int((py+math.sin(player_angle) *40)/64)*mapy+int((px+math.cos(player_angle) *40)/64)]==3:
        map[int((py + math.sin(player_angle) * 40) / 64) * mapy + int((px + math.cos(player_angle) * 40) / 64)] =0
    pygame.display.flip()
    clock.tick(30)