import pygame
from pygame.locals import *

from gameLogic import Game, Direction

FPS = 30
WINWIDTH = 900
WINHEIGHT = 700

TILEWIDTH = 50
TILEHEIGHT = 50

BGCOLOR = (0, 25, 10)


def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    current_level = 1
    game = Game(level=current_level)

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        board = game.board
        player_position = game.player_pos
        new_game_button, undo_button = draw_buttons(DISPLAYSURF)

        if game.state == 'won':
            if current_level == 5:
                you_win_screen(DISPLAYSURF)
                current_level = 1
            else:
                current_level += 1
            game = Game(level=current_level)
        elif game.state == 'lost':
            game_over_screen(DISPLAYSURF)
            game = Game(level=current_level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    game.move(Direction.LEFT)
                elif event.key == K_RIGHT or event.key == K_d:
                    game.move(Direction.RIGHT)
                elif event.key == K_UP or event.key == K_w:
                    game.move(Direction.UP)
                elif event.key == K_DOWN or event.key == K_s:
                    game.move(Direction.DOWN)

                if event.key == K_u:
                    game.undo()

            elif event.type == MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    game = Game(level=current_level)

                elif undo_button.collidepoint(event.pos):
                    game.undo()

        mapSurf = draw_map(board, player_position)
        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (int(WINWIDTH/2), int(WINHEIGHT/2 + 50))

        new_game_text = font.render("Level: " + str(current_level), True, (255, 255, 255))
        DISPLAYSURF.blit(new_game_text, (50, 90))

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        pygame.display.update()
        FPSCLOCK.tick()


def overlay_images(background, overlay):
    combined = background.copy()
    combined.blit(overlay, (0, 0))
    return combined


def add_border(image, color=(99, 95, 95), border_size=1):
    bordered = pygame.Surface((image.get_width() + border_size * 2, image.get_height() + border_size * 2),
                              pygame.SRCALPHA)
    bordered.fill(color)
    bordered.blit(image, (border_size, border_size))
    return bordered


def draw_buttons(screen):
    font = pygame.font.Font(None, 24)
    button_color = (100, 6, 210)
    text_color = (255, 255, 255)

    # New Game Button
    new_game_rect = pygame.Rect(WINWIDTH - 250, 70, 90, 40)
    pygame.draw.rect(screen, button_color, new_game_rect)
    new_game_text = font.render("New Game", True, text_color)
    screen.blit(new_game_text, (new_game_rect.centerx - (new_game_text.get_width() // 2),
                                new_game_rect.centery - (new_game_text.get_height() // 2)))

    # Undo Button
    undo_rect = pygame.Rect(WINWIDTH - 150, 70, 90, 40)
    pygame.draw.rect(screen, button_color, undo_rect)
    undo_text = font.render("Undo", True, text_color)
    screen.blit(undo_text, (undo_rect.centerx - (undo_text.get_width() // 2),
                            undo_rect.centery - (undo_text.get_height() // 2)))

    return new_game_rect, undo_rect


def draw_map(mapObj, player_position):
    font = pygame.font.Font(None, 36)
    mapSurfWidth = len(mapObj[0]) * TILEWIDTH
    mapSurfHeight = len(mapObj) * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight), pygame.SRCALPHA)  # Allow transparency
    mapSurf.fill(BGCOLOR)

    tile_images = {
        '#': pygame.transform.scale(
            pygame.image.load('images/tile.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ),
        '.': pygame.transform.scale(
            pygame.image.load('images/floor.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        ),
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

    number_tile = pygame.transform.scale(
        pygame.image.load('images/tile.png').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
    )

    player = pygame.transform.scale(
            pygame.image.load(f'images/duck.gif').convert_alpha(), (TILEWIDTH, TILEHEIGHT)
        )

    for y in range(len(mapObj)):
        for x in range(len(mapObj[y])):
            tile_type = mapObj[y][x]
            pos = (x * TILEWIDTH, y * TILEHEIGHT)

            if tile_type in tile_images:
                mapSurf.blit(tile_images[tile_type], pos)
            elif tile_type.isnumeric():
                mapSurf.blit(number_tile, pos)

                green_overlay = pygame.Surface((TILEWIDTH, TILEHEIGHT), pygame.SRCALPHA)
                green_overlay.fill((0, 255, 8, int(255 * 0.15)))
                mapSurf.blit(green_overlay, pos)

                number_text = font.render(tile_type, True, (255, 255, 255))
                text_rect = number_text.get_rect(center=(pos[0] + TILEWIDTH // 2, pos[1] + TILEHEIGHT // 2))
                mapSurf.blit(number_text, text_rect)

    player_x, player_y = player_position
    pos = (player_y * TILEWIDTH, player_x * TILEHEIGHT)
    mapSurf.blit(player, pos)

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


def you_win_screen(screen):
    font = pygame.font.Font(None, 50)
    win_text = font.render("YOU WIN!", True, (255, 215, 0))  # Gold color

    screen.fill((0, 0, 0))  # Black background
    screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, 300))
    pygame.display.flip()

    pygame.time.delay(2000)


if __name__ == '__main__':
    main()