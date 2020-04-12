import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, max_x, max_y):
        super().__init__()
        self._size = 8
        self._max_x = max_x
        self._max_y = max_y

        self.direction_x = 1
        self.direction_y = .5
        self.speed = 2
        self._max_speed = 7

        self.image = pygame.Surface([self._size, self._size])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        new_x = self.x + self.speed * self.direction_x
        new_y = self.y + self.speed * self.direction_y

        # if new_x > self._max_x - self._size or new_x < 0:
        #     print(f'Speed: {self.speed}')
        #     # self.direction_x *= -1
        #     self.reset()
        #     return
        # else:
        self.x = new_x
        
        if new_y > self._max_y - self._size or new_y < 0:
            self.direction_y *= -1
            self.y = self.y + self.speed * self.direction_y
            print(self.direction_y)
        else:
            self.y = new_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.speed += 0.001 if self.speed < self._max_speed else 0

    def bounce(self, paddle_y, paddle_height):
        self.direction_x *= -1
        ball_center = self.rect.y + self._size / 2

        y_dir = ((ball_center - paddle_y) / paddle_height) * 2 - 1

        self.direction_y = y_dir

    def reset(self):
        self.x = 40
        self.y = 40
        self.direction_x = 1
        self.direction_y = .5
        self.speed = 2