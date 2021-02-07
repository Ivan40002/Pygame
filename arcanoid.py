import pygame
import random

WIDTH, HEIGHT = 1200, 800
FPS = 60
LEVEL = 0

paddle_w = 300
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2)
ball = pygame.Rect(random.randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2 + 100, ball_rect, ball_rect)
dx = random.choice([-1, 1])
dy = -1
block_list = []

boost_rect = ''

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Arcanoid')
clock = pygame.time.Clock()

boost = pygame.image.load('boost.webp').convert_alpha()
boost = pygame.transform.scale(boost, (50, 50))
img = pygame.image.load('background.jpg').convert()

font = pygame.font.Font(None, 30)
string_rendered = font.render(f'Уровень: {LEVEL + 1}', 1, pygame.Color('darkgreen'))

def end_screen():
    global screen
    img = pygame.image.load('background.jpg').convert()
    font = pygame.font.Font(None, 150)
    string_rendered = font.render('Конец игры!', 1, pygame.Color('darkgreen'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
        screen.blit(img, (0, 0))
        screen.blit(string_rendered, (300, 300))
        pygame.display.flip()
        clock.tick(FPS)

def start_screen():
    global screen
    runing = True
    img = pygame.image.load('background.jpg').convert()
    font = pygame.font.Font(None, 150)
    font_of_rules = pygame.font.Font(None, 50)
    name_of_game = font.render('Arcanoid', 1, pygame.Color('darkgreen'))
    rules = font_of_rules.render('''Нажимая на стрелочки, перемещайте платформу''', 1, pygame.Color('darkgreen'))
    while runing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                        runing = False
        screen.blit(img, (0, 0))
        screen.blit(name_of_game, (380, 300))
        screen.blit(rules, (170, 700))
        pygame.display.flip()
        clock.tick(FPS)



def load_level():
    global block_list, paddle_w, ball_speed, paddle, boost_rect, string_rendered
    string_rendered = font.render(f'Уровень: {LEVEL + 1}', 1, pygame.Color('darkgreen'))
    boost_rect = ''
    paddle_w = 300
    paddle.width = paddle_w
    with open('levels.txt', 'r') as mapFile:
        lines = mapFile.readlines()
        try:
            level_map = lines[LEVEL * 4:LEVEL * 4 + 4]
            for j in range(4):
                for i in range(10):
                    if level_map[j][i] == '-':
                        block_list.append(pygame.Rect(10 + 120 * i, 100 + 70 * j, 100, 50))
                    elif level_map[j][i] == '#':
                        block_list.append(pygame.Rect(10 + 120 * i, 100 + 70 * j, 100, 51))
                    elif level_map[j][i] == '@':
                        block_list.append(pygame.Rect(10 + 120 * i, 100 + 70 * j, 100, 52))
                    elif level_map[j][i] == '!':
                        block_list.append(pygame.Rect(10 + 120 * i, 100 + 70 * j, 100, 53))
        except IndexError:
            end_screen()
                
                    

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if delta_x == delta_y:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

load_level()
start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.blit(img, (0, 0))
    screen.blit(string_rendered, (0, 0))
    if boost_rect == '' and paddle_w == 300:
        if random.randint(1, 1000) == 1:
            boost_rect = boost.get_rect()
            boost_rect.center = (random.randint(51, 1149), random.randint(400, 600))
    for block in block_list:
        if block.height == 50:
            pygame.draw.rect(screen, pygame.Color('brown'), block)
        elif block.height == 51:
            pygame.draw.rect(screen, pygame.Color('darkgrey'), block)
        elif block.height == 52:
            pygame.draw.rect(screen, pygame.Color('green'), block)
        elif block.height == 53:
            pygame.draw.rect(screen, pygame.Color('gold'), block)
    pygame.draw.rect(screen, pygame.Color('orange'), paddle)
    pygame.draw.circle(screen, pygame.Color('red'), ball.center, ball_radius)
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    hit_index = ball.collidelist(block_list)
    if boost_rect != '':
        screen.blit(boost, boost_rect)
        if ball.colliderect(boost_rect):
            paddle_w += 100
            paddle.width = paddle_w
            boost_rect = ''
    if hit_index != -1:
        if block_list[hit_index].height == 50:
            hit_rect = block_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
        elif block_list[hit_index].height == 51:
            hit_rect = block_list[hit_index]
            dx0 = dx
            dy0 = dy
            block_list[hit_index].height = 50
            pygame.draw.rect(screen, pygame.Color('brown'), block_list[hit_index])
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            if dx0 != dx and dy0 != dy:
                ball.x += ball_speed * dx
                ball.y += ball_speed * dy
            elif dx0 != dx:
                ball.x += ball_speed * dx
            elif dy0 != dy:
                ball.y += ball_speed * dy
        elif block_list[hit_index].height == 52:
            hit_rect = block_list[hit_index]
            dx0 = dx
            dy0 = dy
            block_list[hit_index].height = 51
            pygame.draw.rect(screen, pygame.Color('grey'), block_list[hit_index])
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            if dx0 != dx and dy0 != dy:
                ball.x += ball_speed * dx
                ball.y += ball_speed * dy
            elif dx0 != dx:
                ball.x += ball_speed * dx
            elif dy0 != dy:
                ball.y += ball_speed * dy
        elif block_list[hit_index].height == 53:
            hit_rect = block_list[hit_index]
            dx0 = dx
            dy0 = dy
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            if dx0 != dx and dy0 != dy:
                ball.x += ball_speed * dx
                ball.y += ball_speed * dy
            elif dx0 != dx:
                ball.x += ball_speed * dx
            elif dy0 != dy:
                ball.y += ball_speed * dy
    if ball.top < 0:
        LEVEL += 1
        if LEVEL != 0 and LEVEL % 3 == 0:
            ball_speed += 1
        block_list = []
        ball = pygame.Rect(random.randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2 + 100, ball_rect, ball_rect)
        dx = random.choice([-1, 1])
        dy = -1
        load_level()
    if ball.bottom > HEIGHT:
        block_list = []
        ball = pygame.Rect(random.randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2 + 100, ball_rect, ball_rect)
        dx = random.choice([-1, 1])
        dy = -1
        load_level()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed
    pygame.display.flip()
    clock.tick(FPS)
