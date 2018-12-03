"""MAIN CODEBASE."""

import pygame
import timeManager
from stateContr import StateController
from player import Player
import sys
import library
import random
import UI
import os
import soundEffects
import shutil
import playerLight
import math
from fuelMeter import *
from pygame.locals import *

import dungeonGenerator as dunGen
import MelodyGenerator as melGen
import colorBlindFilter
import CollisionDetection as colDetect
import aiAnimations

import mainMenu

# initialize pygame
pygame.init()
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

# create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# set the load bar font here so we know pygame has initialized
library.loading_bar_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 18)
debug_header_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 36)
debug_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 22)

menu = mainMenu.Menu()
# this is set just before main is called at the end of the script
menus = None

# set the window caption
pygame.display.set_caption("Well Escape")

# set the FPS
FPS = 60
# initialize the FPS clock
fps_clock = pygame.time.Clock()

fuel_meter = Torch()


aiAnimationPaths = aiAnimations.AiAnimation()

# Game and menu states
game_state = StateController()
menu_state = StateController()
time = timeManager.TimeManager(pygame.time.get_ticks() / 1000.0)
player_object = Player(75, (0.9, 0.9), time)

background_audio_paths = ["audio/bg_1.wav", "audio/bg_0.wav"]
bg_audio_interval = {"min": 3, "max": 6}
bg_audio_players = []

if not os.path.exists("Well Escape tiles/varieties"):
    os.makedirs("Well Escape tiles/varieties")
else:
    shutil.rmtree("Well Escape tiles/varieties")
    os.makedirs("Well Escape tiles/varieties")


def event_inputs():
    """Get the inputs and set the key presses."""
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            exit_game()
        # change the key pressed state
        elif event.type == KEYDOWN or event.type == KEYUP:

            # set left key pressed (A)
            if event.key == library.MOVE["left"]:
                library.KEY_PRESSED["left"] = event.type == KEYDOWN

                # set right key pressed (D)
            elif event.key == library.MOVE["right"]:
                library.KEY_PRESSED["right"] = event.type == KEYDOWN
                # set forwards key pressed (W)
            elif event.key == library.MOVE["forwards"]:
                library.KEY_PRESSED["forwards"] = event.type == KEYDOWN

                # set backwards key pressed (S)
            elif event.key == library.MOVE["backwards"]:
                library.KEY_PRESSED["backwards"] = event.type == KEYDOWN

            elif event.key == K_p:
                colorBlindFilter.color_blind_filter()
                colorBlindFilter.loop_image()
                print("taking color blind screenshot")
            elif event.key == K_y:
                sound_effects.apply_echo()
            elif event.key == K_h:
                sound_effects.play_echo_sound()
            elif event.key == K_SPACE:
                library.KEY_PRESSED["space"] = event.type == KEYDOWN

        if event.type == KEYUP:
            if event.key == K_F12:
                library.debug_mode = not library.debug_mode

            if library.debug_mode:
                if event.key == K_EQUALS:
                    dunGen.DungeonGenerator.levelCount += 1
                    dunGen.DungeonGenerator.current_dungeon += 1
                elif event.key == K_MINUS and \
                        dunGen.DungeonGenerator.levelCount > 3:
                    dunGen.DungeonGenerator.levelCount -= 1
                    dunGen.DungeonGenerator.current_dungeon -= 1

            if event.key == library.PAUSE:  # Pauses the game
                if game_state.get_state() == "game":
                    game_state.set_state("paused")
                elif game_state.get_state() == "paused":
                    game_state.set_state("game")
        # has a mouse button just been pressed?
        elif event.type == MOUSEBUTTONDOWN:
            library.KEY_PRESSED["mouse"] = True

        # has a mouse button just been released?
        elif event.type == MOUSEBUTTONUP:
            library.KEY_PRESSED["mouse"] = False


def exit_game():
    """Exit the game to desktop."""
    shutil.rmtree("Well Escape tiles/varieties")
    pygame.quit()
    sys.exit()


