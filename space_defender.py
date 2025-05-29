import pygame
import random

# Aloitus
pygame.init()

# Pelin ikkunan asetukset
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")

# Värit
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Lisätty punainen väri ammuksille

# Pelaajan alus (kolmion muoto, terävä kärki ylöspäin)
player_points = [(WIDTH // 2, HEIGHT - 80), (WIDTH // 2 - 25, HEIGHT - 50), (WIDTH // 2 + 25, HEIGHT - 50)]
player_speed = 5  # Pelaajan nopeus

# Ammukset
bullets = []
bullet_speed = 7
bullet_cooldown = 250  # Aika millisekunteina ammusten välillä
last_shot_time = pygame.time.get_ticks()  # Viimeisimmän ammuksen aika

# Pelisilmukka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Näppäimistön syötteet
    keys = pygame.key.get_pressed()

    # Ampuminen
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
        bullet_x = player_points[0][0]
        bullet_y = player_points[0][1]
        bullets.append([bullet_x, bullet_y])
        last_shot_time = current_time

    # Pelaajan liikkuminen sivuttain (x-akselilla)
    if keys[pygame.K_LEFT]:
        can_move = True
        for point in player_points:
            if point[0] <= 0:  # Tarkista, onko mikään piste vasemmassa reunassa
                can_move = False
                break
        if can_move:
            for i in range(3):
                player_points[i] = (player_points[i][0] - player_speed, player_points[i][1])
    if keys[pygame.K_RIGHT]:
        can_move = True
        for point in player_points:
            if point[0] >= WIDTH:  # Tarkista, onko mikään piste oikeassa reunassa
                can_move = False
                break
        if can_move:
            for i in range(3):
                player_points[i] = (player_points[i][0] + player_speed, player_points[i][1])
    # Pelaajan liikkuminen ylös ja alas (y-akselilla)
    if keys[pygame.K_UP]:
        can_move = True
        for point in player_points:
            if point[1] <= 0:  # Tarkista, onko mikään piste yläreunassa
                can_move = False
                break
        if can_move:
            for i in range(3):
                player_points[i] = (player_points[i][0], player_points[i][1] - player_speed)
    if keys[pygame.K_DOWN]:
        can_move = True
        for point in player_points:
            if point[1] >= HEIGHT:  # Tarkista, onko mikään piste alareunassa
                can_move = False
                break
        if can_move:
            for i in range(3):
                player_points[i] = (player_points[i][0], player_points[i][1] + player_speed)

    # Taustan piirto
    screen.fill(BLACK)

    # Ammusten liikkuminen ja piirto
    for bullet in bullets:
        bullet[1] -= bullet_speed  # Liikuta ammusta ylöspäin
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), 5)  # Piirrä ammus
        if bullet[1] < 0:  # Poista ammukset, jotka menevät ruudun ulkopuolelle
            bullets.remove(bullet)


    # Pelaajan aluksen piirto kolmiona
    pygame.draw.polygon(screen, WHITE, player_points)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()