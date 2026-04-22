#импортируют необходимые модули: pygame для создания игровой логики и random для генерации случайных значений.
import pygame
import random

#Для инициализации модуль pygame
pygame.init()

#left и right отвечают за направления движения игрока
left = False
right = False
animCount = 0 # animCount используется для определения текущего кадра анимации
bullets = [] #bullets содержит список всех выстрелов


def drawWindow(): #Функция drawWindow отображает игровое окно.
    global animCount, asteroidy, u #Она использует глобальные переменные: animCount, asteroidy и u.
    window.blit(bg, (0, 0)) # Сначала на фон выводится изображение bg
    for bullet in bullets: #затем отображаются все выстрелы в bullets
        bullet.draw(window)
    if animCount + 1 >= 30:
        animCount = 0
#а затем - текущий кадр анимации игрока в соответствии с направлением движения.
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


#Класс shot описывает выстрел.
class shot():
    def __init__(self, x, y, radius, color, facing): # У него есть координаты x и y, радиус, цвет и направление полёта (facing).
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

#Также он имеет метод draw, который отображает пулю на игровом экране.
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



#Далее загружаются все необходимые изображения: фон (bg), анимации движения вправо (walkRight), влево (walkLeft) и стояния (playerStand).
bg = pygame.image.load("image\\bg.jpg")
walkRight = [pygame.image.load("image\\right_1.png"),pygame.image.load("image\\right_2.png"), pygame.image.load("image\\right_3.png"),pygame.image.load("image\\right_4.png")]
walkLeft = [pygame.image.load("image\\left_1.png"),pygame.image.load("image\\left_2.png"), pygame.image.load("image\\left_3.png"),pygame.image.load("image\\left_4.png")]
playerStand = [pygame.image.load("image\\stand_1.png"),pygame.image.load("image\\stand_2.png"), pygame.image.load("image\\stand_3.png")]


window = pygame.display.set_mode((400, 500)) #Cоздаётся окно размером 400x500 пикселей
pygame.display.set_caption("Space game") #а его заголовок устанавливается на "Space game".
condition = True
colour = (0, 0, 255) #Затем идут переменные для определения начального положения игрока.
x = 165
y = 416
width = 50
height = 50

#В цикле while идёт обработка всех событий, возникающих в игре.
while condition:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Клавиша QUIT используется для выхода из программы.
            condition = False

# Если игрок нажимает пробел, добавляется новый выстрел в список bullets.
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
#Далее происходит проверка движения игрока: если нажата клавиша LEFT, то игрок двигается влево
    if keys[pygame.K_LEFT] and x > 0:
        x -= 5
        left = True
        right = False
#если нажата клавиша RIGHT, то вправо.
    elif keys[pygame.K_RIGHT] and x < (400 - width):
        x += 5
        left = False
        right = True
#Если клавиши не нажаты, то игрок стоит на месте.
    else:
        left = False
        right = False
#После обработки всех событий вызывается функция drawWindow, которая отображает текущее состояние игры на экране.
    drawWindow()
# Далее экран обновляется.
    pygame.display.update()