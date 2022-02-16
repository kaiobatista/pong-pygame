import pygame as pg
pg.init()
vec = pg.Vector2

player_keybinds = {
    1: {
    "up": pg.K_w,
    "down": pg.K_s
    },
    2: {
    "up": pg.K_UP,
    "down": pg.K_DOWN
    }
}

class Player(pg.sprite.Sprite):

    def __init__(self, player_number, *groups) -> None:
        super().__init__(*groups)
        self.width, self.height = 10, 60
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.rect.centery = HEIGHT / 2
        self.direction = ''

        if player_number == 1:
            self.rect.left = 0
        else:
            self.rect.right = WIDTH
            

        self.player_number = player_number

    def update(self):
        key = pg.key.get_pressed()
        if key[player_keybinds[self.player_number]["down"]] and self.rect.bottom < HEIGHT:
            self.rect.y += 10
            self.direction = "up"

        if key[player_keybinds[self.player_number]["up"]] and self.rect.y > 0:
            self.rect.y -= 10
            self.direction = "down"


class Ball(pg.sprite.Sprite):

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pg.Surface((10, 10))
        self.image.fill((125, 125, 125))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.direction = vec(-1, 0)

    def update(self):
        self.rect.x += 5 * self.direction.x
        self.rect.y += 5 * self.direction.y

        if self.rect.top <= 0:
            self.direction.y = 1
        
        elif self.rect.bottom >= HEIGHT:
            self.direction.y = -1


def printonscreen(text, pos):
    font = pg.font.SysFont('arial', 30)
    textsurface = font.render(text, False, (0, 0, 0))
    screen.blit(textsurface, pos)

all_sprites_group = pg.sprite.Group()
player_group = pg.sprite.Group()

WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))

player1 = Player(1, (all_sprites_group, player_group))
player2 = Player(2, (all_sprites_group, player_group))
ball = Ball(all_sprites_group)

clock = pg.time.Clock()

running = True
while running:

    clock.tick(30)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            continue
    
    all_sprites_group.update()
    hit = pg.sprite.spritecollide(ball, player_group, False)
    if hit:
        ball.direction.x *= -1
        ball.direction.y = 1 if hit[-1].direction == "up" else -1

    if ball.rect.left < 0 or ball.rect.right > WIDTH:
        winner = "Player 1" if ball.direction.x == 1 else "Player 2"
        running = False

    screen.fill((0, 0, 0))
    
    pg.draw.rect(screen, (255, 255, 255), (WIDTH / 2 - 2.5, 0, 5, HEIGHT))
    all_sprites_group.draw(screen)

    pg.display.flip()

endscreen = True
while endscreen:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            endscreen = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                endscreen = False
    
    screen.fill((255, 255, 255))
    printonscreen(f'{winner} won!', (WIDTH / 2 - 75, HEIGHT / 4))
    pg.display.flip()
