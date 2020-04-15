import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, offset, max_x, max_y, controls='arrows'):
        super().__init__()
        self._offset = offset
        self._max_x = max_x
        self._max_y = max_y
        self._controls = controls
        
        self._width = 8
        self._height = 50
        self.speed = 5
        self.score = 0

        self.image = pygame.Surface([self._width, self._height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = offset
        self.rect.y = self._max_y / 2 - self._height / 2

    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if self._controls == 'ai':
            return
        elif keys_pressed[pygame.K_UP] and self._controls == 'arrows' or keys_pressed[ord('w')] and self._controls == 'ws':
            self.move_up()
        elif keys_pressed[pygame.K_DOWN] and self._controls == 'arrows' or keys_pressed[ord('s')] and self._controls == 'ws':
            self.move_down()

    def move_up(self):
        self.rect.y = self.rect.y - self.speed if self.rect.y > 0 else 0
    
    def move_down(self):
        self.rect.y = self.rect.y + self.speed if self.rect.y + self._height < self._max_y else self.rect.y
        
    def reset(self):
        self.rect.y = self._max_y / 2 - self._height / 2