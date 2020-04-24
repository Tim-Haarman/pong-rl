import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, offset, max_x, max_y, controls='arrows', side='left', speed=5):
        super().__init__()
        self._offset = offset if side == 'left' else max_x - offset 
        self.side = side
        self._max_x = max_x
        self._max_y = max_y
        self._controls = controls
        
        self._width = 8
        self._height = 50
        self.speed = speed
        self.score = 0
        self.has_lost = False

        self.image = pygame.Surface([self._width, self._height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self._offset
        self.rect.y = self._max_y / 2 - self._height / 2

        self.move_to = self.rect.y

    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if self._controls in ['simple_ai', 'smart_ai', 'neat']:
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