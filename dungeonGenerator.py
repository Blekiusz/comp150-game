"""Driver - Joachim / Navigator - None."""
import pygame
import random
import tileGenerator
import main
import library
import loadSave
from random import choices

tile_class = tileGenerator.Tiles()

tiles = []
tileTypes = []
tileMats = []
floorTilesX = []
floorTilesY = []
wallTiles = []
doorTiles = []

allTilePositions = []
allTiles = []
allTileMaterials = []

TILE_SIZE = tile_class.floorImg.get_rect().width
materials = tile_class.tileTypes


class DungeonGenerator:
    """Generate the procedural dungeon from a pixel map."""

    player = None
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
    chest_map = pygame.Surface
    MAP_WIDTH = 0
    MAP_HEIGHT = 0
    top_col = False
    bottom_col = False
    left_col = False
    right_col = False
    collisions = [top_col, bottom_col, left_col, right_col]
    start_x = []
    start_y = []
    end_x = []
    end_y = []
    # todo rename level count to room count
    START_LEVEL_COUNT = 2
    levelCount = 2
    current_dungeon = 0
    levels = []
    chests = []
    starting_point_x = []
    starting_point_y = []
    current_tile = 0
    last_tile = 0
    current_tiles = []
    prediction_X = 0
    prediction_Y = 0
    secondary_prediction_X = 0
    secondary_prediction_Y = 0
    # should the first room be the well room?
    well_room = True
    reset_fuel = False
    add_fuel = False

    load_count = 1
    current_loaded = 0

    for num in range(levelCount):
        levels.append(pygame.Surface)
        starting_point_x.append(0)
        starting_point_y.append(0)

    def reset(self, first_scene=False, is_reset=False):
        """reset all the tile variables and create a new dungeon."""
        if not first_scene and not is_reset:
            self.current_dungeon += 1
        elif first_scene:
            self.current_dungeon = 0

        self.well_room = first_scene
        self.levelCount = self.START_LEVEL_COUNT + self.current_dungeon
        self.starting_point_x.clear()
        self.starting_point_y.clear()
        self.levels.clear()
        for num in range(self.levelCount):
            self.levels.append(pygame.Surface)
            self.starting_point_x.append(0)
            self.starting_point_y.append(0)

        if is_reset:
            self.reset_fuel = True  # fuel_meter.add_fuel() # reset_fuel()

        floorTilesX.clear()
        floorTilesY.clear()
        wallTiles.clear()
        doorTiles.clear()
        allTilePositions.clear()
        allTiles.clear()
        allTileMaterials.clear()
        self.chests.clear()
        self.start_x.clear()
        self.start_y.clear()
        self.end_x.clear()
        self.end_y.clear()
        # Todo check that the animation are being reset
        #  once the doors are not getting spawned on next level!
        main.aiAnimationPaths.reset_animator(first_scene)
        self.current_tile = 0
        self.create_dungeon(self)

    def create_dungeon(self):
        """Generate the dungeon."""

        # reset all lists
        self.load_count = len(self.levels)
        self.current_loaded = 0

        library.RESET = True
        for i in range(len(self.levels)):
            if i > 0:
                self.gen_rand_map_tiles(self, i)

                # set the starting point for the next room
                self.starting_point_x[i] = \
                    self.starting_point_x[i - 1] + \
                    self.end_x[i-1] * TILE_SIZE - \
                    (self.start_x[i-1] * TILE_SIZE)

                self.starting_point_y[i] = \
                    self.starting_point_y[i - 1] + \
                    self.end_y[i-1] * TILE_SIZE
            else:
                # create the room
                self.gen_rand_map_tiles(self, i)

            self.current_loaded += 1
            loading_x_position = (main.WINDOW_WIDTH/2) - 200;
            library.loading_bar(main.screen,
                                (loading_x_position, 300, 400, 250),
                                self.current_loaded / self.load_count
                                )

            self.initialize_level(self, i)
            self.gen_chest_map(self, i)

        main.aiAnimationPaths.apply_position_offset_to_room_path(
            self.starting_point_x, self.starting_point_y)
        main.start()

    def gen_chest_map(self, level_id):
        """Generate a map of all chests in the level."""
        map_width = self.chest_map.get_width()
        map_height = self.chest_map.get_height()

        for y in range(map_height):
            for x in range(map_width):

                pixel = self.chest_map.get_at((x, y))

                if pixel.r == 125 and pixel.a > 100:  # 0 < pixel_tone < 255:
                    pos_x = x * TILE_SIZE + self.starting_point_x[level_id]
                    pos_y = y * TILE_SIZE + self.starting_point_y[level_id]
                    chest = [pos_x, pos_y]
                    self.chests.append(chest)

        return self.chests

    def draw_chest(self):
        """Draw a chest on screen."""
        for chest in range(len(self.chests)):
            current_chest = self.chests[chest]
            x_pos = self.x + current_chest[0] - self.offsetX
            y_pos = self.y + current_chest[1] - self.offsetY
            main.screen.blit(tile_class.tileTypes[3][0], (x_pos,
                                                          y_pos,
                                                          TILE_SIZE,
                                                          TILE_SIZE)
                             )

    def gen_rand_map_tiles(self, instance):
        """
        Generate the random map tiles with different probabilities.

        :return: tile type ID [x][y]
        """
        # choose a random pixel map and generate a surface for the tiles
        if instance == 0:
            dungeon_room = self.get_dungeon_room(self, self.well_room)
            self.pixel_map = dungeon_room[0]
            self.chest_map = dungeon_room[1]
        else:
            dungeon_room = self.get_dungeon_room(self, False)
            self.pixel_map = dungeon_room[0]
            self.chest_map = dungeon_room[1]
        self.MAP_WIDTH = self.pixel_map.get_width()
        self.MAP_HEIGHT = self.pixel_map.get_height()

        # set variables for random material variation
        material_types = [0, 1, 2]
        material_weights = [0.9, 0.6, 0.3]

        # choose random types of the floor and wall images
        floor = random.randrange(len(tile_class.tileTypes[0]))
        wall = random.randrange(len(tile_class.tileTypes[1]))

        tiles.clear()
        tileTypes.clear()
        tileMats.clear()

        self.load_count += (self.MAP_WIDTH * self.MAP_HEIGHT)

        # Scroll through each pixel in a map and assign according tiles
        # depending on the pixel brightness.
        # Assign a randomly chosen material type value to each tile.
        for y in range(self.MAP_HEIGHT):
            tile_row = []
            type_row = []
            mat_row = []
            for x in range(self.MAP_WIDTH):
                pixel = self.pixel_map.get_at((x, y))
                pixel_tone = (pixel.r + pixel.g + pixel.b) / 3
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
                    self.start_x.append(x)
                    self.start_y.append(y)
                else:
                    if instance == len(self.levels) - 1:
                        tile = 2
                        t_type = 1
                    else:
                        tile = 0
                        t_type = floor
                    self.end_x.append(x)
                    self.end_y.append(y)

                # horizontal row of tiles
                tile_row.append(tile)
                # horizontal row of tile types
                type_row.append(t_type)

                # single material
                material = choices(material_types, material_weights)[0]
                # horizontal row of materials
                mat_row.append(material)

                #update loaded count
                self.current_loaded += 1

            loading_x_position = (main.WINDOW_WIDTH/2) - 200
            library.loading_bar(main.screen,
                                (loading_x_position, 300, 400, 250),
                                self.current_loaded / self.load_count
                                )

            # vertical column of horizontal tile rows
            tiles.append(tile_row)
            # vertical column of horizontal type rows
            tileTypes.append(type_row)
            # vertical column of horizontal material rows
            tileMats.append(mat_row)
        return tiles

    @staticmethod
    def get_position_with_offset(x_pos, y_pos):
        """Get the objects position with the map offset included."""
        x_pos = DungeonGenerator.x + x_pos - DungeonGenerator.offsetX
        y_pos = DungeonGenerator.y + y_pos - DungeonGenerator.offsetY

        return x_pos, y_pos

    def get_positon_by_tile_coordinates(self, x_cord, y_cord):
        """Get a position using the tile coordinates."""
        x_pos, y_pos = self.get_position_with_offset(TILE_SIZE * x_cord,
                                                     TILE_SIZE * y_cord)

        return x_pos, y_pos

    @staticmethod
    def get_coordinates_from_position(x_position, y_position, offset=(0, 0)):
        """
        Driver: ashley.

        :param x_position:      x position to get coords for
        :param y_position:      y position to get coords for
        :param offset           position offset
        :return:                (X coords, Y Coords)
        """
        x_coords = x_position / TILE_SIZE + offset[0]
        y_coords = y_position / TILE_SIZE + offset[1]

        return int(x_coords), int(y_coords)

    @staticmethod
    def assign_material(tileclass, image_id, type_id, material_id):
        """
        Assign a randomly chosen variation texture.

        :arg material_id:   specifies the type of material
         the function will assign
        :arg type_id        specifies the type of image
         that will be used as a base image
        :arg image_id:      input image the function will modify
        :arg tileclass           the class in which the textures were
         generated and assigned values
        :return: Tile texture with randomly generated features
        """
        # load up the base image
        base_image = tileclass.tileTypes[image_id][type_id]
        # if the image type is a floor
        # and material type is not in perfect condition
        if image_id == 1 and material_id > 0:
            # if the material type is really old
            if material_id == 2:
                # choose a randomly chosen really old texture instance
                tileclass.random_inst = tileclass.type_2_inst[
                    random.randint(0, len(tileclass.type_2_inst) - 1)]
            else:
                # choose a randomly chosen dirty texture instance
                tileclass.random_inst = tileclass.type_1_inst[
                    random.randint(0, len(tileclass.type_1_inst) - 1)]

            # assign the variation texture
            texture = pygame.image.load("Well Escape tiles/varieties/" +
                                        "Procedural-" + str(image_id) +
                                        "_type-" + str(type_id) +
                                        "_mat-" + str(material_id) +
                                        "_inst-" + str(tileclass.random_inst)
                                        + ".png")
        else:
            # keep the texture the same
            texture = base_image

        return texture

    def initialize_level(self, surface_id):
        """Draw the tiles with according images on a blank surface."""
        # generate the map
        DungeonGenerator.levels[surface_id] = pygame.Surface(
            (DungeonGenerator.MAP_WIDTH * TILE_SIZE,
             DungeonGenerator.MAP_HEIGHT * TILE_SIZE))

        self.load_count += len(tile_class.tileTypes[1]) * \
                           DungeonGenerator.mud_variations
        self.load_count += len(tile_class.tileTypes[1]) * \
                           DungeonGenerator.moss_variations

        # generate material variations
        while DungeonGenerator.mud_variations > 0 or \
                DungeonGenerator.moss_variations > 0:



            if self.mud_variations > 0:
                for i in range(len(tile_class.tileTypes[1])):
                    tile_class.generate_material(1, i, 1, DungeonGenerator.
                                                 mud_variations)
                    self.current_loaded += 1
                DungeonGenerator.mud_variations -= 1

            if self.moss_variations > 0:
                for i in range(len(tile_class.tileTypes[1])):
                    tile_class.generate_material(1, i, 2, DungeonGenerator.
                                                 moss_variations)
                    self.current_loaded += 1
                DungeonGenerator.moss_variations -= 1

            loading_x_position = (main.WINDOW_WIDTH / 2) - 200
            library.loading_bar(main.screen,
                                (loading_x_position, 300, 400, 250),
                                self.current_loaded / self.load_count
                                )

        self.load_count += (DungeonGenerator.MAP_HEIGHT *
                            DungeonGenerator.MAP_WIDTH
                            )

        # draw the tiles to the level surface
        for column in range(DungeonGenerator.MAP_HEIGHT):
            for row in range(DungeonGenerator.MAP_WIDTH):
                x_pos = row * TILE_SIZE
                y_pos = column * TILE_SIZE

                material = pygame.Surface
                if tiles[column][row] == 0:
                    if surface_id == 0:
                        if column == 1:
                            floorTilesX.append([x_pos +
                                                DungeonGenerator.
                                               starting_point_x[surface_id],
                                                y_pos +
                                                DungeonGenerator.
                                               starting_point_y[surface_id]])
                        if row == 1:
                            floorTilesY.append([x_pos +
                                                DungeonGenerator.
                                               starting_point_x[surface_id],
                                                y_pos +
                                                DungeonGenerator.
                                               starting_point_y[surface_id]])

                    material = self.assign_material(tile_class,
                                                    tiles[column][row],
                                                    tileTypes[column][row],
                                                    tileMats[column][row])

                elif tiles[column][row] == 1:
                    wallTiles.append([x_pos +
                                      DungeonGenerator.starting_point_x[
                                          surface_id],
                                      y_pos +
                                      DungeonGenerator.starting_point_y[
                                          surface_id]])

                    material = self.assign_material(tile_class,
                                                    tiles[column][row],
                                                    tileTypes[column][row],
                                                    tileMats[column][row])

                elif tiles[column][row] == 2:
                    doorTiles.append([x_pos +
                                      DungeonGenerator.starting_point_x[
                                          surface_id],
                                      y_pos +
                                      DungeonGenerator.starting_point_y[
                                          surface_id]])

                    material = self.assign_material(
                        tile_class, tiles[column][row],
                        tileTypes[column][row], tileMats[column][row])

                elif tiles[column][row] == 3:
                    material = self.assign_material(
                        tile_class, tiles[column][row],
                        tileTypes[column][row], tileMats[column][row])

                # todo make the allTiles list a 2d array
                # (append only the columns)
                allTiles.append(tiles[column][row])
                allTileMaterials.append(tileTypes[column][row])
                allTilePositions.append([x_pos +
                                         DungeonGenerator.starting_point_x[
                                             surface_id],
                                         y_pos +
                                         DungeonGenerator.starting_point_y[
                                             surface_id]])
                DungeonGenerator.levels[surface_id].blit(material,
                                                         (x_pos, y_pos,
                                                          TILE_SIZE,
                                                          TILE_SIZE))

    def get_dungeon_room(self, first):
        """
        Choose a pixel map.

        :param first:   specifies if there's a need to generate
         the starting room
        :return:    a randomly chosen pixel map
        """
        # load up the pixel maps
        # the start map need to come from its own folder
        # so it is not included in the main room maps
        start_map = "pixelLevels/startMap/"
        pixel_map = "pixelLevels/"
        chest_map = "pixelLevels/chestMaps/"
        ai_map = "pixelLevels/aiOverlays/"

        # we only need to store the file names with out the path.
        # as there **MUST** be a corresponding image in both
        # chestMaps and aiOverlays with the same name.

        # [hallway, small_room, mid_room]
        rooms = loadSave.get_file_names_in_directory(pixel_map, ".png")

        indexes = list(range(len(rooms)))
        # Todo this needs to be set at the start
        # so it does not change each time we select a room.
        # [0.5, 0.75, 0.25]
        room_weights = self.get_random_room_weights(len(indexes))

        if first:
            # load up and choose the starting room pixel map
            current_module = pygame.image.load(start_map + "start.png")
            current_chest = pygame.image.load(start_map + "start_chest.png")
        else:
            # choose a random pixel map
            current_index = random.choices(indexes, room_weights)[0]
            current_module = pygame.image.load(pixel_map + rooms[
                current_index])
            current_chest = pygame.image.load(chest_map + rooms[current_index])
            main.aiAnimationPaths.load_paths(ai_map + rooms[current_index])

        return current_module, current_chest

    @staticmethod
    def get_random_room_weights(count):
        """Get a random list of weights.

        :param count:   Amount of weights to generate
        :return:        weights list
        """
        weights = []

        for i in range(count):
            weights.append(random.random())

        return weights

    @staticmethod
    def get_edge_name_from_move_direction(move_direction):
        """
        Get the related edge name for move direction.

        Driver: Ashley
        :param move_direction: name of move direction
        :return:               name of edge corresponding to the move direction
        """
        if move_direction == "forwards":
            return "top"
        elif move_direction == "right":
            return "right"
        elif move_direction == "backwards":
            return "bottom"
        elif move_direction == "left":
            return "left"
        else:
            print(
                "Error: direction (",
                move_direction,
                ") not fond (DungGen.get_edge_name_from_move_direction)"
            )

    def get_collider_edge(self, edge_name):
        """
        Get players collider edges value.

        Driver: Ashley
        :param edge_name:   Name of edge to reset
        :return:            Value of the player collider edges
        """
        if edge_name == "top":
            return self.top_col
        elif edge_name == "right":
            return self.right_col
        elif edge_name == "bottom":
            return self.bottom_col
        elif edge_name == "left":
            return self.left_col
        else:
            print(
                "Error: Edge (",
                edge_name,
                ") not fond (DungGen.get_collider_edge)"
            )

    def reset_collider_edge(self, edge_name):
        """
        Reset collider edge.

        Driver: Ashley
        :param edge_name:   Name of edge to reset
        :return:            None
        """
        if edge_name == "top":
            self.top_col = False
        elif edge_name == "right":
            self.right_col = False
        elif edge_name == "bottom":
            self.bottom_col = False
        elif edge_name == "left":
            self.left_col = False
        else:
            print(
                "Error: Edge (",
                edge_name,
                ") not fond (DungGen.reset_collider_edge)"
            )

    def update_position(self,
                        move_direction,
                        move_amount,
                        previous_position=None
                        ):
        """
        Update dungeon position.

        Driver: Ashley
        :param move_direction:      name of direction to move in
        :param move_amount:         amount to move
        :param previous_position:   if None its set to position
        :return:                    None
        """
        if move_direction == "forwards" or move_direction == "backwards":
            if previous_position is None:
                self.previousY = self.y
            else:
                self.previousY = previous_position

            self.y += move_amount

        else:
            if previous_position is None:
                self.previousX = self.x
            else:
                self.previousX = previous_position

            self.x += move_amount

    def get_axis_position_from_move_direction(self, move_direction):
        """
        Get position of an axis corresponding to the move direction.

        Driver: Ashley
        :param move_direction:  name of direction to get the position of
        :return:                position of the corresponding axis
        """
        if move_direction == "forwards" or move_direction == "backwards":
            return self.y
        else:
            return self.x

    def get_axis_previous_position_from_move_direction(self, move_direction):
        """
        Get previous position of an axis corresponding to the move direction.

        Driver: Ashley
        :param move_direction:  name of direction to get the position of
        :return:                previous position of the corresponding axis
        """
        if move_direction == "forwards" or move_direction == "backwards":
            return self.previousY
        else:
            return self.previousX

    def set_prediction(self,
                       move_direction,
                       main_value=None,
                       secondary_value=None
                       ):
        """
        Set main and secondary values corresponding to move direction.

        Driver: Ashley
        :param move_direction:
        :param main_value:          value to set main prediction
                                    (ignored if None)
        :param secondary_value:     value to set secondary prediction
                                    (ignored if None)
        :return:                    None
        """
        if move_direction == "forwards" or move_direction == "backwards":
            if main_value is not None:
                self.prediction_Y = main_value

            if secondary_value is not None:
                self.secondary_prediction_Y = secondary_value

        else:
            if main_value is not None:
                self.prediction_X = main_value

            if secondary_value is not None:
                self.secondary_prediction_X = secondary_value

    def update_dungeon(self,
                       move_direction,
                       opposite_move_direction,
                       move_amount,
                       prediction_value,
                       other_direction_1,
                       other_direction_2
                       ):
        """
        Update the dungeon position.

        Driver: Ashley
        :param move_direction:              Direction to test if moving
        :param opposite_move_direction:     Opposite direction of move test
        :param move_amount:                 Amount to move
        :param prediction_value:            Prediction value
        :param other_direction_1:           One of the other two directions
        :param other_direction_2:           The other, other direction.
        :return:                            None
        """
        if (library.KEY_PRESSED[move_direction] and
                not library.KEY_PRESSED[opposite_move_direction]):
            # Get names of all the edges so its orientated correctly
            move_direction_edge_name = \
                self.get_edge_name_from_move_direction(
                    move_direction
                    )

            opposite_move_direction_edge_name = \
                self.get_edge_name_from_move_direction(
                    opposite_move_direction
                    )

            other_direction_1_edge_name = \
                self.get_edge_name_from_move_direction(
                    other_direction_1
                    )

            other_direction_2_edge_name = \
                self.get_edge_name_from_move_direction(
                    other_direction_2
                    )

            self.reset_collider_edge(self, opposite_move_direction_edge_name)

            if not self.get_collider_edge(self, move_direction_edge_name):
                # move the dungeon and assign prediction values
                prv_axis_position = \
                    self.get_axis_position_from_move_direction(
                        self,
                        move_direction
                        )

                self.update_position(
                    self,
                    move_direction,
                    move_amount,
                    prv_axis_position
                    )

                self.set_prediction(
                    self,
                    move_direction,
                    main_value=prediction_value
                    )

                if not (library.KEY_PRESSED[other_direction_1] or
                        library.KEY_PRESSED[other_direction_2]):
                    self.set_prediction(
                        self,
                        other_direction_1,
                        main_value=0,
                        secondary_value=0
                        )

                if not (self.get_collider_edge(self,
                                               other_direction_1_edge_name
                                               ) or
                        self.get_collider_edge(self,
                                               other_direction_2_edge_name
                                               )):
                    self.set_prediction(
                        self,
                        move_direction,
                        secondary_value=prediction_value
                    )

            else:
                self.set_prediction(self, move_direction, main_value=0)

                current_pos = \
                    self.get_axis_position_from_move_direction(
                        self,
                        move_direction
                    )

                prv_pos = \
                    self.get_axis_previous_position_from_move_direction(
                        self,
                        move_direction
                    )

                if current_pos != prv_pos:
                    self.update_position(self, move_direction, 0)
