import pygame
import sys 

pygame.init()

WIDTH , HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong")

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

padH, padW = 80,12
padsped = 6
balsize = 14
balspeedx = 5
balspeedy = 5

#font
font = pygame.font.SysFont(None, 72)

padLeft = pygame.Rect(20,HEIGHT//2 - padH//2,padW,padH)
padRight = pygame.Rect(WIDTH-20-padW,HEIGHT//2 - padH//2,padW,padH)
bal = pygame.Rect(WIDTH//2-balsize//2,HEIGHT//2-balsize//2,balsize,balsize)

baldx= balspeedx
baldy= balspeedy

scorel =0
scorer =0

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()

    #input
    keys = pygame.key.get_pressed()

    #left paddle
    if keys[pygame.K_w] and padLeft.top > 0:
        padLeft.y -= padsped

    if keys[pygame.K_s] and padLeft.bottom < HEIGHT:
        padLeft.y += padsped

    #right paddle
    if keys[pygame.K_UP] and padRight.top > 0:
        padRight.y -= padsped

    if keys[pygame.K_DOWN] and padRight.bottom < HEIGHT:
        padRight.y += padsped


    #ball movement
    bal.x += baldx
    bal.y += baldy


    #bounce top bottom
    if bal.top <= 0 or bal.bottom >= HEIGHT:
        baldy *= -1


    #paddle collision
    if bal.colliderect(padLeft) and baldx < 0:
        baldx *= -1

    if bal.colliderect(padRight) and baldx > 0:
        baldx *= -1


    #score
    if bal.left <= 0:
        scorer += 1

        bal.center = (WIDTH//2, HEIGHT//2)

        baldx = balspeedx
        baldy = balspeedy


    if bal.right >= WIDTH:
        scorel += 1

        bal.center = (WIDTH//2, HEIGHT//2)

        baldx = -balspeedx
        baldy = balspeedy


    #draw
    WIN.fill(BLACK)


    #middle line
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(
            WIN,
            WHITE,
            (WIDTH//2-2, y, 4, 18)
        )


    #draw objects
    pygame.draw.rect(WIN, WHITE, padLeft)
    pygame.draw.rect(WIN, WHITE, padRight)

    pygame.draw.ellipse(WIN, WHITE, bal)


    #score text
    lefttxt = font.render(str(scorel), True, WHITE)
    righttxt = font.render(str(scorer), True, WHITE)


    WIN.blit(
        lefttxt,
        (WIDTH//4-lefttxt.get_width()//2,20)
    )

    WIN.blit(
        righttxt,
        (3*WIDTH//4-righttxt.get_width()//2,20)
    )


    pygame.display.flip()