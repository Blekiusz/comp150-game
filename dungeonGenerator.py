"""Driver - Joachim / Navigator - None"""
import pygame
import random
import tileGenerator
from random import choices

tile_class = tileGenerator.Tiles()

tiles = []
tileTypes = []
tileMats = []
floorTiles = []
wallTiles = []
doorTiles = []

allTilePositions = []
allTiles = []

TILE_SIZE = tile_class.floorImg.get_rect().width
materials = tile_class.tileTypes


class GameStore:
    """A variable storage class."""

    playerX = 0
    playerY = 0
    previousPlayerX = 0
    previousPlayerY = 0
    previousX = 0
    previousY = 0
    offsetX = 0
    offsetY = 0
    x = 0
    y = 0
    playerSpawnPoint = []
    mud_variations = 15
    moss_variations = 15
    pixel_map = pygame.Surface
    MAP_WIDTH = 0
    MAP_HEIGHT = 0
    top_col = False
    bottom_col = False
    left_col = False
    right_col = False
    collisions = [top_col, bottom_col, left_col, right_col]
    start_x = 0
    start_y = 0
    levelCount = 2
    levels = []
    starting_point_x = []
    starting_point_y = []
    current_tile = 0
    last_tile = 0
    current_tiles = []
    prediction_X = 0
    prediction_Y = 0
    secondary_prediction_X = 0
    secondary_prediction_Y = 0
    set_position = True


for num in range(GameStore.levelCount):
    GameStore.levels.append(pygame.Surface)
    GameStore.starting_point_x.append(0)
    GameStore.starting_point_y.append(0)


def create_dungeon():
    """Generate the dungeon."""
    for i in range(len(GameStore.levels)):
        if i > 0:
            # set the starting point for the next room
            GameStore.starting_point_x[i] = \
                GameStore.starting_point_x[i-1] + \
                GameStore.start_x * TILE_SIZE - TILE_SIZE

            GameStore.starting_point_y[i] = \
                GameStore.starting_point_y[i-1] + \
                GameStore.start_y * TILE_SIZE

        # create the room
        initialize_level(i)


def gen_rand_map_tiles(instance):
    """
    Generate the random map tiles with different probabilities.

    :return: tile type ID [x][y]
    """
    # choose a random pixel map and generate a surface for the tiles
    if instance == 0:
        GameStore.pixel_map = get_dungeon_room(True)
    else:
        GameStore.pixel_map = get_dungeon_room(False)
    GameStore.MAP_WIDTH = GameStore.pixel_map.get_width()
    GameStore.MAP_HEIGHT = GameStore.pixel_map.get_height()

    # reset all lists
    tiles.clear()
    tileTypes.clear()
    tileMats.clear()

    # set variables for random material variation
    material_types = [0, 1, 2]
    material_weights = [0.9, 0.6, 0.3]

    # choose random types of the floor and wall images
    floor = random.randrange(len(tile_class.tileTypes[0]))
    wall = random.randrange(len(tile_class.tileTypes[1]))

    '''
    Scroll through each pixel in a map and assign according tiles depending
     on the pixel brightness.

    Assign a randomly chosen material type value to each tile.
    '''
    for y in range(GameStore.MAP_HEIGHT):
        tile_row = []
        type_row = []
        mat_row = []
        for x in range(GameStore.MAP_WIDTH):
            pixel = GameStore.pixel_map.get_at((x, y))
            pixel_tone = (pixel.r + pixel.g + pixel.b) / 3  # pixel brightness
            if pixel_tone == 255:
                tile = 0
                t_type = floor
            elif pixel_tone == 0:
                tile = 1
                t_type = wall
            elif pixel_tone < 150:
                if instance == 0:
                    tile = 2
                    t_type = 0
                else:
                    tile = 0
                    t_type = floor
            else:
                if instance == len(GameStore.levels) - 1:
                    tile = 2
                    t_type = 1
                else:
                    tile = 0
                    t_type = floor
                GameStore.start_x = x
                GameStore.start_y = y
            tile_row.append(tile)  # horizontal row of tiles
            type_row.append(t_type)  # horizontal row of tile types

            # single material
            material = choices(material_types, material_weights)[0]
            mat_row.append(material)  # horizontal row of materials

        tiles.append(tile_row)  # vertical column of horizontal tile rows
        tileTypes.append(type_row)  # vertical column of horizontal type rows
        tileMats.append(mat_row)  # vertical column of horizontal material rows
    return tiles


