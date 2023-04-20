import math
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('resources/space_background.png')

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('resources/enemy.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('resources/player.png')
playerX = 375
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Enemy
enemy = pygame.image.load('resources/enemy.png')
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Bullet

bulletImg = pygame.image.load('resources/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 25, y + 4))


def isCollision(enemyX, enemyY, bulletX, bulletY, number):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < number:
        return True
    else:
        return False


for i in range(num_of_enemies):
    enemy_Img.append(pygame.image.load('resources/enemy.png'))
    enemyX.append(random.randint(0, 740))
    enemyY.append(random.randint(60, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def resetEnemyNScore():
    global bullet_state, score_value
    score_value=0
    for i in range(num_of_enemies):
        bullet_state = "ready"
        enemyX[i] = random.randint(0, 740)
        enemyY[i] = random.randint(60, 150)


def enemy(x, y, i):
    screen.blit(enemy_Img[i], (x, y))


def set_background():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


def keyboard_logic():
    global running, playerX_change, bulletX, playerX
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750


def enemy_move():
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 740:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)


def enemy_bullet_collision():
    global bulletY, bullet_state, score_value
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, 25)
        if collision and bullet_state == "fire":
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 740)
            enemyY[i] = random.randint(60, 150)


def bullet_miss_reload():
    global bulletY, bulletX, bullet_state
    if bulletY <= 0:
        bulletY = playerY
        bulletX = playerX

        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bullet_state == "ready":
        bulletY = playerY
        bulletX = playerX


def player_enemy_collision():
    global gameOver
    global running
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY, 30)
        if collision:
            gameOver = True


running = True
gameOver = False
while running:
    set_background()
    keyboard_logic()
    enemy_move()
    player_enemy_collision()
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gameOver = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('33')
                    gameOver = False
                    resetEnemyNScore()
    enemy_bullet_collision()
    bullet_miss_reload()
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
