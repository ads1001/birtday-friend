import pygame
import random
import sys

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎂 Reto de Cumpleaños 🎂")

# Colores y paleta
DARK_BG = (20, 24, 33)      # Fondo nocturno de lluvia
RAIN_COLOR = (100, 180, 255) 
WALL_BROWN = (139, 69, 19)   # Muros de tierra
GRASS_TOP = (50, 205, 50)    # Pasto superior
PINK_BG = (255, 240, 245)    # Fondo rosa tierno para la victoria
PASTEL_PINK = (255, 182, 193)
TEXT_COLOR = (110, 70, 90)
YELLOW = (255, 223, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Laberinto más grande y desafiante (1 = Muro, 0 = Camino, 2 = Meta)
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

rows = len(laberinto)
cols = len(laberinto[0])
tile_width = WIDTH // cols
tile_height = 420 // rows 

# Jugador
player_size = 16
start_x = tile_width * 1 + tile_width // 4
start_y = tile_height * 1 + tile_height // 4
player_x, player_y = start_x, start_y
speed = 3

# Enemigos móviles [x, y, direccion_x, direccion_y, min_lim, max_lim, tipo_movimiento]
# tipo: 'H' (horizontal) o 'V' (vertical)
enemigos = [
    [tile_width * 5, tile_height * 3, 2, 0, tile_width * 5, tile_width * 9, 'H'],
    [tile_width * 11, tile_height * 5, 0, 2, tile_height * 3, tile_height * 7, 'V'],
    [tile_width * 3, tile_height * 7, 2, 0, tile_width * 1, tile_width * 5, 'H'],
    [tile_width * 16, tile_height * 2, 0, 2, tile_height * 1, tile_height * 5, 'V']
]

drops = [[random.randint(0, WIDTH), random.randint(0, 500)] for _ in range(120)]

font = pygame.font.SysFont("Arial", 16, bold=True)
big_font = pygame.font.SysFont("Arial", 24, bold=True)
clock = pygame.time.Clock()
victoria = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not victoria:
        # Movimiento del jugador
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = speed

        # Colisiones eje X
        player_x += dx
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for r_idx, row in enumerate(laberinto):
            for c_idx, val in enumerate(row):
                if val == 1:
                    wall_rect = pygame.Rect(c_idx * tile_width, r_idx * tile_height, tile_width, tile_height)
                    if player_rect.colliderect(wall_rect):
                        if dx > 0: player_x = wall_rect.left - player_size
                        if dx < 0: player_x = wall_rect.right

        # Colisiones eje Y
        player_y += dy
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for r_idx, row in enumerate(laberinto):
            for c_idx, val in enumerate(row):
                if val == 1:
                    wall_rect = pygame.Rect(c_idx * tile_width, r_idx * tile_height, tile_width, tile_height)
                    if player_rect.colliderect(wall_rect):
                        if dy > 0: player_y = wall_rect.top - player_size
                        if dy < 0: player_y = wall_rect.bottom

        # Mover enemigos y verificar colisión con el jugador (si choca, regresa al inicio)
        for e in enemigos:
            if e[6] == 'H':
                e[0] += e[2]
                if e[0] <= e[4] or e[0] >= e[5]:
                    e[2] *= -1
            else:
                e[1] += e[3]
                if e[1] <= e[4] or e[1] >= e[5]:
                    e[3] *= -1
            
            enemy_rect = pygame.Rect(e[0], e[1], 18, 18)
            if player_rect.colliderect(enemy_rect):
                player_x, player_y = start_x, start_y  # Reinicia al tocar enemigo

        # Verificar si llega a la meta (2)
        for r_idx, row in enumerate(laberinto):
            for c_idx, val in enumerate(row):
                if val == 2:
                    goal_rect = pygame.Rect(c_idx * tile_width + 4, r_idx * tile_height + 4, tile_width - 8, tile_height - 8)
                    if player_rect.colliderect(goal_rect):
                        victoria = True

    # --- RENDERIZADO ---
    if not victoria:
        screen.fill(DARK_BG)

        # Lluvia
        for drop in drops:
            drop[1] += 6
            if drop[1] > 450:
                drop[1] = 0
                drop[0] = random.randint(0, WIDTH)
            pygame.draw.line(screen, RAIN_COLOR, (drop[0], drop[1]), (drop[0], drop[1] + 10), 2)

        # Laberinto
        for r_idx, row in enumerate(laberinto):
            for c_idx, val in enumerate(row):
                wx = c_idx * tile_width
                wy = r_idx * tile_height
                if val == 1:
                    pygame.draw.rect(screen, WALL_BROWN, (wx, wy, tile_width, tile_height))
                    pygame.draw.rect(screen, GRASS_TOP, (wx, wy, tile_width, 6))
                elif val == 2:
                    pygame.draw.circle(screen, PINK_BG, (wx + tile_width//2, wy + tile_height//2), 8)
                    pygame.draw.circle(screen, YELLOW, (wx + tile_width//2, wy + tile_height//2), 3)

        # Dibujar enemigos (rojos con picos simulados)
        for e in enemigos:
            pygame.draw.rect(screen, (220, 20, 60), (e[0], e[1], 18, 18), border_radius=3)

        # Jugador
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size), border_radius=4)

        # Instrucción
        txt_ins = font.render("Esquiva los bloques rojos móviles, cruza el laberinto y llega a la flor.", True, WHITE)
        screen.blit(txt_ins, (20, HEIGHT - 40))

    else:
        # Pantalla de Victoria estética estilo tarjeta rosa pastel
        screen.fill(PINK_BG)

        # Dibujar Guirnalda de corazones superior
        for h in range(0, WIDTH, 40):
            pygame.draw.circle(screen, PASTEL_PINK, (h + 20, 30), 10)
            pygame.draw.circle(screen, PASTEL_PINK, (h + 30, 30), 10)
            pygame.draw.polygon(screen, PASTEL_PINK, [(h + 10, 33), (h + 40, 33), (h + 25, 48)])

        # Dibujar pastel de cumpleaños central (estilo dibujo de la imagen)
        cake_x, cake_y = WIDTH // 2 - 110, 90
        # Plato
        pygame.draw.ellipse(screen, (200, 180, 190), (cake_x - 20, cake_y + 110, 300, 25))
        # Base del pastel (rosa)
        pygame.draw.rect(screen, PASTEL_PINK, (cake_x, cake_y + 40, 260, 75), border_radius=15)
        # Capa superior del pastel
        pygame.draw.rect(screen, (255, 192, 203), (cake_x + 20, cake_y + 10, 220, 50), border_radius=12)
        # Vela
        pygame.draw.rect(screen, WHITE, (cake_x + 120, cake_y - 20, 16, 35))
        # Fuego de la vela
        pygame.draw.ellipse(screen, YELLOW, (cake_x + 120, cake_y - 38, 16, 22))

        # Textos emotivos centrados
        t1 = big_font.render("¡FELIZ CUMPLEAÑOS!", True, TEXT_COLOR)
        t2 = font.render("¡Te deseo lo mejor en tu día!", True, TEXT_COLOR)
        t3 = font.render("Gracias por todos los momentos, las risas y las historias que compartimos.", True, TEXT_COLOR)
        t4 = font.render("De parte de todo el grupo: ¡Feliz cumpleaños!", True, TEXT_COLOR)

        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 235))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 275))
        screen.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 330))
        screen.blit(t4, (WIDTH // 2 - t4.get_width() // 2, 370))

    pygame.display.flip()
    clock.tick(60)
