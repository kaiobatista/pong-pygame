from random import random, choice
import pygame as pg
from time import sleep
pg.init()
vec = pg.Vector2

WIDTH, HEIGHT = 800, 600

class Player(pg.sprite.Sprite):

    def __init__(self, player_number, *groups) -> None:
        super().__init__(*groups)
        self.width, self.height = 10, 60
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.rect.centery = HEIGHT / 2 + 15
        self.direction = choice(['up', 'down'])
        self.player_keybinds = {
            1: {
            "up": pg.K_w,
            "down": pg.K_s
            },
            2: {
            "up": pg.K_UP,
            "down": pg.K_DOWN
            }
        }

        if player_number == 1:
            self.rect.left = 25
        else:
            self.rect.right = WIDTH - 25
            

        self.player_number = player_number

    def update(self):
        key = pg.key.get_pressed()

        if key[self.player_keybinds[self.player_number]["down"]] and self.rect.bottom < HEIGHT:
            self.rect.y += 10
            self.direction = "up"

        if key[self.player_keybinds[self.player_number]["up"]] and self.rect.y > 0:
            self.rect.y -= 10
            self.direction = "down"
        
        if self.rect.top < 85:
            self.rect.top = 85

        elif self.rect.bottom > HEIGHT - 25:
            self.rect.bottom = HEIGHT - 25


class Ball(pg.sprite.Sprite):
    
    def __init__(self, dir, *groups) -> None:
        super().__init__(*groups)
        self.image = pg.Surface((10, 10))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.direction = dir
        self.speed = 1

        pg.draw.circle(self.image, (112, 47, 150), (5, 5), 5)

    def update(self):
        self.rect.x += 5 * self.direction.x * self.speed
        self.rect.y += 5 * self.direction.y * self.speed

        if self.rect.top <= 85:
            self.direction.y = 1
        
        elif self.rect.bottom >= HEIGHT - 25:
            self.direction.y = -1


class Game:
    
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.all_sprites_group = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.load()
        self.player1 = Player(1, (self.all_sprites_group, self.player_group))
        self.player2 = Player(2, (self.all_sprites_group, self.player_group))
        self.ball = Ball(vec(1 if random() <= 0.5 else -1, 0), self.all_sprites_group)
        self.clock = pg.time.Clock()
        self.winner = None
        self.running = True
        self.play_again = False
        self.score = {
            'p1': 0,
            'p2': 0
        }
        
    
    def load(self):
        self.bg = pg.image.load('src/background3.jpg').convert()
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.bg_start = pg.image.load('src/background-start.jpg').convert()
        self.bg_start = pg.transform.scale(self.bg_start, (WIDTH, HEIGHT))
        

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        
        self.all_sprites_group.update()

        hit = pg.sprite.spritecollide(self.ball, self.player_group, False)
        if hit:
            self.ball.direction.x *= -1
            self.ball.direction.y = 1 if hit[-1].direction == "up" else -1

        if self.ball.rect.left <= 25 or self.ball.rect.right >= WIDTH - 25:
            self.winner = "Player 1" if self.ball.direction.x == 1 else "Player 2"
            self.ball.kill()
            if self.winner == "Player 1":
                self.score['p1'] += 1
            elif self.winner == "Player 2":
                self.score['p2'] += 1
            self.ball = Ball(vec(-1 if self.winner == 'Player 1' else 1), self.all_sprites_group)
            self.ball.rect.y, self.ball.rect.x = HEIGHT / 2, WIDTH / 2

        
        if self.score['p1'] >= 5 or self.score['p2'] >= 5:
            sleep(1)
            self.running = False

    def draw(self):
        self.screen.fill((100, 100, 100))
        self.screen.blit(self.bg, (0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), (20, 80, WIDTH - 40, HEIGHT - (85 + 25 - 10)))
        pg.draw.rect(self.screen, (0, 0, 0), (25, 85, WIDTH - 50, HEIGHT - (85 + 25)))
        pg.draw.rect(self.screen, (255, 255, 255), (WIDTH / 2 - 2.5, 85, 5, HEIGHT - (85 + 25))) # Linha divisória
        self.printonscreen(f"{self.score['p1']} x {self.score['p2']}", (WIDTH / 2 - 50.5, 22), color=(255, 255, 255), font_size=48)
        self.all_sprites_group.draw(self.screen)
        pg.display.flip()

    def run(self):
        while self.running:

            self.clock.tick(30)
            self.update()
            self.draw()
        print('[LOG]: Saiu do while self.running')

    def endscreen(self):
        endscreen = True
        while endscreen:
    
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    endscreen = False
                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        endscreen = False

                    elif event.key == pg.K_SPACE or pg.K_KP_ENTER:
                        self.play_again = True
                        endscreen = False

            self.screen.fill((255, 255, 255))
            self.printonscreen(f'{self.winner} won!', (WIDTH / 2 - 80, HEIGHT / 6))
            self.printonscreen('Press "ENTER" key to keep playing!', (WIDTH / 2 - 225, HEIGHT / 4 + 50))
            self.printonscreen('Press "Q" to exit game.', (WIDTH / 2 - 150, HEIGHT / 2), color=(255, 20, 0))
            pg.display.flip()
    
    def startscreen(self):
        startscreen = True
        while startscreen:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()

                elif e.type == pg.KEYDOWN:
                    startscreen = False

                elif e.type == pg.MOUSEBUTTONUP:
                    mouse_pos = pg.mouse.get_pos()

                    if mouse_pos[0] >= WIDTH / 2 - 100 and mouse_pos[1] >= HEIGHT / 2:

                        if mouse_pos[0] <= WIDTH / 2 + 100 and mouse_pos[1] <= HEIGHT / 2 + 60:
                            startscreen = False
                            continue
        
            self.screen.fill((20, 255, 0))
            self.screen.blit(self.bg_start, (0, 0))
            pg.draw.rect(self.screen, (49, 17, 82), (WIDTH / 2 - 100, HEIGHT / 2, 200, 60))
            self.printonscreen('PLAY', (WIDTH / 2 - 35, HEIGHT / 2 + 17), color=(255, 255, 255))
            self.printonscreen('Ping Pong', (WIDTH / 2 - 70, HEIGHT / 2 - 200), color=(255, 255, 255))
            pg.display.flip()

    def printonscreen(self, text, pos, color=(0, 0, 0), font_size=30):
        font = pg.font.SysFont('arial', font_size)
        textsurface = font.render(text, False, color)
        self.screen.blit(textsurface, pos)


if __name__ == '__main__':
    game = Game()
    game.startscreen()
    game.run()
    game.endscreen()
    while game.play_again:
        print('[LOG]: Iniciando')
        game = Game()
        game.run()
        game.endscreen()
    pg.quit()
    quit()