def initialize_level(surface_id):
    """Draw the tiles with according images on a blank surface."""
    # generate the map
    gen_rand_map_tiles(surface_id)
    GameStore.levels[surface_id] = pygame.Surface(
        (GameStore.MAP_WIDTH * TILE_SIZE,
         GameStore.MAP_HEIGHT * TILE_SIZE))

    # generate material variations
    while GameStore.mud_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 1, GameStore.mud_variations)
        GameStore.mud_variations -= 1

    while GameStore.moss_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 2, GameStore.moss_variations)
        GameStore.moss_variations -= 1

    # draw the tiles to the level surface
    for column in range(GameStore.MAP_HEIGHT):
        for row in range(GameStore.MAP_WIDTH):
            x_pos = row * TILE_SIZE
            y_pos = column * TILE_SIZE

            material = pygame.Surface
            if tiles[column][row] == 0:
                if surface_id == 0:
                    floorTiles.append([x_pos +
                                       GameStore.starting_point_x[surface_id],
                                       y_pos +
                                       GameStore.starting_point_y[surface_id]])

                material = assign_material(tile_class, tiles[column][row],
                                           tileTypes[column][row],
                                           tileMats[column][row])

            elif tiles[column][row] == 1:
                wallTiles.append([x_pos +
                                  GameStore.starting_point_x[surface_id],
                                  y_pos +
                                  GameStore.starting_point_y[surface_id]])

                material = assign_material(tile_class, tiles[column][row],
                                           tileTypes[column][row],
                                           tileMats[column][row])

            elif tiles[column][row] == 2:
                doorTiles.append([x_pos +
                                  GameStore.starting_point_x[surface_id],
                                  y_pos +
                                  GameStore.starting_point_y[surface_id]])

                material = assign_material(
                    tile_class, tiles[column][row],
                    tileTypes[column][row], tileMats[column][row])

            allTiles.append(tiles[column][row])
            allTilePositions.append([x_pos +
                                    GameStore.starting_point_x[surface_id],
                                    y_pos +
                                    GameStore.starting_point_y[surface_id]])
            GameStore.levels[surface_id].blit(material, (x_pos, y_pos,
                                                         TILE_SIZE, TILE_SIZE))


def assign_material(self, image_id, type_id, material_id):
    """
    Assign a randomly chosen variation texture.

    :arg material_id:   specifies the type of material the function will assign
    :arg type_id        specifies the type of image
     that will be used as a base image
    :arg image_id:      input image the function will modify
    :arg self           the class in which the textures were
     generated and assigned values
    :return: Tile texture with randomly generated features
    """
    # load up the base image
    base_image = self.tileTypes[image_id][type_id]
    # if the image type is a floor
    # and material type is not in perfect condition
    if image_id == 1 and material_id > 0:
        # if the material type is really old
        if material_id == 2:
            # choose a randomly chosen really old texture instance
            self.random_inst = self.type_2_inst[
                random.randint(0, len(self.type_2_inst)-1)]
        else:
            # choose a randomly chosen dirty texture instance
            self.random_inst = self.type_1_inst[
                random.randint(0, len(self.type_1_inst)-1)]

        # assign the variation texture
        texture = pygame.image.load("Well Escape tiles/varieties/" +
                                    "Procedural-" + str(image_id) +
                                    "_type-" + str(type_id) +
                                    "_mat-" + str(material_id) +
                                    "_inst-" + str(self.random_inst) + ".png")
    else:
        # keep the texture the same
        texture = base_image

    return texture


def get_dungeon_room(first):
    """
    Choose a pixel map.

    :param first:   specifies if there's a need to generate the starting room
    :return:    a randomly chosen pixel map
    """
    # load up the pixel maps
    pixel_map = "pixelLevels/"
    small_room = pygame.image.load(pixel_map + "smallRoom_000.png")
    hallway = pygame.image.load(pixel_map + "hall_000.png")
    mid_room = pygame.image.load(pixel_map + "MidRoom_000.png")
    rooms = [hallway, small_room, mid_room]
    room_weights = [0.5, 0.75, 0.25]
    if first:
        # load up and choose the starting room pixel map
        current_module = pygame.image.load(pixel_map + "start.png")
    else:
        # choose a random pixel map
        current_module = random.choices(rooms, room_weights)[0]

    return current_module
