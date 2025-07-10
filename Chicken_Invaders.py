import pygame
import os
import random

pygame.init()
pygame.mixer.init()
# Screen
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chicken Invaders")
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Image", "background1.jpg")), (WIDTH, HEIGHT))
# Enemy
chicken_image = pygame.image.load(os.path.join('Image', 'Chicken1.png'))
chicken_transform = pygame.transform.scale(chicken_image, (50, 50))
FIRE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FIRE_EVENT, 1000)

linkPlanes = pygame.image.load(os.path.join('Image', 'planes.png'))
PLANE = pygame.transform.scale(linkPlanes, (60, 60))
linkBullet = pygame.image.load(os.path.join('Image', 'Heart.png'))

BULLET_SOUND = pygame.mixer.Sound('Sound/laser.wav')
CHICKEN_EXPLORE_SOUND = pygame.mixer.Sound('Sound/gun-shoot.mp3')
GAMEOVER = pygame.mixer.Sound('Sound/gameover.mp3')

BULLET = pygame.transform.scale(linkBullet, (10, 10))

main_font = pygame.font.SysFont("times", 50)
font_of_score = pygame.font.SysFont("times", 40)


class Display:
    def __init__(self):
        SCREEN.blit(BG, (0, 0))


class Plane:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH / 2, 750, 50, 50)

        self.max_of_bullet = 8

        # Vận tốc của máy bay
        self.VPlanes = 5

        # Danh sách các viên đạn mà máy bay bắn ra
        self.listBullet = []

        # Tốc độ của viên đạn
        self.speed_bullet = 5

        #
        self.health = 1

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def draw(self):
        SCREEN.blit(PLANE, (self.rect.x, self.rect.y))

    def draw_bullet(self):
        for bullet in self.listBullet:
            bullet.y -= self.speed_bullet
            SCREEN.blit(BULLET, (bullet.x, bullet.y))
            if bullet.y < 0:
                self.listBullet.remove(bullet)

    def on_key_pressed(self, key_pressed):
        if (key_pressed[pygame.K_LEFT]) and self.rect.x - self.VPlanes >= 0:
            self.rect.x -= self.VPlanes
        if (key_pressed[pygame.K_RIGHT]) and self.rect.x + self.VPlanes + PLANE.get_width() < WIDTH:
            self.rect.x += self.VPlanes
        if (key_pressed[pygame.K_DOWN]) and self.rect.y + self.VPlanes + PLANE.get_height() < HEIGHT:
            self.rect.y += self.VPlanes
        if (key_pressed[pygame.K_UP]) and self.rect.y - self.VPlanes >= 0:
            self.rect.y -= self.VPlanes

    def add_new_bullet(self):
        bullet = pygame.Rect(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, 10, 5)
        self.listBullet.append(bullet)

    def on_attack(self, list_of_chicken):
        for chicken in list_of_chicken:
            if self.rect.colliderect(chicken):
                self.health = self.health - 1
                list_of_chicken.remove(chicken)


class Chicken:
    def __init__(self):
        self.x = random.randrange(50, 1445)
        self.y = random.randrange(-1400, -100)

        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.wave_length = 5
        self.enemy_vel = 1
        self.level = 1

    def move(self):
        new_y = self.rect.y + self.enemy_vel
        self.rect.y = new_y
        self.y = self.rect.y

    def draw(self):
        SCREEN.blit(chicken_transform, (self.rect.x, self.rect.y))

    def on_attack(self, list_of_bullet):
        for bullet in list_of_bullet:
            if self.rect.colliderect(bullet):
                list_of_bullet.remove(bullet)
                return True
        return False


def show_score_text(score):
    draw_text = font_of_score.render('Score: ' + str(score), 1, (255, 0, 0))

    SCREEN.blit(draw_text, (20, 20))


def show_lose_text():
    draw_text = main_font.render('You lose!' + ' Use SPACE to replay', 1, (0, 255, 0))
    SCREEN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height()))


def play_game():
    chickens = []

    # Khởi tạo máy bay
    plane = Plane()

    is_game_over = False
    score = 0

    while True:

        if not is_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(plane.listBullet) < plane.max_of_bullet:
                        plane.add_new_bullet()
                        BULLET_SOUND.play()

                if event.type == FIRE_EVENT:
                    chickens.append(Chicken())
                    chickens.append(Chicken())

            Display()
            for chicken in chickens:
                chicken.draw()
                chicken.move()
                if chicken.y > HEIGHT:
                    chickens.remove(chicken)

                if chicken.on_attack(plane.listBullet):
                    score = score + 1
                    chickens.remove(chicken)
                    CHICKEN_EXPLORE_SOUND.play()

            plane.draw()
            plane.on_key_pressed(pygame.key.get_pressed())
            plane.draw_bullet()
            plane.on_attack(chickens)

            if plane.health <= 0:
                is_game_over = True
        else:
            show_lose_text()
            GAMEOVER.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play_game()
                        break

        show_score_text(score)
        pygame.display.update()


play_game()
