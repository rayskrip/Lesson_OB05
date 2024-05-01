import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shuttle Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Класс для космического корабля
class Spaceshuttle(pygame.sprite.Sprite):
    def __init__(self):
        super(Spaceshuttle, self).__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.last_hit_time = None

    def update(self, direction):
        if direction == 'left':
            self.rect.x -= self.speed
        elif direction == 'right':
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        # Восстанавливаем цвет, если прошло более полсекунды после столкновения
        if self.last_hit_time and pygame.time.get_ticks() - self.last_hit_time > 500:
            self.image.fill(WHITE)
            self.last_hit_time = None

    def hit(self):
        self.image.fill(RED)
        self.last_hit_time = pygame.time.get_ticks()


# Класс для астероидов
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), -20))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Класс для управления игрой
class Game:
    def __init__(self):
        self.shuttle = Spaceshuttle()
        self.asteroids = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.shuttle)
        self.clock = pygame.time.Clock()
        self.running = True
        self.damage = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.shuttle.update('left')
        if keys[pygame.K_RIGHT]:
            self.shuttle.update('right')

    def update(self):
        if random.randint(1, 20) == 1:
            asteroid = Asteroid()
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)

        self.asteroids.update()
        self.check_collision()

    def check_collision(self):
        if pygame.sprite.spritecollide(self.shuttle, self.asteroids, True):
            self.shuttle.hit()
            self.damage += 1
            if self.damage >= 3:
                self.running = False
                print("Game Over!")
                pygame.quit()
                sys.exit()

    def draw(self):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)
        pygame.display.flip()


# Запуск игры
if __name__ == '__main__':
    game = Game()
    game.run()