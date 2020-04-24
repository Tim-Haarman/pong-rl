import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, max_x, max_y):
        super().__init__()
        self._size = 8
        self._max_x = max_x
        self._max_y = max_y

        self.direction_x = 1
        self.direction_y = .5
        self.speed = 3
        self._speed_increase_per_tick = 0.0005
        self._max_speed = 10

        self.image = pygame.Surface([self._size, self._size])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.x = self.x + self.speed * self.direction_x
        new_y = self.y + self.speed * self.direction_y
        
        if new_y > self._max_y - self._size or new_y < 0:
            self.direction_y *= -1
            self.y = self.y + self.speed * self.direction_y
        else:
            self.y = new_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.speed += self._speed_increase_per_tick if self.speed < self._max_speed else 0

    def bounce(self, paddle_y, paddle_height):
        self.direction_x *= -1
        ball_center = self.rect.y + self._size / 2

        y_dir = ((ball_center - paddle_y) / paddle_height) * 2 - 1

        self.direction_y = y_dir

    def reset(self, side, paddle_offset):
        self.x = paddle_offset + self._size + 5 if side == 'left' else self._max_x - paddle_offset - self._size - 5
        self.direction_x = 1 if side == 'left' else -1
        self.y = random.randint(0, self._max_y - self._size)
        self.direction_y = random.random() * 2 - 1
        self.speed = 3