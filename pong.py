import pygame
import os
import neat
import time
from ball import Ball
from paddle import Paddle

generation_number = 1

class Pong():

    def __init__(self, genomes, config):
        self._WINDOW_WIDTH = 1000
        self._WINDOW_HEIGHT = 800
        self._SCOREBAR_HEIGHT = 300
        self._FIELD_HEIGHT = self._WINDOW_HEIGHT - self._SCOREBAR_HEIGHT
        self._PADDLE_OFFSET = 40
        self._LINE_WIDTH = 4
        self._NUM_AGENTS = len(genomes)
        self._FPS = 1000

        self.nn = []
        self.ge = []

        for _, genome in genomes:
            genome.fitness = 0
            self.nn.append(neat.nn.FeedForwardNetwork.create(genome, config))
            self.ge.append(genome)

        self.balls = [Ball(50, 50, self._WINDOW_WIDTH, self._FIELD_HEIGHT) for _ in range(self._NUM_AGENTS)]
        self.left_paddles = [Paddle(self._PADDLE_OFFSET, self._WINDOW_WIDTH, self._FIELD_HEIGHT, controls='neat', side='left', speed=2) for _ in range(self._NUM_AGENTS)]
        self.right_paddles = [Paddle(self._PADDLE_OFFSET, self._WINDOW_WIDTH, self._FIELD_HEIGHT, controls='simple_ai', side='right', speed=2) for _ in range(self._NUM_AGENTS)]

        self.sprite_groups = []
        for ball, left_paddle, right_paddle in zip(self.balls, self.left_paddles, self.right_paddles):
            sprite_group = pygame.sprite.Group()
            sprite_group.add(ball)
            sprite_group.add(left_paddle)
            sprite_group.add(right_paddle)
            self.sprite_groups.append(sprite_group)

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 18)

    def draw_text(self, screen, side, text):
        x_factor = 0.25 if side == 'left' else 0.75
        text_render = self.font.render(text, True, (255, 255, 255))
        
        text_size = list(self.font.size(text))
        x = self._WINDOW_WIDTH * x_factor - 0.5 * text_size[0]
        y = self._FIELD_HEIGHT + .5 * self._SCOREBAR_HEIGHT - 0.5 * text_size[1]
        screen.blit(text_render, (x, y))

    def draw_genome_scores(self, screen):
        row = 0
        height_idx = 0

        fitnesses = [genome.fitness for genome in self.ge]
        max_fit = max(fitnesses)
        min_fit = min(fitnesses)

        for idx, lpaddle in enumerate(self.left_paddles):
            text = f'{idx}: {str(lpaddle.score)}-{str(self.right_paddles[idx].score)} ({str(self.ge[idx].fitness)})'
            text_size = list(self.font.size(text))

            new_height = height_idx * (text_size[1] + 10)
            if new_height > self._SCOREBAR_HEIGHT - (text_size[1] + 10):
                row += 1
                height_idx = 0
            
            x = 10 + row * 150
            y = self._FIELD_HEIGHT + 10 + height_idx * (text_size[1] + 10) 
            scaled = (self.ge[idx].fitness - min_fit) / (max_fit - min_fit) if max_fit != min_fit else 0
            text_render = self.font.render(text, True, (255-(scaled*255), scaled * 255, 0))
            screen.blit(text_render, (x, y))

            height_idx += 1

    def draw_field(self, screen):
        screen.fill((0, 0, 0))
        mid_point = self._WINDOW_WIDTH/2 - self._LINE_WIDTH/2
        pygame.draw.line(screen, (255, 255, 255), [mid_point, 0], [mid_point, self._FIELD_HEIGHT], self._LINE_WIDTH)
        pygame.draw.line(screen, (255, 255, 255), [0, self._FIELD_HEIGHT], [self._WINDOW_WIDTH, self._FIELD_HEIGHT], self._LINE_WIDTH)

        self.draw_genome_scores(screen)

    def check_collisions(self):
        for idx, ball in enumerate(self.balls):
            collisions = pygame.sprite.spritecollide(ball, self.sprite_groups[idx], False)
            if len(collisions) > 1:
                paddle = collisions[1]
                if paddle.side == 'left' and ball.direction_x == -1 or paddle.side == 'right' and ball.direction_x == 1:
                    ball.bounce(paddle_y=paddle.rect.y, paddle_height=paddle._height)

    def run_ai(self):
        for idx, ball in enumerate(self.balls):
            for paddle in [self.left_paddles[idx], self.right_paddles[idx]]:
                if paddle._controls == 'simple_ai':
                    self.run_simple_ai(ball, paddle)
                elif paddle._controls == 'smart_ai':
                    self.run_smart_ai(ball, paddle)
                elif paddle._controls == 'neat':
                    self.run_neat(ball, paddle, idx)

    def run_simple_ai(self, ball, paddle):
        if paddle.rect.y < ball.y:
            paddle.move_down()
        elif paddle.rect.y > ball.y:
            paddle.move_up()
    
    def run_smart_ai(self, ball, paddle):
        if ((ball.direction_x == 1 and paddle._offset < self._WINDOW_WIDTH / 2) or
            (ball.direction_x == -1 and paddle._offset > self._WINDOW_WIDTH / 2)):
            target = self._FIELD_HEIGHT / 2 - paddle._height / 2
        else:
            if ball.direction_x == 1:
                ball_dist = self._WINDOW_WIDTH - ball.x - self._PADDLE_OFFSET
            else:
                ball_dist = ball.x - self._PADDLE_OFFSET

            total_change = ball.direction_y * ball_dist

            if total_change + ball.y < 0:
                target = (total_change + ball.y) * -1
            elif total_change + ball.y > self._FIELD_HEIGHT:
                target = self._FIELD_HEIGHT - (total_change - (self._FIELD_HEIGHT - ball.y)) 
            else:
                target = ball.y + total_change
            
            target -= paddle._height / 2

        if paddle.rect.y - target < -2:
            paddle.move_down()
        elif paddle.rect.y - target > 2:
            paddle.move_up()

    def run_neat(self, ball, paddle, idx):
        output = self.nn[idx].activate((ball.x, ball.y, ball.direction_y, paddle.rect.y))

        if output[0] > 0.5:
            paddle.move_down()
        else:
            paddle.move_up()
        
    def reset_sprites(self, side, idx):
        self.left_paddles[idx].reset()
        self.right_paddles[idx].reset()
        self.balls[idx].reset(side=side, paddle_offset=self._PADDLE_OFFSET)

    def check_point_scored(self):
        for idx, ball in enumerate(self.balls):
            if ball.x > self._WINDOW_WIDTH - ball._size:
                self.left_paddles[idx].score += 1
                self.ge[idx].fitness += 5
                self.reset_sprites(side='left', idx=idx)
            elif ball.x < 0:
                self.right_paddles[idx].score += 1
                self.ge[idx].fitness -= 2
                self.left_paddles[idx].has_lost = True
                self.reset_sprites(side='right', idx=idx)

    def run(self):
        global generation_number
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self._WINDOW_WIDTH, self._WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == ord('q')):
                    exit()
            
            for group in self.sprite_groups:
                group.update()
            self.run_ai()
            self.check_point_scored()
            self.check_collisions()
            self.draw_field(screen)

            # Draw only best
            fitnesses = [genome.fitness for genome in self.ge]
            max_idx = fitnesses.index(max(fitnesses))
            self.sprite_groups[max_idx].draw(screen)


            text_render = self.font.render(f'Generation {generation_number}, viewing genome {max_idx}', True, (255, 255, 255))
            screen.blit(text_render, (150, 20))

            clock.tick(self._FPS)
            pygame.display.flip()

            if time.time()-start_time > 30:
                generation_number += 1
                break

    def main(self):
        pygame.init()
        self.run()
        pygame.quit()

def eval_genomes(genomes, config):
    game = Pong(genomes, config)
    game.main()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 10)

    print(f'\nBest genome:\n{winner}')

