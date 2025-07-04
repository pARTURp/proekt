from pygame import *
import math
import random
import os

init()

WIDTH, HEIGHT = 640, 480
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Меню с 3 мини-играми")

FONT = font.SysFont(None, 48)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Button:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rendered = FONT.render(text, True, WHITE)
        self.rect = self.rendered.get_rect(center=pos)

    def draw(self, screen, hover=False):
        color = BLUE if hover else GRAY
        draw.rect(screen, color, self.rect.inflate(20, 10))
        screen.blit(self.rendered, self.rect)

    def is_hover(self, mouse_pos):
        return self.rect.inflate(20, 10).collidepoint(mouse_pos)

def game1():
    from random import randint as rd, shuffle
    # -------------------- НАСТРОЙКИ ИГРЫ --------------------
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 500
    WINDOW_BACKGROUND = 'background_game1.jpg'
    FPS = 100
    display.set_caption("лабиринт")

    finish = False

    font.init()
    my_font = font.Font(None, 100)
    FONT = font.Font(None, 36)
    win_text = my_font.render('Победа', 0, (100, 255, 0))
    text = FONT.render('Нажми R для перезапуска ESC для выхода', 0, (255, 255, 255))

    # -------------------- ИНИЦИАЛИЗАЦИЯ ЭКРАНА --------------------
    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = transform.scale(image.load(WINDOW_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = time.Clock()

    # -------------------- КЛАССЫ --------------------
    class GameSprite(sprite.Sprite):
        def __init__(self, x, y, width, height, speed, img_path):
            super().__init__()
            self.speed = speed
            self.image = transform.scale(image.load(img_path), (width, height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def show(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    class Player(GameSprite):
        def move(self):
            keys = key.get_pressed()
            dx, dy = 0, 0
            if keys[K_w] and self.rect.y > 0:
                dy = -self.speed
            if keys[K_s] and self.rect.y < WINDOW_HEIGHT - self.rect.height:
                dy = self.speed
            if keys[K_a] and self.rect.x > 0:
                dx = -self.speed
            if keys[K_d] and self.rect.x < WINDOW_WIDTH - self.rect.width:
                dx = self.speed

            if not self.check_collision(dx, 0):
                self.rect.x += dx
            if not self.check_collision(0, dy):
                self.rect.y += dy

        def check_collision(self, dx, dy):
            future_rect = self.rect.move(dx, dy)
            for wall in walls:
                if future_rect.colliderect(wall.rect):
                    return True
            return False

    class Enemy(GameSprite):
        def move_towards_player(self, target):
            if self.rect.x < target.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > target.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < target.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > target.rect.y:
                self.rect.y -= self.speed

    class goal(GameSprite):
        def move_goal(self):
            self.rect.y += rd(-20, 10)
            self.rect.x += rd(-20, 10)

    class Wall(sprite.Sprite):
        def __init__(self, x, y, width, height, color=(0, 0, 0)):
            super().__init__()
            self.image = Surface((width, height))
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft=(x, y))

        def show(self):
            window.blit(self.image, self.rect)

    def create_goals():
        positions = [(0, 0), (650, 450), (650, 0)]
        shuffle(positions)
        g1 = goal(*positions[0], 50, 50, 0, 'goal_game1.png')
        g2 = goal(*positions[1], 50, 50, 0, 'goal_game1.png')
        g3 = goal(*positions[2], 50, 50, 0, 'goal_game1.png')
        return g1, g2, g3

    # -------------------- СОЗДАНИЕ СПРАЙТОВ --------------------
    player = Player(0, 450, 50, 50, 4, 'player_game1.png')
    enemy = Enemy(300, 300, 50, 50, 1.4, 'enemy_game1.png')
    goalf1, goalf, goalt = create_goals()

    # -------------------- СТЕНЫ --------------------
    walls = [                                       #справо от игрока
        Wall(x=615, y=130, width=15, height=400), #вертикальная правая стена
        Wall(x=0, y=420, width=530, height=15), #горизонтальная нижняя стена
        Wall(x=230, y=340, width=300, height=15), #горизонтальная стена выше
        Wall(x=515, y=240, width=15, height=100), #вертикальная стена выше

        Wall(x=80, y=60, width=700, height=15), #самая верхняя стена
        Wall(x=230, y=125, width=15, height=215), #вертикальная стена сверху второй гор. стены
        Wall(x=130, y=190, width=15, height=160),
        Wall(x=0, y=190, width=140, height=15),
    ]

    
    # -------------------- ИГРОВОЙ ЦИКЛ --------------------
    while True:
        window.blit(background, (0, 0))
        if not finish:
            player.move()
            enemy.move_towards_player(player)

            if sprite.collide_rect(player, enemy):
                player.rect.x = 0
                player.rect.y = 450
                enemy.rect.x = rd(0, 500)
                enemy.rect.y = rd(0, 500)
                goalf1, goalf, goalt = create_goals()

            if sprite.collide_rect(player, goalf):
                goalf.move_goal()
            elif sprite.collide_rect(player, goalf1):
                goalf1.move_goal()
        if sprite.collide_rect(player, goalt):
            window.blit(win_text, (230, 200))
            finish = True
            window.blit(text, (100, 300))
        player.show()
        enemy.show()
        goalf1.show()
        goalf.show()
        goalt.show()

        for wall in walls:
            wall.show()

        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    display.set_caption("Меню с 3 мини-играми")
                    return
                elif finish and e.key == K_r:
                    finish = False
                    player.rect.x = 0
                    player.rect.y = 450
                    goalf1, goalf, goalt = create_goals()
                    enemy.rect.x = rd(0, 500)
                    enemy.rect.y = rd(0, 500)

        display.flip()
        clock.tick(FPS)



def game2():
    # -------------------- НАСТРОЙКИ ИГРЫ --------------------
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 500
    WINDOW_BACKGROUND = 'background_game1.jpg'
    display.set_caption("андртейл на минималках")

    FPS = 100
    finish = False
    paused = False  # Для паузы при открытии инвентаря

    font.init()
    my_font = font.Font(None, 150)
    small_font = font.Font(None, 36)
    lose_text = my_font.render('Поражение', 0, (255, 0, 0))
    score_text = None
    record_text = None

    # -------------------- ИНИЦИАЛИЗАЦИЯ ЭКРАНА --------------------
    window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = transform.scale(image.load(WINDOW_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = time.Clock()

    # -------------------- ЗАГРУЗКА РЕКОРДА --------------------
    record_file = "record.txt"
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            try:
                record = int(f.read())
            except:
                record = 0
    else:
        record = 0

    score = 0
    health = 100

    inventory = {
        "Золотое яблоко": 1,
        "Пирог": 1,
        "Снег": 1
    }

    def open_inventory():
        nonlocal paused, health
        paused = True
        inventory_font = font.Font(None, 36)
        inventory_font_small = font.Font(None, 34)
        while paused:
            window.blit(background, (0, 0))
            inv_text = inventory_font.render("ИНВЕНТАРЬ", True, (255, 255, 255))
            window.blit(inv_text, (180, 30))
            y = 150
            for idx, (item, count) in enumerate(inventory.items()):
                text = small_font.render(f"{idx+1}. {item} ({count})", True, (255, 255, 255))
                window.blit(text, (100, y))
                y += 40
            hint = inventory_font_small.render("Нажми 1-3, чтобы использовать предмет. ESC - закрыть.", True, (255, 255, 255))
            window.blit(hint, (10, 400))
            display.update()

            for e in event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        paused = False
                    elif e.key == K_1 and inventory["Золотое яблоко"] > 0:
                        health = min(100, health + 60)
                        inventory["Золотое яблоко"] -= 1
                        paused = False
                    elif e.key == K_2 and inventory["Пирог"] > 0:
                        health = min(100, health + 30)
                        inventory["Пирог"] -= 1
                        paused = False
                    elif e.key == K_3 and inventory["Снег"] > 0:
                        health = min(100, health + 10)
                        inventory["Снег"] -= 1
                        paused = False

    # -------------------- КЛАССЫ --------------------
    class GameSprite(sprite.Sprite):
        def __init__(self, x, y, width, height, speed, img_path):
            super().__init__()
            self.speed = speed
            self.image = transform.scale(image.load(img_path), (width, height))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.vel_x = 0
            self.vel_y = 0

        def show(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    class Player(GameSprite):
        def update(self):
            keys = key.get_pressed()
            if keys[K_w] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < WINDOW_HEIGHT - self.rect.height:
                self.rect.y += self.speed
            if keys[K_a] and self.rect.x > 0:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < WINDOW_WIDTH - self.rect.width:
                self.rect.x += self.speed

    class Enemy(GameSprite):
        def update(self):
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or
                self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
                self.kill()

    # -------------------- СПРАЙТЫ --------------------
    player = Player(x=300, y=250, width=57, height=70, speed=5, img_path='player_game2.png')
    player_group = sprite.Group(player)
    enemys = sprite.Group()

    spawn_timer = 0
    spawn_interval = 500

    # -------------------- ОСНОВНОЙ ЦИКЛ --------------------
    while True:
        dt = clock.tick(FPS)
        if not paused:
            spawn_timer += dt

        for some_event in event.get():
            if some_event.type == QUIT:
                quit()
                return
            elif some_event.type == KEYDOWN:
                if finish:
                    if some_event.key == K_r:
                        finish = False
                        health = 100
                        player.rect.x = 300
                        player.rect.y = 250
                        enemys.empty()
                        score = 0
                        spawn_timer = 0
                    elif some_event.key == K_ESCAPE:
                        return
                elif some_event.key == K_ESCAPE:
                    display.set_caption("Меню с 3 мини-играми")
                    return
                elif some_event.key == K_LCTRL:
                    open_inventory()

        if not finish and not paused:
            window.blit(background, (0, 0))

            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                side = random.choice(['left', 'right', 'top', 'bottom'])
                speed = random.randint(3, 5)
                enemy = Enemy(0, 0, 80, 60, 0, 'enemy_game2.png')

                if side == 'left':
                    enemy.rect.x = -enemy.rect.width
                    enemy.rect.y = random.randint(0, WINDOW_HEIGHT - enemy.rect.height)
                    enemy.vel_x = speed
                    enemy.vel_y = 0
                elif side == 'right':
                    enemy.rect.x = WINDOW_WIDTH
                    enemy.rect.y = random.randint(0, WINDOW_HEIGHT - enemy.rect.height)
                    enemy.vel_x = -speed
                    enemy.vel_y = 0
                elif side == 'top':
                    enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
                    enemy.rect.y = -enemy.rect.height
                    enemy.vel_x = 0
                    enemy.vel_y = speed
                else:
                    enemy.rect.x = random.randint(0, WINDOW_WIDTH - enemy.rect.width)
                    enemy.rect.y = WINDOW_HEIGHT
                    enemy.vel_x = 0
                    enemy.vel_y = -speed

                enemys.add(enemy)
                score += 1

            player_group.update()
            enemys.update()

            player_group.draw(window)
            enemys.draw(window)

            score_text = small_font.render(f"Счет: {score}", True, (255, 255, 255))
            record_text = small_font.render(f"Рекорд: {record}", True, (255, 255, 0))
            health_text = small_font.render(f"Здоровье: {health}/100", True, (255, 0, 0))

            window.blit(score_text, (10, 10))
            window.blit(record_text, (10, 40))
            window.blit(health_text, (10, 70))

            if sprite.spritecollide(player, enemys, True):
                damage = random.randint(10, 30)
                health -= damage
                if health <= 0:
                    health = 0
                    window.blit(lose_text, (50, 200))
                    finish = True
                    if score > record:
                        record = score
                        with open(record_file, "w") as f:
                            f.write(str(record))
        elif finish:
            hint = small_font.render("Нажми R для перезапуска или ESC для выхода", True, (255, 255, 255))
            window.blit(hint, (50, 350))

        display.update()





def game3():
    WIDTH, HEIGHT = 700, 500
    WHITE = (255, 255, 255)
    FPS = 100
    WINDOW_BACKGROUND = 'background_game1.jpg'

    font.init()
    my_font = font.Font(None, 36)
    FONT = font.Font(None, 36)
    text = my_font.render('Нажми R для перезапуска ESC для выхода', 0, (255, 255, 255))
    background = transform.scale(image.load(WINDOW_BACKGROUND), (WIDTH, HEIGHT))

    screen = display.set_mode((WIDTH, HEIGHT))
    display.set_caption("шутер")
    clock = time.Clock()

    # Загрузка рекорда из файла
    record_file = 'record_game2.txt'
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            try:
                record = int(f.read())
            except:
                record = 0
    else:
        record = 0

    class Player(sprite.Sprite):
        def __init__(self, x, y, img_path):
            super().__init__()
            self.original_image = transform.scale(image.load(img_path), (30, 70))
            self.image = self.original_image
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 5

        def update(self):
            keys = key.get_pressed()
            if keys[K_w] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed
            if keys[K_a] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.right < WIDTH:
                self.rect.x += self.speed

            # Поворот в сторону мыши
            mx, my = mouse.get_pos()
            dx = mx - self.rect.centerx
            dy = my - self.rect.centery
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            self.image = transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        def fire(self):
            mx, my = mouse.get_pos()
            dx = mx - self.rect.centerx
            dy = my - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1
            dx /= dist
            dy /= dist
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy, 'bullet_game3.png')
            bullets.add(bullet)

    class Enemy(sprite.Sprite):
        def __init__(self, x, y, img_path):
            super().__init__()
            self.image = transform.scale(image.load(img_path), (40, 70))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 2

        def update(self, player_pos):
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
                self.kill()

    class Bullet(sprite.Sprite):
        def __init__(self, x, y, dx, dy, img_path):
            super().__init__()
            self.image = transform.scale(image.load(img_path), (20, 40))
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            self.image = transform.rotate(self.image, angle)
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 10
            self.dx = dx
            self.dy = dy

        def update(self):
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
            if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
                self.kill()

    player = Player(WIDTH // 2, HEIGHT // 2, 'player.png')
    player_group = sprite.Group(player)
    enemys = sprite.Group()
    bullets = sprite.Group()

    spawn_timer = 0
    spawn_interval = 250

    finish = False
    score = 0

    while True:
        dt = clock.tick(FPS)
        spawn_timer += dt

        for e in event.get():
            if e.type == QUIT:
                if score > record:
                    with open(record_file, 'w') as f:
                        f.write(str(score))
                quit()
            elif e.type == KEYDOWN:
                if e.key == K_r and finish:
                    finish = False
                    player.rect.center = (WIDTH // 2, HEIGHT // 2)
                    enemys.empty()
                    bullets.empty()
                    score = 0
                    spawn_timer = 0
                if e.key == K_ESCAPE:
                    display.set_caption("Меню с 3 мини-играми")
                    if score > record:
                        with open(record_file, 'w') as f:
                            f.write(str(score))
                    return
                if e.key == K_SPACE and not finish:
                    player.fire()

        if not finish:
            screen.blit(background, (0, 0))

            if spawn_timer >= spawn_interval:
                spawn_timer = 0
                side = random.choice(['left', 'right', 'top', 'bottom'])
                if side == 'left':
                    x = -30
                    y = random.randint(0, HEIGHT)
                elif side == 'right':
                    x = WIDTH + 30
                    y = random.randint(0, HEIGHT)
                elif side == 'top':
                    x = random.randint(0, WIDTH)
                    y = -30
                else:
                    x = random.randint(0, WIDTH)
                    y = HEIGHT + 30

                enemy = Enemy(x, y, 'enemy.png')
                enemys.add(enemy)

            player_group.update()
            enemys.update(player.rect.center)
            bullets.update()

            player_group.draw(screen)
            enemys.draw(screen)
            bullets.draw(screen)

            hits = sprite.groupcollide(bullets, enemys, True, True)
            score += len(hits)

            if sprite.spritecollide(player, enemys, False):
                finish = True
                screen.blit(text, (100, 300))
                if score > record:
                    record = score
                    with open(record_file, 'w') as f:
                        f.write(str(record))

            score_text = FONT.render(f'Счет: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

            record_text = FONT.render(f'Рекорд: {record}', True, WHITE)
            screen.blit(record_text, (10, 50))

            info_text = FONT.render("Пробел - стрелять, ESC - выйти", True, WHITE)
            screen.blit(info_text, info_text.get_rect(center=(WIDTH // 2, 20)))

        display.flip()


def quit_game():
    quit()
    exit()

def main_menu():
    display.set_caption("Меню с 3 мини-играми")
    buttons = [
        Button("лабиринт", (WIDTH//2, HEIGHT//2 - 110)),
        Button("андртейл", (WIDTH//2, HEIGHT//2 - 40)),
        Button("стрелялка", (WIDTH//2, HEIGHT//2 + 30)),
        Button("Выход", (WIDTH//2, HEIGHT//2 + 100)),
    ]

    while True:
        screen.fill(BLACK)
        mouse_pos = mouse.get_pos()

        for e in event.get():
            if e.type == QUIT:
                quit_game()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                for i, btn in enumerate(buttons):
                    if btn.is_hover(mouse_pos):
                        if i == 0:
                            game1()
                        elif i == 1:
                            game2()
                        elif i == 2:
                            game3()
                        elif i == 3:
                            quit_game()

        for btn in buttons:
            btn.draw(screen, btn.is_hover(mouse_pos))

        title = FONT.render("Выберите игру", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 170)))

        display.flip()

if __name__ == "__main__":
    main_menu()
