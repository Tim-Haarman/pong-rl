import pygame
from ball import Ball
from paddle import Paddle

class Pong():

    def __init__(self):
        self._WINDOW_WIDTH = 800
        self._WINDOW_HEIGHT = 600
        self._SCOREBAR_HEIGHT = 100
        self._FIELD_HEIGHT = self._WINDOW_HEIGHT - self._SCOREBAR_HEIGHT
        self._PADDLE_OFFSET = 40
        self._LINE_WIDTH = 4
        
        self.ball = Ball(50, 50, self._WINDOW_WIDTH, self._FIELD_HEIGHT)
        self.left_paddle = Paddle(self._PADDLE_OFFSET, self._WINDOW_WIDTH, self._FIELD_HEIGHT, controls='ai')
        self.right_paddle = Paddle(self._WINDOW_WIDTH - self._PADDLE_OFFSET, self._WINDOW_WIDTH, self._FIELD_HEIGHT, controls='arrows')

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.ball)
        self.sprite_group.add(self.left_paddle)
        self.sprite_group.add(self.right_paddle)

        pygame.font.init()
        self.font = pygame.font.SysFont('tlwgtypewriter', 40)

    def draw_text(self, screen, side, text):
        y_factor = 0.25 if side == 'left' else 0.75
        text_render = self.font.render(text, True, (255, 255, 255))
        
        text_size = list(self.font.size(text))
        x = self._WINDOW_WIDTH * y_factor - 0.5 * text_size[0]
        y = self._FIELD_HEIGHT + .5 * self._SCOREBAR_HEIGHT - 0.5 * text_size[1]
        screen.blit(text_render, (x, y))

    def draw_field(self, screen):
        screen.fill((0, 0, 0))
        mid_point = self._WINDOW_WIDTH/2 - self._LINE_WIDTH/2
        pygame.draw.line(screen, (255, 255, 255), [mid_point, 0], [mid_point, self._FIELD_HEIGHT], self._LINE_WIDTH)
        pygame.draw.line(screen, (255, 255, 255), [0, self._FIELD_HEIGHT], [self._WINDOW_WIDTH, self._FIELD_HEIGHT], self._LINE_WIDTH)
        
        self.draw_text(screen, side='left', text=str(self.left_paddle.score))
        self.draw_text(screen, side='right', text=str(self.right_paddle.score))

    def check_collision(self):
        collisions = pygame.sprite.spritecollide(self.ball, self.sprite_group, False)
        if len(collisions) > 1:
            paddle = collisions[1]
            self.ball.bounce(paddle_y=paddle.rect.y, paddle_height=paddle._height)

    def run_ai(self):
        for paddle in [self.left_paddle, self.right_paddle]:
            if paddle._controls == 'ai':
                if paddle.rect.y < self.ball.y:
                    paddle.move_down()
                elif paddle.rect.y > self.ball.y:
                    paddle.move_up()

    def reset_sprites(self, side):
        # for sprite in self.sprite_group:
        #     sprite.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset(side=side, paddle_offset=self._PADDLE_OFFSET)

    def check_point_scored(self):
        if self.ball.x > self._WINDOW_WIDTH - self.ball._size:
            self.left_paddle.score += 1
            self.reset_sprites(side='left')
        elif self.ball.x < 0:
            self.right_paddle.score += 1
            self.reset_sprites(side='right')

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == ord('q')):
                    return

            self.sprite_group.update()
            self.run_ai()
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