# creates a new level and positions everything accordingly in that level
def start():
    """Initialise the game."""
    # create movement variables
    screen_rect = screen.get_rect()
    level_rect = dunGen.DungeonGenerator.levels[0].get_rect()

    if dunGen.DungeonGenerator.well_room:
        # find a random floor tile and get it's position coordinates
        spawn_x = (math.ceil(len(dunGen.floorTilesX) * 0.5)
                   + random.randint(-2, 2)) * dunGen.TILE_SIZE
        spawn_y = (math.ceil(len(dunGen.floorTilesY) * 0.5)
                   + random.randint(-1, 1)) * dunGen.TILE_SIZE
        dunGen.DungeonGenerator.playerSpawnPoint = [spawn_x, spawn_y]
        dunGen.DungeonGenerator.well_room = False
    else:
        door_pos = dunGen.allTilePositions[dunGen.allTiles.index(2)]
        dunGen.DungeonGenerator.playerSpawnPoint = [door_pos[0], door_pos[1]
                                                    + (dunGen.TILE_SIZE * 0.5)]

    player_object.position[0] = dunGen.DungeonGenerator.playerSpawnPoint[0]
    player_object.position[1] = dunGen.DungeonGenerator.playerSpawnPoint[1]

    # variables for centering the level
    dunGen.DungeonGenerator.x = screen_rect.centerx - level_rect.centerx
    dunGen.DungeonGenerator.y = screen_rect.centery - level_rect.centery

    # variables for offsetting everything
    # so the starting tile is always at the center
    dunGen.DungeonGenerator.offsetX = -level_rect.centerx + \
        dunGen.DungeonGenerator.playerSpawnPoint[0]
    dunGen.DungeonGenerator.offsetY = -level_rect.centery + \
        dunGen.DungeonGenerator.playerSpawnPoint[1]
    library.RESET = False


# UI functions
def ui_controls():
    """Draw the controls image on screen."""
    screen.blit(pygame.transform.scale(pygame.image.load("UI/Controls.png"),
                                       (800, 600)), (200, 200))


def set_game_states(state):
    """Create the game states and set the default state."""
    state.add_state("main menu", "main menu")
    state.add_state("loading", "loading")
    state.add_state("game", "game")
    state.add_state("game over", "game over")
    state.add_state("paused", "paused")
    state.add_state("editor", "editor")

    # set the state to the default main menu
    state.set_state("main menu")


def set_menu_states(state):
    """Create the menu states and set the default state."""
    state.add_state("main menu", "main menu")
    state.add_state("options", "Options")
    state.add_state("paused", "paused")
    state.add_state("Controls", "Controls")

    # set the state to the default main menu
    state.set_state("main menu")


def menu_audio(is_playing, play):
    """Play or stop the menu audio."""

    if library.SOUND_HAS_INITIALIZED is None:
        return

    if play and not is_playing:
        pygame.mixer.music.play(-1)
        return True

    elif not play and is_playing:
        pygame.mixer.music.stop()
        return False

    return is_playing

def game_background_audio():
    """play in game background audio."""

    if library.SOUND_HAS_INITIALIZED is None:
        return

    random_bg_sound_id = random.randint(0, len(background_audio_paths)-1)
    audio = pygame.mixer.Sound(background_audio_paths[random_bg_sound_id])
    audio.set_volume(0.5)
    audio.play()

def stop_audio():
    """Stop all audio.

    :return:    0 so it can reset any timers
    """

    if library.SOUND_HAS_INITIALIZED is None:
        return

    pygame.mixer.stop()

    return 0


def draw_dungeon():
    """Draw the dungeon on screen."""
    # Todo this can be optimized so it only draws the rooms we can see.
    for i in range(len(dunGen.DungeonGenerator.levels) - 1, -1, -1):
        screen.blit(dunGen.DungeonGenerator.levels[i],
                    (dunGen.DungeonGenerator.x +
                     dunGen.DungeonGenerator.starting_point_x[i] -
                     dunGen.DungeonGenerator.offsetX,
                     dunGen.DungeonGenerator.y +
                     dunGen.DungeonGenerator.starting_point_y[i] -
                     dunGen.DungeonGenerator.offsetY))


