import pygame
pygame.init()

def drawWindow():
    global animCount
    window.blit(bg, (0, 0))
    if animCount + 1 >= 30:
        animCount = 0
    if left:
        window.blit(walkLeft[animCount % 4], (x, y))
        animCount += 1
    elif right:
        window.blit(walkRight[animCount % 4], (x, y))
        animCount += 1
    else:
        window.blit(playerStand[animCount % 3], (x, y))
        animCount += 1
        pygame.display.update()
    drawWindow()


left = False
right = False
animCount = 0
bullets = []


window = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Space Game")

x = 50
y = 50
width = 40
height = 40
red = (255, 0, 0)
black = (0, 0, 0)
condition = True

while condition:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition = False
    window.blit(bg, (0,0))
    pygame.draw.rect(window, red, (x, y, width, height))
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 0:
        x -= 5
    elif keys[pygame.K_RIGHT] and x < 400 - width:
        x += 5
    if keys[pygame.K_UP] and y > 0:
        y -= 5
    elif keys[pygame.K_DOWN] and y < 500 - width:
        y += 5
    if keys[pygame.K_LEFT] and x > 0:
        x -= 5
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 400 - width:
        x += 5
        left = False
        right = True
    else:
        left = False
        right = False


