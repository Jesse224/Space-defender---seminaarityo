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
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Lisätty sininen väri ammuksille

# Pelaajan alus (kolmion muoto, terävä kärki ylöspäin)
player_points = [(WIDTH // 2, HEIGHT - 80), (WIDTH // 2 - 25, HEIGHT - 50), (WIDTH // 2 + 25, HEIGHT - 50)]
player_speed = 5  # Pelaajan nopeus
player_is_alive = True  # Pelaajan elossaolotila

# Ammukset
bullets = []
bullet_speed = 7
bullet_cooldown = 250  # Aika millisekunteina ammusten välillä
last_shot_time = pygame.time.get_ticks()  # Viimeisimmän ammuksen aika

# Viholliset
enemies = []
enemy_speed = 2
enemy_spawn_cooldown = 1000  # Aika millisekunteina vihollisten välillä
last_enemy_spawn_time = pygame.time.get_ticks()


def spawn_enemy():
    """Luo uuden vihollisen satunnaiseen paikkaan yläreunassa."""
    enemy_x = random.randint(0, WIDTH - 30)  # Vihollisen leveys on 30
    enemy_y = 0
    enemies.append([enemy_x, enemy_y])


def reset_game():
    """Aloittaa pelin uudelleen."""
    global player_points, bullets, enemies, last_shot_time, last_enemy_spawn_time, player_is_alive
    player_points = [(WIDTH // 2, HEIGHT - 80), (WIDTH // 2 - 25, HEIGHT - 50), (WIDTH // 2 + 25, HEIGHT - 50)]
    bullets = []
    enemies = []
    last_shot_time = pygame.time.get_ticks()
    last_enemy_spawn_time = pygame.time.get_ticks()
    player_is_alive = True


# Pelisilmukka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Näppäimistön syötteet (vain jos pelaaja on elossa)
    keys = pygame.key.get_pressed()
    if player_is_alive:
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

    # Vihollisten luominen
    if current_time - last_enemy_spawn_time > enemy_spawn_cooldown:
        spawn_enemy()
        last_enemy_spawn_time = current_time

    # Vihollisten liikkuminen
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:  # Poista viholliset, jotka menevät ruudun ulkopuolelle
            enemies.remove(enemy)

        # Osumisen tarkistus pelaajaan (vain jos pelaaja on elossa)
        if player_is_alive:
            player_x = player_points[0][0] - 25  # Pelaajan kolmion vasen reuna
            player_y = player_points[0][1]      # Pelaajan kolmion yläreuna
            if (
                enemy[0] < player_x + 50  # Pelaajan leveys (noin)
                and enemy[0] + 30 > player_x
                and enemy[1] < player_y + 30  # Pelaajan korkeus (noin)
                and enemy[1] + 30 > player_y
            ):
                player_is_alive = False
                reset_game()  # Aloitetaan peli uudelleen

    # Osumien tarkistus ammuksiin
    bullets_to_remove = []
    enemies_to_remove = []

    for bullet in bullets:
        for enemy in enemies:
            # Tarkistetaan, onko ammus osunut viholliseen
            if (
                bullet[0] > enemy[0]
                and bullet[0] < enemy[0] + 30  # Vihollisen leveys
                and bullet[1] > enemy[1]
                and bullet[1] < enemy[1] + 30  # Vihollisen korkeus
            ):
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(enemy)

    # Poistetaan osuneet ammukset ja viholliset
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)

    # Taustan piirto (SIIRRETTY YLÖS!)
    screen.fill(BLACK)

    # Ammusten liikkuminen ja piirto
    for bullet in bullets:
        bullet[1] -= bullet_speed  # Liikuta ammusta ylöspäin
        pygame.draw.circle(screen, BLUE, (bullet[0], bullet[1]), 5)  # Piirrä ammus sinisenä
        if bullet[1] < 0:  # Poista ammukset, jotka menevät ruudun ulkopuolelle
            bullets.remove(bullet)

    # Pelaajan aluksen piirto kolmiona (vain jos pelaaja on elossa)
    if player_is_alive:
        pygame.draw.polygon(screen, WHITE, player_points)

    # Vihollisten piirto
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 30, 30))  # Piirrä vihollinen punaisena neliönä

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()