def debug():
    """Switch the game to debug mode."""
    if library.debug_mode:
        # display some stats to screen
        debug_header_surface = debug_header_font_face.render(
            "DEBUG MODE",
            True,
            library.WHITE
        )
        debug_room_count_surface = debug_font_face.render(
            "Level Room count: " + str(dunGen.DungeonGenerator.levelCount),
            True,
            library.WHITE
        )

        for room in range(len(dunGen.DungeonGenerator.starting_point_x)):
            room_numb = room + 1
            room_numb_surface = debug_font_face.render(
                str(room_numb),
                True,
                library.WHITE
            )
            display_position = dunGen.DungeonGenerator.\
                get_position_with_offset(
                    dunGen.DungeonGenerator.starting_point_x[room] +
                    (dunGen.TILE_SIZE // 2),
                    dunGen.DungeonGenerator.starting_point_y[room] +
                    (dunGen.TILE_SIZE // 2))
            screen.blit(room_numb_surface, display_position)

        screen.blit(debug_header_surface, (0, 0))
        screen.blit(debug_room_count_surface, (0, 33))


def main():
    """Main game loop."""
    player_object.get_world_position_funct = \
        dunGen.DungeonGenerator.get_position_with_offset
    dunGen.DungeonGenerator.create_dungeon(dunGen.DungeonGenerator)
    # players current direction
    current_direction = library.BACKWARDS

    # setup the states for both game and menus
    set_game_states(game_state)
    set_menu_states(menu_state)

    dunGen.DungeonGenerator.player = player_object

    # prevent the menu audio generating if the audio has not initialized
    if library.SOUND_HAS_INITIALIZED is not None:
        print("Audio has not been initialized")
        melGen.MusicGenerator.generate_track(melGen.MusicGenerator)
        pygame.mixer.music.load(str(melGen.MusicGenerator.filename
                                    + str(melGen.MusicGenerator.current_track)
                                    + melGen.MusicGenerator.filetype))

    menu_audio_is_playing = False

    next_background_audio_time = 0

    # main game loop
    while True:

        time.update_time(pygame.time.get_ticks()/1000.0)

        # amount of time that passed since the last frame in seconds
        delta_time = time.delta_time
        movement_speed = 75 * delta_time

        event_inputs()

        # fill the background
        screen.fill(library.BLACK)

        # NEW MAIN CODE
        if game_state.get_state() == "main menu"\
                or game_state.get_state() == "game over"\
                or game_state.get_state() == "paused":
            screen.blit(library.background, (0, 0))

        if game_state.get_state() == "loading":  # treat this as RESET.

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)
        elif game_state.get_state() == "game":
            # Audio
            sound_effects.play_footprint()
            menu_audio_is_playing = menu_audio(menu_audio_is_playing, False)

            # Dungeon
            colDetect.CollisionDetector.detect_collision(
                colDetect.CollisionDetector
            )

            dunGen.DungeonGenerator. update_dungeon(
                dunGen.DungeonGenerator,
                "forwards",
                "backwards",
                movement_speed,
                -10,
                "right",
                "left"
            )
            dunGen.DungeonGenerator. update_dungeon(
                dunGen.DungeonGenerator,
                "backwards",
                "forwards",
                -movement_speed,
                10,
                "right",
                "left"
            )
            dunGen.DungeonGenerator. update_dungeon(
                dunGen.DungeonGenerator,
                "left",
                "right",
                movement_speed,
                -20,
                "forwards",
                "backwards"
            )
            dunGen.DungeonGenerator. update_dungeon(
                dunGen.DungeonGenerator,
                "right",
                "left",
                -movement_speed,
                15,
                "forwards",
                "backwards"
            )

            draw_dungeon()
            dunGen.DungeonGenerator.draw_chest(dunGen.DungeonGenerator)

            # Ghost Animation
            aiAnimationPaths.update_animations(delta_time, screen)

            # Player
            player_object.block_move_direction(
                dunGen.DungeonGenerator.top_col,
                dunGen.DungeonGenerator.right_col,
                dunGen.DungeonGenerator.bottom_col,
                dunGen.DungeonGenerator.left_col
            )
            player_object.update(library.KEY_PRESSED)
            player_object.draw(dunGen.TILE_SIZE, screen)

            player_x_pos, player_y_pos = dunGen.DungeonGenerator.\
                get_position_with_offset(player_object.position[0],
                                         player_object.position[1])

            if not library.debug_mode and aiAnimationPaths.ghost_in_position(
                    player_x_pos,
                    player_y_pos,
                    screen
            ):
                game_state.set_state("game over")

            # Light
            playerLight.update_light(fuel_meter.get_fuel_percentage())
            playerLight.initialise_lightning(dunGen.TILE_SIZE)
            playerLight.draw_light(screen, dunGen)
            playerLight.overlay(screen)

            # Audio
            if next_background_audio_time is None or next_background_audio_time <= 0:
                game_background_audio()
                next_background_audio_time = random.uniform(
                    float(bg_audio_interval["min"]),
                    float(bg_audio_interval["max"])
                )

            next_background_audio_time -= delta_time

            # Fuel Meta (UI)
            if not library.debug_mode:
                fuel_meter.update_fuel_timer(delta_time)

            fuel_meter.display_fuel_meter(screen, (630, 50))

            if dunGen.DungeonGenerator.reset_fuel:
                fuel_meter.reset_fuel()
                dunGen.DungeonGenerator.reset_fuel = False
            elif dunGen.DungeonGenerator.add_fuel:
                fuel_meter.add_fuel()
                dunGen.DungeonGenerator.add_fuel = False
            elif fuel_meter.torch_time == 0:
                game_state.set_state("game over")

        elif game_state.get_state() == "game over":

            menus.draw_buttons(
                screen, pygame.mouse.get_pos(),
                library.KEY_PRESSED["mouse"], "Game Over", "Game Over")
            menus.is_button_pressed(
                pygame.mouse.get_pos(),
                library.KEY_PRESSED["mouse"], "Game Over")

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)

        elif game_state.get_state() == "main menu":

            if not menu_audio_is_playing:
                next_background_audio_time = stop_audio()

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)

            if menu_state.get_state() == "Controls":
                ui_controls()
                menus.draw_buttons(
                    screen,
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Controls", "Controls"
                )
                menus.is_button_pressed(
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Controls"
                )
            else:
                # New ui code!
                menus.draw_buttons(
                    screen,
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Well Escape", "main menu"
                )
                menus.is_button_pressed(
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "main menu"
                )

        elif game_state.get_state() == "paused":

            if not menu_audio_is_playing:
                next_background_audio_time = stop_audio()

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)

            if menu_state.get_state() == "Controls":
                ui_controls()
                menus.draw_buttons(
                    screen,
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Controls", "Controls"
                )
                menus.is_button_pressed(
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Controls"
                )
            else:
                menus.draw_buttons(
                    screen,
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "Paused", "paused"
                )
                menus.is_button_pressed(
                    pygame.mouse.get_pos(),
                    library.KEY_PRESSED["mouse"], "paused"
                )
        elif game_state.get_state() == "editor":
            Editor.display()

        debug()

        # update the display.
        fps_clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":
    import tileEditor as Editor
    # set games state in the tile editor so we can return.
    Editor.EditorStore.game_state = game_state

    # set shared functions with the menu system
    menu.set_functions_by_name("exit", exit_game)
    menu.set_functions_by_name("menu_state", menu_state)
    menu.set_functions_by_name("game state", game_state)

    menus = menu.initialize_menu()
    colorBlindFilter.initialization()

    library.SOUND_HAS_INITIALIZED = pygame.mixer.get_init()
    sound_effects = soundEffects.SoundFX()

    main()
