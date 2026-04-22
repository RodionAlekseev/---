import pygame
import random

# Инициализация pygame
pygame.init()

# Создание окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Asteroids Game')

# Установка цветов
white_color = (255, 255, 255)
black_color = (0, 0, 0)
red_color = (255, 0, 0)

# Загрузка изображения корабля
ship_img = [pygame.image.load('image\\stand_1.png'), pygame.image.load('image\\stand_2.png'), pygame.image.load('image\\stand_3.png')]

# Создание класса Ship
class Ship:
    def __init__(self):
        self.image = ship_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height - self.height
        self.speed = 10

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > screen_width - self.width:
            self.x = screen_width - self.width

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Создание класса Asteroid
class Asteroid:
    def __init__(self):
        self.width = random.randint(50, 100)
        self.height = self.width
        self.x = random.randint(0, screen_width - self.width)
        self.y = 0 - self.height
        self.speed = random.randint(5, 15)

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, white_color, (self.x, self.y, self.width, self.height))

# Создание корабля
ship = Ship()

# Создание списка астероидов
asteroids_list = []

# Установка начального значения счета
score = 0

# Создание функции main
def main():
    global score

    # Создание цикла игры
    running = True
    while running:
        # Цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обработка нажатий клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.move_left()
        if keys[pygame.K_RIGHT]:
            ship.move_right()

        # Создание нового астероида
        if random.randint(0, 50) == 0:
            asteroid = Asteroid()
            asteroids_list.append(asteroid)

        # Перемещение астероидов
        for asteroid in asteroids_list:
            asteroid.move()

            # Определение, столкнулся ли астероид с кораблем
            if asteroid.y + asteroid.height >= ship.y and asteroid.x >= ship.x and asteroid.x + asteroid.width <= ship.x + ship.width:
                running = False

            # Удаление астероидов, достигших нижнего края экрана
            if asteroid.y >= screen_height:
                asteroids_list.remove(asteroid)
                score += 1

        # Отрисовка объектов
        screen.fill(black_color)
        ship.draw()
        for asteroid in asteroids_list:
            asteroid.draw()

        # Отрисовка счета
        score_font = pygame.font.SysFont("monospace", 36)
        score_text = score_font.render("Score: " + str(score), 1, red_color)
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

        # Обновление экрана
        pygame.display.update()

    # Закрытие игры
    pygame.quit()

# Запуск игры
if __name__ == '__main__':
    main()