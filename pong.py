import pygame
from ball import Ball
from paddle import Paddle

class Pong():

    def __init__(self):
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 500
        self._LINE_WIDTH = 4
        
        self.ball = Ball(50, 50, self._WINDOW_WIDTH, self._WINDOW_HEIGHT)
        self.left_paddle = Paddle(40, self._WINDOW_WIDTH, self._WINDOW_HEIGHT, controls='arrows')
        self.right_paddle = Paddle(self._WINDOW_WIDTH - 40, self._WINDOW_WIDTH, self._WINDOW_HEIGHT, controls='ws')

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.ball)
        self.sprite_group.add(self.left_paddle)
        self.sprite_group.add(self.right_paddle)

    def draw_field(self, screen):
        screen.fill((0, 0, 0))
        mid_point = self._WINDOW_WIDTH/2 - self._LINE_WIDTH/2
        pygame.draw.line(screen, (255, 255, 255), [mid_point, 0], [mid_point, self._WINDOW_HEIGHT], self._LINE_WIDTH)

    def check_collision(self):
        collisions = pygame.sprite.spritecollide(self.ball, self.sprite_group, False)
        if len(collisions) > 1:
            paddle = collisions[1]
            self.ball.bounce(paddle_y=paddle.rect.y, paddle_height=paddle._height)

    def check_point_scored(self):
        if self.ball.x > self._WINDOW_WIDTH - self.ball._size or self.ball.x < 0:
            for sprite in self.sprite_group:
                sprite.reset()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == ord('q')):
                    return

            self.sprite_group.update()
            self.check_point_scored()
            self.check_collision()
            self.draw_field(screen)
            self.sprite_group.draw(screen)

            clock.tick(60)
            pygame.display.flip()

    def main(self):
        pygame.init()
        self.run()
        pygame.quit()

if __name__ == "__main__":
    game = Pong()
    game.main()