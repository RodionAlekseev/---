#Импортируем модуль pygame
import pygame

#Импортируем pygame
pygame.init()

#Создаем окно
window = pygame.display.set_mode((400, 500))

#Устаналиваем заголово окна
pygame.display.set_caption("Space Game")

#Задаемм начальные значения координат и размеры игрока
x = 50
y = 50
width = 40
height = 40

#Задаем цыета, которые будут использоваться в игре
red = (255, 0, 0)
black = (0, 0, 0)

#Устаналиваем условия для цикла вайл
condition = True

#Запускаем бесконечный цикл
while condition:
    #Задержка в 100 мс
    pygame.time.delay(100)
    #Обработка всех событий
    for event in pygame.event.get():
        # Если пользователь выходит из игры, то завершаем цикл
        if event.type == pygame.QUIT:
            condition = False
    # Очищаем окно, закрашивая его черным цветом       
    window.fill(black)
     #Рисуем игрока (квадрат) на заданных координатах 
     #с заданными размерами и цветом
    pygame.draw.rect(window, red, (x, y, width, height))
    #Обновляем окно
    pygame.display.update()
    #Получаем информацию о нажатых клавишах на клавиатуре
    keys = pygame.key.get_pressed()
    #Передвигаем игрока в зависимости от нажатых клавиш
    if keys[pygame.K_LEFT] and x > 0:
        x -= 5
    elif keys[pygame.K_RIGHT] and x < 400 - width:
        x += 5
    if keys[pygame.K_UP] and y > 0:
        y -= 5
    elif keys[pygame.K_DOWN] and y < 500 - width:
        y += 5
#Завершаем работу pygame
pygame.quit()