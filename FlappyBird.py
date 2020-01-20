import os
import sys
import pygame
import random
import sqlite3

pygame.init()
clock = pygame.time.Clock()

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50
STEP = 10
score = 0
player = pygame.sprite.Group()
fon = pygame.sprite.Group()
cls = pygame.sprite.Group()
btns = pygame.sprite.Group()
running = True
con = sqlite3.connect("flappybird.db")
cur = con.cursor()
pygame.mixer.music.load('data/Summertime.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
bs = []
flag = True


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if name.endswith(".png"):
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global bs
    fon = pygame.transform.scale(load_image('start.jpg'), (width,
                                                           height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 285 and event.pos[1] > 180 and event.pos[
                        0] < 415 and event.pos[1] < 215:
                    bs = (0.1, -3.5, 'easy')
                    return
                elif event.pos[0] > 285 and event.pos[1] > 230 and event.pos[
                        0] < 415 and event.pos[1] < 270:
                    bs = (0.15, -4.5, 'medium')
                    return
                elif event.pos[0] > 285 and event.pos[1] > 280 and event.pos[
                        0] < 415 and event.pos[1] < 320:
                    bs = (0.3, -6.5, 'hard')
                    return
                elif event.pos[0] > 285 and event.pos[1] > 330 and event.pos[
                        0] < 415 and event.pos[1] < 370:
                    records()
        pygame.display.flip()
        clock.tick(FPS)


def records():
    global running
    fon = pygame.transform.scale(load_image('records_fon.png'), (width,
                                                                 height))
    screen.blit(fon, (0, 0))

    menu = pygame.sprite.Group()
    menu_btn = pygame.sprite.Sprite(menu)
    menu_btn.image = load_image('menu.png')
    menu_btn.rect = menu_btn.image.get_rect()
    menu_btn.rect.x = 560
    menu_btn.rect.y = 12
    menu.draw(screen)

    font = pygame.font.Font(None, 40)

    text_easy = font.render('Easy:', 1, (255, 255, 255))
    text_x = 100
    text_y = 125
    screen.blit(text_easy, (text_x, text_y))

    text_medium = font.render('Medium:', 1, (255, 255, 255))
    text2_x = 300
    text2_y = 125
    screen.blit(text_medium, (text2_x, text2_y))

    text_hard = font.render('Hard:', 1, (255, 255, 255))
    text3_x = 525
    text3_y = 125
    screen.blit(text_hard, (text3_x, text3_y))

    easy = sorted(cur.execute("""SELECT score from score
                          where level = 'easy'""").fetchall())
    medium = sorted(cur.execute("""SELECT score from score
                            where level = 'medium'""").fetchall())
    hard = sorted(cur.execute("""SELECT score from score
                          where level = 'hard'""").fetchall())

    for i in range(1, 4):
        x1, x2, x3 = 100, 300, 525
        y = 175
        if i == 1:
            for j in range(1, 4):
                text = font.render('{}) {}'.format(j, easy[-j][0]), 1,
                                   (255, 255, 255))
                screen.blit(text, (x1, y + (j - 1) * 50))
        elif i == 2:
            for j in range(1, 4):
                text = font.render('{}) {}'.format(j, medium[-j][0]), 1,
                                   (255, 255, 255))
                screen.blit(text, (x2, y + (j - 1) * 50))
        elif i == 3:
            for j in range(1, 4):
                text = font.render('{}) {}'.format(j, hard[-j][0]), 1,
                                   (255, 255, 255))
                screen.blit(text, (x3, y + (j - 1) * 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = True
                    return
                elif event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (560 <= event.pos[0] <= 688) and \
                            (12 <= event.pos[1] <= 50):
                        running = True
                        start_screen()
                        return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    global running
    cur.execute("""INSERT INTO score(level, score) VALUES(?, ?)""",
                (bs[2], score))
    con.commit()
    for x in btns:
        x.kill()
    restart_btn = pygame.sprite.Sprite(btns)
    leave_btn = pygame.sprite.Sprite(btns)
    menu_btn = pygame.sprite.Sprite(btns)

    restart_btn.image = load_image('restart.png')
    leave_btn.image = load_image('leave.png')
    menu_btn.image = load_image('menu.png')
    restart_btn.rect = restart_btn.image.get_rect()
    leave_btn.rect = leave_btn.image.get_rect()
    menu_btn.rect = menu_btn.image.get_rect()
    restart_btn.rect.x = 280
    restart_btn.rect.y = 12
    leave_btn.rect.x = 560
    leave_btn.rect.y = 12
    menu_btn.rect.x = 420
    menu_btn.rect.y = 12

    btns.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = True
                    return
                elif event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (280 <= event.pos[0] <= 408) and \
                            (12 <= event.pos[1] <= 50):
                        running = True
                        return
                    if (420 <= event.pos[0] <= 548) and \
                            (12 <= event.pos[1] <= 50):
                        running = True
                        start_screen()
                        cycle()
                    elif (560 <= event.pos[0] <= 688) and \
                            (12 <= event.pos[1] <= 50):
                        terminate()
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


class NightFon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bckgrd2.png'), (width * 3,
                                                               height))
    speed = 1

    def __init__(self, group):
        super().__init__(group)
        self.image = NightFon.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, height

    def update(self):
        if self.rect.y > 0:
            self.rect.y -= 3
        self.rect.x -= Fon.speed
        if self.rect.x == -width * 2:
            self.rect.x = 0


class Bird(pygame.sprite.Sprite):
    speed = 1
    jump_flag = True
    up_flag = False
    dir_speed = 1

    def __init__(self, group, sheet, columns, rows, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.num = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = 1
        self.k = 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global running
        self.mask = pygame.mask.from_surface(self.image)
        if self.jump_flag:
            if 0 < self.rect.y + 50 < height:
                self.rect.y += Bird.speed
                Bird.speed += bs[0]
                self.num += 1
                self.k += 0.1
                self.cur_frame = (round(self.k)) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            else:
                Column.speed = 0
                Fon.speed = 0
                Bird.speed = 0
                Bird.jump_flag = False
                Bird.dir_speed = 0
                running = False

    def jump(self):
        if Bird.jump_flag is True:
            Bird.up_flag = True
            Bird.speed = bs[1]
            self.num = 0


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
        global running
        self.rect.x -= Column.speed
        if pygame.sprite.collide_mask(self, bird):
            Column.speed = 0
            Fon.speed = 0
            Bird.speed = 0
            Bird.jump_flag = False
            Bird.dir_speed = 0
            running = False


def reset():
    global player, fon, cls, bird, back, cl, score, flag
    Fon.image = pygame.transform.scale(load_image('bckgrd.png'),
                                       (width * 3,
                                        height))
    if flag is False:
        pygame.mixer.music.load('data/Summertime.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
    player = pygame.sprite.Group()
    fon = pygame.sprite.Group()
    cls = pygame.sprite.Group()
    bird = Bird(player, load_image("bird_sheet5x1.png"), 5, 1, width // 2,
                height // 2)
    back = Fon(fon)
    cl = Column(cls)
    Fon.speed = 1
    Bird.speed = 1
    Column.speed = 2
    score = 0
    flag = True
    Bird.jump_flag = True


font = pygame.font.Font(None, 40)

start_screen()
closed = False


def cycle():
    global score, cl, flag, back, text_w, text_h
    while not closed:
        reset()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        bird.jump()
            screen.fill(pygame.Color('black'))
            if cl.rect.x < width / 2 - 130:
                cl = Column(cls)
                score += 1
            fon.update()
            fon.draw(screen)
            player.update()
            player.draw(screen)
            cls.update()
            cls.draw(screen)
            text = font.render("Score: {}".format(score), 1, (0, 0, 0))
            text_x = 12
            text_y = 12
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            if score % 40 == 0 and score > 1 and flag:
                NightFon.image = pygame.transform.scale(
                    load_image('bckgrd.png'),
                    (width * 3,
                     height))
                back = NightFon(fon)
                flag = False
                pygame.mixer.music.load('data/Summertime.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            elif score % 20 == 0 and score > 1 and flag:
                NightFon.image = pygame.transform.scale(
                    load_image('bckgrd2.png'),
                    (width * 3,
                     height))
                back = NightFon(fon)
                flag = False
                pygame.mixer.music.load('data/AlanWalkerFaded.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            elif str(score)[-1] == 9:
                flag = True
            pygame.display.flip()
            clock.tick(75)

        end_screen()


cycle()
terminate()
