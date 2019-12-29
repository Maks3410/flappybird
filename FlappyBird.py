import os
import sys
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50
STEP = 10
player = pygame.sprite.Group()
fon = pygame.sprite.Group()
cls = pygame.sprite.Group()


def load_image(name, color_key=-1):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            if name != 'bckgrd.png':
                image.set_colorkey(pygame.Color('white'))
        else:
            image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Игра Flappy Bird", "",
                  "Правила игры",
                  "Используйте Пробел, чтобы прыгать,",
                  "Пролетайте между колоннами и не врезайтесь!",
                  "Нажмите любую кнопку, чтобы начать."]

    fon = pygame.transform.scale(load_image('bckgrd.png'), (width * 3,
                                                            height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type ==  \
                    pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bckgrd.png'), (width * 3,
                                                              height))
    speed = 1

    def __init__(self, group):
        super().__init__(group)
        self.image = Fon.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def update(self):
        self.rect.x -= Fon.speed
        if self.rect.x == -width * 2:
            self.rect.x = 0


class Bird(pygame.sprite.Sprite):
    image1 = load_image('1.png')
    image2 = load_image('2.png')
    f_speed = 2
    jump_flag = True
    dir_speed = 1

    def __init__(self, group):
        super().__init__(group)
        self.image = Bird.image1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - 30, height // 2 - 25
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = 1

    def update(self):
        if self.rect.y + 50 < height:
            self.rect.y += Bird.f_speed
            if self.dir % 30 == 0:
                self.image = Bird.image2
            elif self.dir % 15 == 0:
                self.image = Bird.image1
            self.dir += Bird.dir_speed

    def jump(self):
        if Bird.jump_flag is True:
            Bird.f_speed = 0
            for i in range(50):
                self.rect.y -= 1
            Bird.f_speed = 2


class Column(pygame.sprite.Sprite):
    cl = load_image('cl.png')
    speed = 2

    def __init__(self, group):
        super().__init__(group)
        self.image = Column.cl
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width, -200 + random.randint(-179, 179)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.x -= Column.speed
        if pygame.sprite.collide_mask(self, bird):
            Column.speed = 0
            Fon.speed = 0
            Bird.f_speed = 0
            Bird.jump_flag = False
            Bird.dir_speed = 0


bird = Bird(player)
back = Fon(fon)
cl = Column(cls)
start_screen()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    screen.fill(pygame.Color('black'))
    if cl.rect.x < width / 2:
        cl = Column(cls)
    fon.update()
    fon.draw(screen)
    player.update()
    player.draw(screen)
    cls.update()
    cls.draw(screen)
    pygame.display.flip()
    clock.tick(75)

terminate()
