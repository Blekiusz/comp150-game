"""Collision System by Joachim Rayski."""
import pygame
from pygame.locals import *
import dungeonGenerator as dunGen
import main
import library


class CollisionDetector:
    """Make the player collide with the world."""

    current_tile_index = 0
    current_tile_pos = [0, 0]
    current_tile_type = 0
    current_tile_material = 0

    current_tile_index2 = 0
    current_tile_pos2 = [0, 0]
    current_tile_type2 = 0
    current_tile_material2 = 0

    current_tile_index3 = 0
    current_tile_pos3 = [0, 0]
    current_tile_type3 = 0
    current_tile_material3 = 0

    current_chest_index = 0
    current_chest_pos = [0, 0]

    previous_inputs = [False, False, False, False]

    @staticmethod
    def find_current_tile(prediction_x, prediction_y):
        """
        Find or predict the tile the player is/will be on.

        :param prediction_x: offset for predicting the next tile on the x axis
        :param prediction_y: offset for predicting the next tile on the y axis
        :return: index of the current tile the player is on
        """
        previous_tile = dunGen.allTilePositions[dunGen.DungeonGenerator.
                                                current_tile]
        # round the current player position to the position of the nearest tile
        current_tile_x = int(((dunGen.DungeonGenerator.player.position[0] +
                               prediction_x)
                              / dunGen.TILE_SIZE)
                             + 0.5) * dunGen.TILE_SIZE
        current_tile_y = int(((dunGen.DungeonGenerator.player.position[1] +
                               prediction_y)
                              / dunGen.TILE_SIZE)
                             + 0.85) * dunGen.TILE_SIZE
        tile_pos = [current_tile_x, current_tile_y]

        # if a tile with the calculated position exists
        # and it's not the same as the previous tile
        # set it as the current tile and return the value
        if tile_pos in dunGen.allTilePositions\
                and not tile_pos == previous_tile:
            dunGen.DungeonGenerator.current_tile = \
                dunGen.allTilePositions.index(tile_pos)

        return dunGen.DungeonGenerator.current_tile

    def detect_collision(self):
        """Check for collision between the player and the wall tiles."""
        dunGen.DungeonGenerator.collisions = [dunGen.DungeonGenerator.
                                              top_col,
                                              dunGen.DungeonGenerator.
                                              bottom_col,
                                              dunGen.DungeonGenerator.
                                              left_col,
                                              dunGen.DungeonGenerator.
                                              right_col]

        # find values of the tile the player is currently on
        self.current_tile_index = self.find_current_tile(0, 0)
        self.current_tile_pos = dunGen.allTilePositions[
            self.current_tile_index]
        self.current_tile_type = dunGen.allTiles[
            self.current_tile_index]
        self.current_tile_material = dunGen.allTileMaterials[
            self.current_tile_index]

        # find values of the predicted tile that the player might land on
        self.current_tile_index2 = self.find_current_tile(
            dunGen.DungeonGenerator.prediction_X,
            dunGen.DungeonGenerator.prediction_Y)
        self.current_tile_pos2 = dunGen.allTilePositions[
            self.current_tile_index2]
        self.current_tile_type2 = dunGen.allTiles[
            self.current_tile_index2]
        self.current_tile_material2 = dunGen.allTileMaterials[
            self.current_tile_index2]

        # find values of the second predicted tile
        # that the player might land on
        self.current_tile_index3 = self.find_current_tile(
            dunGen.DungeonGenerator.secondary_prediction_X,
            dunGen.DungeonGenerator.secondary_prediction_Y)
        self.current_tile_pos3 = dunGen.allTilePositions[
            self.current_tile_index3]
        self.current_tile_type3 = dunGen.allTiles[
            self.current_tile_index3]
        self.current_tile_material3 = dunGen.allTileMaterials[
            self.current_tile_index3]

        if self.current_tile_pos in dunGen.DungeonGenerator.chests:
            self.current_chest_index = dunGen.DungeonGenerator.chests.index(
                self.current_tile_pos)
            self.current_chest_pos = dunGen.DungeonGenerator.chests[
                self.current_chest_index]
        else:
            self.current_chest_index = -1

        # if the secondary predicted tile is a floor or a door
        if (self.current_tile_type2 == 0
            or self.current_tile_type2 > 1) and \
                not (self.current_tile_type2 == 2
                     and self.current_tile_material2 == 0) and\
                not self.current_tile_type == 1:

            # save the current movement inputs
            if library.KEY_PRESSED["forwards"]:
                self.previous_inputs[0] = True
                self.previous_inputs[1] = False
            elif library.KEY_PRESSED["backwards"]:
                self.previous_inputs[1] = True
                self.previous_inputs[0] = False
            else:
                self.previous_inputs[0] = False
                self.previous_inputs[1] = False

            if library.KEY_PRESSED["left"]:
                self.previous_inputs[2] = True
                self.previous_inputs[3] = False
            elif library.KEY_PRESSED["right"]:
                self.previous_inputs[3] = True
                self.previous_inputs[2] = False
            else:
                self.previous_inputs[2] = False
                self.previous_inputs[3] = False

            # save the current predicted tile
            dunGen.DungeonGenerator.last_tile = self.current_tile_index2

            # if the current tile is an exit door, block the bottom
            # and let the player press space to restart
            if self.current_tile_type == 2 \
                    and self.current_tile_material == 1:
                    dunGen.DungeonGenerator.reset(dunGen.DungeonGenerator)
                    if self.current_tile_pos[1] <\
                            dunGen.DungeonGenerator.player.position[1]:
                        dunGen.DungeonGenerator.bottom_col = True
                    else:
                        dunGen.DungeonGenerator.bottom_col = False

            if self.current_chest_index > -1:
                dunGen.DungeonGenerator.add_fuel = True
                dunGen.DungeonGenerator.chests.pop(self.current_chest_index)

        # if the secondary predicted tile is a wall tile
        if self.current_tile_type3 == 1 or self.current_tile_type2 == 1 \
                or self.current_tile_type == 1 \
                or (self.current_tile_type3 == 2
                    and self.current_tile_material3 == 0):

            # add all the true collision values to a list
            true_collisions = []
            for i in range(len(dunGen.DungeonGenerator.collisions)):
                if dunGen.DungeonGenerator.collisions[i]:
                    true_collisions.append(dunGen.DungeonGenerator.
                                           collisions[i])

            # block the movement in corresponding directions
            # depending on the current and predicted tiles' types
            if self.current_tile_type == 1 and \
                    not self.current_tile_type3 == 0:
                if self.previous_inputs[0]:
                    dunGen.DungeonGenerator.top_col = True
                if self.previous_inputs[1]:
                    dunGen.DungeonGenerator.bottom_col = True
                if self.previous_inputs[2]:
                    dunGen.DungeonGenerator.left_col = True
                if self.previous_inputs[3]:
                    dunGen.DungeonGenerator.right_col = True
            else:
                difference = dunGen.DungeonGenerator.last_tile \
                             - self.current_tile_index2
                if difference > 1:
                    dunGen.DungeonGenerator.top_col = True
                    if len(true_collisions) < 1:
                        dunGen.DungeonGenerator.secondary_prediction_X = 0
                if difference < -1:
                    dunGen.DungeonGenerator.bottom_col = True
                    if len(true_collisions) < 1:
                        dunGen.DungeonGenerator.secondary_prediction_X = 0
                if difference == 1:
                    dunGen.DungeonGenerator.left_col = True
                    if len(true_collisions) < 1:
                        dunGen.DungeonGenerator.secondary_prediction_Y = 0
                if difference == -1:
                    dunGen.DungeonGenerator.right_col = True
                    if len(true_collisions) < 1:
                        dunGen.DungeonGenerator.secondary_prediction_Y = 0
        else:
            # disable collisions
            dunGen.DungeonGenerator.top_col = False
            if not self.current_tile_type2 == 2:
                dunGen.DungeonGenerator.bottom_col = False
            dunGen.DungeonGenerator.left_col = False
            dunGen.DungeonGenerator.right_col = False

    def draw_collision(self):
        """Draw the collision bounds."""
        # create a rect for the current tile
        current_tile_rect = Rect(dunGen.DungeonGenerator.x
                                 + self.current_tile_pos[0]
                                 - dunGen.DungeonGenerator.offsetX,
                                 dunGen.DungeonGenerator.y
                                 + self.current_tile_pos[1]
                                 - dunGen.DungeonGenerator.offsetY,
                                 dunGen.TILE_SIZE, dunGen.TILE_SIZE)
        # create a rect for the predicted tile
        current_tile_rect2 = Rect(dunGen.DungeonGenerator.x
                                  + self.current_tile_pos2[0]
                                  - dunGen.DungeonGenerator.offsetX,
                                  dunGen.DungeonGenerator.y
                                  + self.current_tile_pos2[1]
                                  - dunGen.DungeonGenerator.offsetY,
                                  dunGen.TILE_SIZE, dunGen.TILE_SIZE)
        # create a rect for the secondary predicted tile
        current_tile_rect3 = Rect(dunGen.DungeonGenerator.x
                                  + self.current_tile_pos3[0]
                                  - dunGen.DungeonGenerator.offsetX,
                                  dunGen.DungeonGenerator.y
                                  + self.current_tile_pos3[1]
                                  - dunGen.DungeonGenerator.offsetY,
                                  dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        pygame.draw.rect(main.screen, Color("red"), current_tile_rect3, 3)
        pygame.draw.rect(main.screen, Color("orange"), current_tile_rect2, 3)
        pygame.draw.rect(main.screen, Color("green"), current_tile_rect, 3)
