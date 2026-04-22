import pygame
import random

pygame.init()

left = False
right = False
animCount = 0
bullets = []


def drawWindow():
    global animCount, asteroidy, u
    window.blit(bg, (0, 0))
    for bullet in bullets:
        bullet.draw(window)
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


class shot():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


bg = pygame.image.load("image\\bg.jpg")

walkRight = [pygame.image.load("image\\right_1.png"),
             pygame.image.load("image\\right_2.png"), pygame.image.load("image\\right_3.png"),
             pygame.image.load("image\\right_4.png")]

walkLeft = [pygame.image.load("image\\left_1.png"),
            pygame.image.load("image\\left_2.png"), pygame.image.load("image\\left_3.png"),
            pygame.image.load("image\\left_4.png")]

playerStand = [pygame.image.load("image\\stand_1.png"),
               pygame.image.load("image\\stand_2.png"), pygame.image.load("image\\stand_3.png")]

window = pygame.display.set_mode((400, 500))

pygame.display.set_caption("Пробная игра")
condition = True
colour = (0, 0, 255)
x = 165
y = 416
width = 50
height = 50

while condition:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            condition = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if len(bullets) > 0:
                if bullets[-1].y < 350:
                    bullets.append(shot(round(x + width // 2), round(y), 5, (255, 0, 0), 1))
            else:
                bullets.append(shot(round(x + width // 2), round(y), 5, (255, 0, 0), 1))

    for bullet in bullets:
        if bullet.y < 500 and bullet.y > 25:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_LEFT] and x > 0:
        x -= 5
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < (400 - width):
        x += 5
        left = False
        right = True
    else:
        left = False
        right = False
    drawWindow()
    pygame.display.update()
