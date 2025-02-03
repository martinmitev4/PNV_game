import pygame
import itertools
from pygame.locals import *

from gameLogic import Game, Direction

FPS = 30
WINWIDTH = 900 # width of the program's window, in pixels
WINHEIGHT = 700 # height in pixels

TILEWIDTH = 40
TILEHEIGHT = 40

BGCOLOR = (  225, 225, 255)

def main():
    global WINWIDTH, WINHEIGHT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    curren_level = 1
    game = Game(level=curren_level)

    while True:
        board = game.board
        player_position = game.player_pos

        if game.state == 'won':
            if curren_level == 5:
                curren_level = 1
            else:
                curren_level += 1
            game = Game(level=curren_level)
        elif game.state == 'lost':
            game_over_screen(DISPLAYSURF)
            game = Game(level=curren_level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                moveTo = ""
                if event.key == K_LEFT or event.key == K_a:
                    moveTo = Direction.LEFT
                elif event.key == K_RIGHT or event.key == K_d:
                    moveTo = Direction.RIGHT
                elif event.key == K_UP or event.key == K_w:
                    moveTo = Direction.UP
                elif event.key == K_DOWN or event.key == K_s:
                    moveTo = Direction.DOWN
                if moveTo != "":
                    game.move(moveTo)

                if event.key == K_u:
                    game.undo()
                    board = game.board

        mapSurf = draw_map(board, player_position)
        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (int(WINWIDTH/2), int(WINHEIGHT/2 + 50))

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        pygame.display.update()  # Refresh the screen
        FPSCLOCK.tick()

def adjust_brightness(image, brightness=1.0):
    """Modify brightness where 1.0 is normal, <1.0 is darker, >1.0 is brighter"""
    bright_image = image.copy()
    brightness_value = int(255 * brightness)

    # Ensure the value is clamped between 0 and 255
    brightness_value = max(0, min(255, brightness_value))

    # Apply brightness filter using an (R, G, B, A) tuple
    bright_image.fill((brightness_value, brightness_value, brightness_value, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return bright_image


# Function to overlay images
def overlay_images(background, overlay):
    combined = background.copy()
    combined.blit(overlay, (0, 0))
    return combined


# Function to add border
def add_border(image, color=(99, 95, 95), border_size=1):
    bordered = pygame.Surface((image.get_width() + border_size * 2, image.get_height() + border_size * 2),
                              pygame.SRCALPHA)
    bordered.fill(color)
    bordered.blit(image, (border_size, border_size))
    return bordered


def draw_map(mapObj, player_position):
    """Draws the map to a Surface object, including the player and lava."""

    mapSurfWidth = len(mapObj[0]) * TILEWIDTH
    mapSurfHeight = len(mapObj) * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight), pygame.SRCALPHA)  # Allow transparency
    mapSurf.fill(BGCOLOR)

    # Load and modify images
    tile_images = {
        '#': adjust_brightness(pygame.transform.scale(
            pygame.image.load('images/tile.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ), 1.0),
        '.': adjust_brightness(pygame.transform.scale(
            pygame.image.load('images/floor.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ), 1.45),
        'G': add_border(overlay_images(
            pygame.transform.scale(
                pygame.image.load('images/tile.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
            ), pygame.transform.scale(
                pygame.image.load('images/p2.gif').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
            )
        )),
        'L': pygame.transform.scale(
            pygame.image.load('images/lava48.gif').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ),
        'W': pygame.transform.scale(
            pygame.image.load('images/WaterTileOcean.gif').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ),
        'B': pygame.transform.scale(
            pygame.image.load('images/box.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ),
    }

    player_frames = [
        pygame.transform.scale(
            pygame.image.load(f'images/duck.gif').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        )
    ]
    player_animation = itertools.cycle(player_frames)  # Placeholder for multiple frames

    for y in range(len(mapObj)):
        for x in range(len(mapObj[y])):
            tile_type = mapObj[y][x]
            pos = (x * TILEWIDTH, y * TILEHEIGHT)

            # Blit the correct tile image
            if tile_type in tile_images:
                mapSurf.blit(tile_images[tile_type], pos)

    # Draw player with animation
    player_x, player_y = player_position
    pos = (player_y * TILEWIDTH, player_x * TILEHEIGHT)
    mapSurf.blit(next(player_animation), pos)

    return mapSurf


def game_over_screen(screen):
    """Displays a Game Over screen with options to retry or quit."""
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Press ENTER to Retry", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    screen.fill((0, 0, 0))  # Black background
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
    screen.blit(retry_text, (screen.get_width() // 2 - retry_text.get_width() // 2, 250))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 300))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart game
                    return True
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    exit()

if __name__ == '__main__':
    main()