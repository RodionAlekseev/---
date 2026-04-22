import sys #Импортируем sys

import pygame #Импортируем pygame
import random #Импортируем модуль random

pygame.init() #Инициализация pygame

# Переменные
left = False
right = False
animCount = 0
bullets = []
asteroids = []
score = 0
lives = 3

#Функция drawWindow() отвечает за отрисовку игрового окна
def drawWindow():
    #global` - оператор, который позволяет использовать глобальные переменные внутри функции.
    global animCount, bullets, asteroids, score, lives # animCount`, `bullets`, `asteroids`, `score`, `lives` - глобальные переменные, используемые в функции
    #`blit()` - метод объекта `window`, который копирует изображение на экран в указанные координаты.
    # `bg` - изображение фона, которое копируется на экран.
    # `(0, 0)` - координаты, куда копируется изображение фона.
    window.blit(bg, (0, 0))
    #for - цикл, который перебирает все объекты в списке `bullets`. bullet - текущий объект в списке `bullets`.
    for bullet in bullets:
        bullet.draw(window) # bullet.draw(window)` - метод объекта `bullet`, который отрисовывает изображение на экране, заданное в объекте `bullet`
    #- `for` - цикл, который перебирает все объекты в списке `asteroids`.
    # `asteroid` - текущий объект в списке `asteroids`.
    for asteroid in asteroids:
        window.blit(asteroid_img, asteroid) #метод объекта `window`, который копирует изображение астероида на экран в координаты, заданные в объекте `asteroid`.
        if asteroid.colliderect(player_rect): #условный оператор, который проверяет столкновение объекта `asteroid` с объектом `player_rect`.
            lives -= 1 # уменьшает количество жизней на единицу, если произошло столкновение.
    window.blit(satellite_img, satellite_rect) # метод объекта `window`, который копирует изображение спутника на экран в координаты, заданные в объекте `satellite_rect`.
    if satellite_rect.colliderect(player_rect): #`if satellite_rect.colliderect(player_rect):` - условный оператор, который проверяет столкновение объекта `satellite_rect` с объектом `player_rect`.
        lives -= 1 # `lives -= 1` - уменьшает количество жизней на единицу, если произошло столкновение.
#- `if animCount + 1 >= 30:` - условный оператор, который сбрасывает счетчик анимации `animCount`, если он достиг максимального значения.
    if animCount + 1 >= 30:
        animCount = 0
    if left: #условный оператор, который проверяет, что игрок движется влево.
        window.blit(walkLeft[animCount % 4], (x, y)) #метод, который копирует изображение игрока, находящегося в состоянии движения влево, на экран в координаты `(x, y)`.
        animCount += 1 #увеличивает значение счетчика анимации на единицу.
    elif right: #условный оператор, который проверяет, что игрок движется вправо.
        window.blit(walkRight[animCount % 4], (x, y))
        animCount += 1
    else:
        window.blit(playerStand[animCount % 3], (x, y))
        animCount += 1

    font = pygame.font.SysFont('comicsans', 30)
    score_text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    lives_text = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (320, 10))

    pygame.display.update()

#Создание класса Shot()
class Shot():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#Загрузка изображений
bg = pygame.image.load("image\\bg.jpg")
walkRight = [pygame.image.load("image\\right_1.png"), pygame.image.load("image\\right_2.png"), pygame.image.load("image\\right_3.png"), pygame.image.load("image\\right_4.png")]
walkLeft = [pygame.image.load("image\\left_1.png"), pygame.image.load("image\\left_2.png"), pygame.image.load("image\\left_3.png"), pygame.image.load("image\\left_4.png")]
playerStand = [pygame.image.load("image\\stand_1.png"), pygame.image.load("image\\stand_2.png"), pygame.image.load("image\\stand_3.png")]
asteroid_img = pygame.image.load("image\\asteroid.png")
satellite_img = pygame.image.load("image\\satellite.png")

#Создание окна
window = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Space game")

condition = True #Установка переменной
colour = (0, 0, 255) #Установка цвета
#Установка начальных координат игрока (x=165, y=416)
x = 165
y = 416
#Установка размеров (ширина=50, высота=50)
width = 50
height = 50

#Создание прямоугольника для игрока (player_rect)
player_rect = pygame.Rect(x, y, width, height)

# Создаем спутник в случайном месте на экране
satellite_rect = satellite_img.get_rect()
satellite_rect.x = random.randint(0, 350)
satellite_rect.y = random.randint(0, 350)

#Начало игрового цикла while condition
while condition:
    pygame.time.delay(30) #Задержка на 30 миллисекунд
    for event in pygame.event.get(): #Обработка всех событий pygame
        if event.type == pygame.QUIT or lives == 0: #Если происходит событие "QUIT" (закрытие окна) или заканчиваются жизни игрока,
            condition = False # устанавливается значение condition в False, что приводит к выходу из игрового цикла.

        keys = pygame.key.get_pressed() #Получение всех нажатых клавиш на клавиатуре
        if keys[pygame.K_SPACE]: #Если нажата клавиша "SPACE", то
            if len(bullets) > 0: #добавляется новый объект типа Shot в список bullets
                if bullets[-1].y < 350: #Если список bullets не пустой и координаты последнего выстрела по y меньше 350, то
                    bullets.append(Shot(round(x + width // 2), round(y), 5, (255, 0, 0), 1)) #добавляется новый выстрел в список bullets
            else: #Если список bullets пустой, то добавляется новый выстрел в список bullets
                bullets.append(Shot(round(x + width // 2), round(y), 5, (255, 0, 0), 1))

    for bullet in bullets: #Обработка движения пуль выстрела
        if bullet.y < 500 and bullet.y > 25: #Если пуля находится в заданном диапазоне высоты окна (25 < y < 500),
            bullet.y -= bullet.vel # то координата y пули уменьшается на bullet.vel,
        else: #иначе
            bullets.pop(bullets.index(bullet)) #пуля удаляется из списка bullets

        #Обработка движения игрока
        if keys[pygame.K_LEFT] and x > 0: #Если нажата клавиша "LEFT" и игрок не достиг левой границы окна (x > 0), то
            x -= 5 #то координата x уменьшается на 5,
            left = True # и игрок поворачивается влево
            right = False

        elif keys[pygame.K_RIGHT] and x < (400 - width): #Если нажата клавиша "RIGHT" и игрок не достиг правой границы окна (x < 350), то
            x += 5 #координата x увеличивается на 5,
            left = False
            right = True #и игрок поворачивается вправо (right=True)
        else: #Если игрок не движется, то
            left = False #left и right устанавливаются в False,
            right = False
            animCount = 0 #и переменная animCount устанавливается в 0

    # Создаем случайные астероиды в верхней части экрана
    if len(asteroids) == 0: #если список asteroids пустой
        #Добавление астероидов на экран и проверка столкновения
        # астероидов со спутником и игроком
        asteroid_rect = asteroid_img.get_rect()
        asteroid_rect.x = random.randint(0, 350)
        asteroid_rect.y = random.randint(-50, 0)
        asteroids.append(asteroid_rect)

    # Двигаем астроиды вниз экрана
    for detect in range(len(asteroids)):
        asteroids[detect] = asteroids[detect].move(0, 5)
        drawWindow()
    # Если астроиды достигают нижнего края экрана, удаляем их и генерируем новые.
    for detect in range(len(asteroids)):
        if asteroids[detect].y > 500:
            asteroids.pop(detect)

