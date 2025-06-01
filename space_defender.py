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
YELLOW = (255, 255, 0)  # Lisätty keltainen väri varoitusviivalle

# Fontit
font = pygame.font.Font(None, 36)  # Oletusfontti, koko 36
small_font = pygame.font.Font(None, 24)  # Pienempi fontti ohjeille

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
enemy_spawn_cooldown = 1500  # Aika millisekunteina vihollisten välillä (Alkuperäinen arvo)
last_enemy_spawn_time = pygame.time.get_ticks()
enemy_reach_bottom = False  # Onko vihollinen päässyt alareunaan

# Pelin vaikeustaso
game_difficulty = 1  # Aloitetaan helpolla (1)
difficulty_increase_time = 10000  # Aika millisekunteina, jonka jälkeen vaikeus kasvaa (esim. 10 sekuntia)
last_difficulty_increase = pygame.time.get_ticks()

# Peliaika
start_time = 0  # Aika millisekunteina, jolloin peli alkoi
elapsed_time = 0  # Kulunut aika

# Pelitila
game_state = "menu"  # "menu", "playing", "gameover"
warning_line_y = HEIGHT - 30  # Y-koordinaatti varoitusviivalle


def spawn_enemy():
    """Luo uuden vihollisen satunnaiseen paikkaan yläreunassa."""
    enemy_x = random.randint(0, WIDTH - 30)  # Vihollisen leveys on 30
    enemy_y = 0
    enemies.append([enemy_x, enemy_y])


def reset_game():
    """Aloittaa pelin uudelleen."""
    global player_points, bullets, enemies, last_shot_time, last_enemy_spawn_time, player_is_alive, enemy_reach_bottom, game_difficulty, last_difficulty_increase, start_time, elapsed_time
    player_points = [(WIDTH // 2, HEIGHT - 80), (WIDTH // 2 - 25, HEIGHT - 50), (WIDTH // 2 + 25, HEIGHT - 50)]
    bullets = []
    enemies = []
    last_shot_time = pygame.time.get_ticks()
    last_enemy_spawn_time = pygame.time.get_ticks()
    player_is_alive = True
    enemy_reach_bottom = False
    game_difficulty = 1  # Palautetaan vaikeustaso alkuperäiseen
    last_difficulty_increase = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()  # Nollataan pelin aloitusaika
    elapsed_time = 0  # Nollataan kulunut aika


def increase_difficulty():
    """Lisää pelin vaikeustasoa."""
    global enemy_speed, enemy_spawn_cooldown, game_difficulty
    game_difficulty += 0.5  # Lisätään vaikeustasoa
    enemy_speed += 0.2  # Lisätään vihollisten nopeutta
    enemy_spawn_cooldown = max(
        500, enemy_spawn_cooldown - 50
    )  # Vähennetään spawn cooldownia (max 0.5 sekuntia)
    print(f"Vaikeustaso: {game_difficulty}, Vihollisen nopeus: {enemy_speed}, Spawn cooldown: {enemy_spawn_cooldown}")


def show_menu():
    """Näyttää aloitusmenun."""
    screen.fill(BLACK)
    title_text = font.render("Space Defender", True, WHITE)
    start_text = font.render("Paina SPACE aloittaaksesi", True, WHITE)
    controls_text = small_font.render(
        "Liiku: Nuolinäppäimet, Ammu: SPACE", True, WHITE
    )  # Ohjeteksti
    objective_text = small_font.render(
        "Estä vihollisia pääsemästä alareunaan!", True, YELLOW
    )  # Uusi ohjeteksti
    difficulty_text = small_font.render(
        "Vaikeus kasvaa ajan myötä!", True, YELLOW
    )  # Uusi ohjeteksti
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))  # Ohjeiden paikka
    objective_rect = objective_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 100)
    )  # Uuden ohjeen paikka
    difficulty_rect = difficulty_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 150)
    )  # Uuden ohjeen paikka
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(controls_text, controls_rect)  # Piirrä ohjeet
    screen.blit(objective_text, objective_rect)  # Piirrä uusi ohje
    screen.blit(difficulty_text, difficulty_rect)  # Piirrä uusi ohje
    pygame.display.flip()


def show_gameover(elapsed_time):
    """Näyttää Game Over -ruudun ja selviytymisajan."""
    screen.fill(BLACK)
    gameover_text = font.render("Game Over", True, RED)
    time_text = font.render(
        f"Selviydyit: {elapsed_time // 1000} sekuntia", True, WHITE
    )  # Näytetään aika sekunteina
    restart_text = font.render("Paina SPACE aloittaaksesi uudelleen", True, WHITE)
    gameover_rect = gameover_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    screen.blit(gameover_text, gameover_rect)
    screen.blit(time_text, time_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()


# Pelisilmukka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "menu" and event.key == pygame.K_SPACE:
                game_state = "playing"
                reset_game()  # Aloita peli kun painetaan spacea
            if game_state == "gameover" and event.key == pygame.K_SPACE:
                game_state = "playing"
                reset_game()

    if game_state == "menu":
        show_menu()
    elif game_state == "playing":
        # Laske kulunut aika
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Näppäimistön syötteet (vain jos pelaaja on elossa)
        keys = pygame.key.get_pressed()
        if player_is_alive:
            # Ampuminen
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
            if enemy[1] > HEIGHT:  # Onko vihollinen päässyt alareunaan?
                enemy_reach_bottom = True
                player_is_alive = False  # Pelaaja menettää
                game_state = "gameover"  # Siirry Game Over -tilaan
                # ÄLÄ KÄYTÄ BREAK TÄSSÄ!
            # Osumisen tarkistus pelaajaan (vain jos pelaaja on elossa)
            if player_is_alive:
                player_x = player_points[0][0] - 25  # Pelaajan kolmion vasen reuna
                player_y = player_points[0][1]  # Pelaajan kolmion yläreuna
                if (
                    enemy[0] < player_x + 50  # Pelaajan leveys (noin)
                    and enemy[0] + 30 > player_x
                    and enemy[1] < player_y + 30  # Pelaajan korkeus (noin)
                    and enemy[1] + 30 > player_y
                ):
                    player_is_alive = False
                    game_state = "gameover"  # Siirry Game Over -tilaan
                    # ÄLÄ KÄYTÄ BREAK TÄSSÄ!

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

        # Varoitusviivan piirto
        pygame.draw.line(screen, YELLOW, (0, warning_line_y), (WIDTH, warning_line_y), 2)

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

        # Vaikeustason nosto
        if current_time - last_difficulty_increase > difficulty_increase_time:
            increase_difficulty()
            last_difficulty_increase = current_time

    elif game_state == "gameover":
        show_gameover(elapsed_time)  # Näytetään Game Over -ruutu ja selviytymisaika

pygame.quit()