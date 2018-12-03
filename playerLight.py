"""Creates 'blocky' shadow and puts overlay on screen."""
import pygame


class Variables:
    """Class that stores all variables."""

    light_intensity = 0.5
    light_range = 9
    light_surface = None
    overlay_image = pygame.image.load('./UI/overlay.png')


def overlay(surface):
    """
    Overlay overlay_image on a surface.

    :param surface: Surface that image will be blit to.
    :return:        No return.
    """
    surface.blit(Variables.overlay_image, (0, 0))


def draw_light(surface, other_script):
    """
    Function displays light_surface on a surface.

    :param surface:     Surface that lightning will be displayed on.
    :param other_script:Connects this script with other so I can use its
                        functions.
    :return:            No return.
    """
    current_tile_x, current_tile_y = other_script.DungeonGenerator.\
        get_coordinates_from_position(
            other_script.DungeonGenerator.player.position[0],
            other_script.DungeonGenerator.player.position[1], (0.5, 0.85))

    current_tile_x -= ((Variables.light_range - 1) // 2)
    current_tile_y -= ((Variables.light_range - 1) // 2)

    pos_x, pos_y = other_script.DungeonGenerator.\
        get_positon_by_tile_coordinates(
            other_script.DungeonGenerator, current_tile_x, current_tile_y)

    surface.blit(Variables.light_surface, (pos_x, pos_y))


def create_light_map(range_value, tile_size, light_intensity, light_surface):
    """
    Function applies linear function to modify alpha channel of a shadow.

    :param range_value:     Value is used to calculate new light_map
    :param tile_size:       Variable used in further functions.
    :param light_intensity: Value changes alpha channel of all squares and
                            lowers them depending on its value
    :param light_surface:   Variable used in further functions.
    :return:                No return.
    """
    for y_range in range(range_value):
        for x_range in range(range_value):
            x_light_value = -(range_value - 1) / 2 + x_range
            y_light_value = -(range_value - 1) / 2 + y_range
            if x_light_value < 0:
                x_light_value = x_light_value * -1
            if y_light_value < 0:
                y_light_value = y_light_value * -1
            x_intensity = (-1 * x_light_value + 3) / 6 * light_intensity
            y_intensity = (-1 * y_light_value + 3) / 6 * light_intensity
            if x_intensity < 0:
                x_intensity = 0
            if y_intensity < 0:
                y_intensity = 0

            total_intensity = (x_intensity + y_intensity)
            total_intensity = round(total_intensity, 2)

            pygame.draw.rect(light_surface,
                             (0, 0, 0, 255 * (1 - total_intensity)),
                             (x_range * tile_size,
                              y_range * tile_size,
                              tile_size,
                              tile_size
                              )
                             )


def initialisation_of_light_surface(range_value, tile_size,
                                    light_intensity):
    """
    Function calculates size of the light_surface.

    :param range_value:     Variable used to calculate size of a light_surface.
    :param tile_size:       Variable used to calculate size of a light_surface.
    :param light_intensity: Variable used in further functions.
    :return:                No return.
    """
    light_surface_size = range_value * tile_size
    light_surface = pygame.Surface((light_surface_size, light_surface_size),
                                   pygame.SRCALPHA
                                   )
    Variables.light_surface = light_surface
    create_light_map(range_value, tile_size, light_intensity, light_surface)


def initialise_lightning(tile_size):
    """
    Function starts lightning generation procedure.

    :param tile_size:   Variable used in further functions.
    :return:            No return.
    """
    initialisation_of_light_surface(Variables.light_range, tile_size,
                                    Variables.light_intensity
                                    )


def update_light(intensity):
    """
    Function synchronises light_intensity value with other script.

    :param intensity:   Value that replaces current light_intensity value.
    :return:            No return
    """
    Variables.light_intensity = intensity
