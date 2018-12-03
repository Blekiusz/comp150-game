"""Driver Ashley Sands; Navigator: None."""
import pygame
import math
import library


def gray_scale_image(pixel_color, color_weight=(1, 1, 1)):
    """
    Grey scale an image.

    :param pixel_color:     color of pixel
    :param color_weight:    color channel weights
    :return:                gray scale image (r, g, b, a)
    """
    # apply the weights the color
    weighted_color = multiply_color(pixel_color, color_weight)
    # get the average
    color_average = (weighted_color[0] +
                     weighted_color[1] +
                     weighted_color[2]
                     ) // 3
    # clamp the color to 255
    if color_average > 255:
        color_average = 255

    # return color [2, 1, 0, 3] this prevents the red and blue
    # channels from flipping
    # return the original pixel alpha to preserve the transparency
    return color_average, color_average, color_average, pixel_color[3]


def distance(color_base, color_comparitor):
    """
    It does not matter what way base and comparitor are.

    :param color_base:          Color to remove
    :param color_comparitor:    Color to test
    :return:                    difference
    """
    red = (color_base[0] - color_comparitor[0]) ** 2
    green = (color_base[1] - color_comparitor[1]) ** 2
    blue = (color_base[2] - color_comparitor[2]) ** 2

    return math.sqrt(red + green + blue)


def close_enough(pixle_color, color_comparitor, tolerance):
    """
    Check if the pixel colour is close enough to the comparitor.

    :param pixle_color:         color
    :param color_comparitor:    color to test agants
    :param tolerance:           tolerance 0 - 1
    :return:                    turn if close enough
    """
    if distance(pixle_color, color_comparitor) < (tolerance*450):
        return True
    else:
        return False


def change_color(color_base, color_comparitor, tolerance, replace_color):
    """Change the colour of the image."""
    if close_enough(color_base, color_comparitor, tolerance):
        # return color [2, 1, 0, 3] this prevents the red and blue
        # channels from flipping
        # return the alpha form color base to preserve the original alpha
        return (replace_color[0], replace_color[1],
                replace_color[2], color_base[3])
    else:
        # return color [2, 1, 0, 3] this prevents the red and blue
        # channels from flipping
        return color_base[0], color_base[1], color_base[2], color_base[3]


def posterization(new_color_amount, pixel_color):
    """
    Posterize the image.

    :param new_color_amount: Tuple of 3 amouts [0] = min, [1] = mid, [2] = max
    :param pixel_color: the current pixel color
    :return: Color (r, g, b, a)
    """
    one_third = 255 // 3

    for c in range(3):
        if pixel_color[c] < one_third:
            pixel_color[c] = new_color_amount[0]
        elif pixel_color[c] < (one_third * 2):
            pixel_color[c] = new_color_amount[1]
        elif pixel_color[c] < 255:
            pixel_color[c] = new_color_amount[2]

    # im not shore why but this one needs to be returned [0, 1, 2, 3]
    # rather than [2, 1, 0, 3]
    # to prevent the red and blue channels getting flipped
    return pixel_color[0], pixel_color[1], pixel_color[2], pixel_color[3]


def posterization_color_distance(new_color, pixel_color,
                                 color_comparitor, tolerance):
    """
    Second posterization algorithm.

    :param new_color: there needs to be one more color than tollerances
    :param pixel_color:
    :param color_comparitor:
    :param tolerance: tuple or list of tolerance.
     must be in order smallest to largest
    :return:    new color (r, g, b, a)
    """
    for t in range(len(tolerance)):
        if close_enough(pixel_color, color_comparitor, tolerance[t]):
            # return color [2, 1, 0, 3] this prevents the red and blue
            # channels from flipping
            # return with the original pixel alpha to preserve the transparency
            return (new_color[t][2], new_color[t][1],
                    new_color[t][0], pixel_color[3])

    # return color [2, 1, 0, 3] this prevents the red and blue
    # channels from flipping
    # return with the original pixel alpha to preserve the transparency
    return (new_color[len(tolerance)-1][2], new_color[len(tolerance)-1][1],
            new_color[len(tolerance)-1][0], pixel_color[3])


def tint_image(pixel_color, color_weight=(1.1, 0.9, 1),
               tones=(62, 191), base_color_id=0):
    """
    Tint the image.

    :param pixel_color:     color to update
    :param color_weight:    rgb
    :param tones:           tints[0] = shadows, [1] == midtones
    :param base_color_id    0 = red, 1 = green, 2 = blue
    (does nothing if image is grayscale)
    :return:                new color.
    """
    if pixel_color[base_color_id] < tones[0]:
        pixel_color = multiply_color(pixel_color, color_weight)

    if pixel_color[base_color_id] > tones[0] < tones[1]:
        pixel_color = multiply_color(pixel_color, color_weight)

    if pixel_color[base_color_id] >= tones[1]:
        pixel_color = multiply_color(pixel_color, color_weight)

    pixel_color = clamp255_color(pixel_color)

    return pixel_color[2], pixel_color[1], pixel_color[0], pixel_color[3]


def blur(x, y, amount, image, tolerance=0):
    """
    Blur an image.

    :param x:           current X axis pixel id
    :param y:           current Y axis puxel id
    :param amount:      the amount of blue (0-n)
    :param image:       the image that is getting blued
    (or a dif image of the same size for a funky effect)
    :return:            blued pixel
    """
    # set p to count the amount of pixels in the tolerance range
    p = 0
    # store the current pixel so it can be tested against it neighboring pixels
    current_pixel_color = image.get_at((x, y))
    # stores the sum for color
    temp_col = [0, 0, 0]
    # stores the sum for transparency
    trans = 0

    for ix in range(-1, 1):
        for iy in range(-1, 1):
            # check the pixel exists or is not the current pixel
            if (ix != 0 or iy != 0) and x + ix >= 0 < image.get_width()\
                    and y + iy >= 0 < image.get_height():

                # neighboring pixel color
                pixel_color = image.get_at((x + ix, y + iy))
                # check pixel color is in range and skip trans pixels
                if close_enough(current_pixel_color, pixel_color, tolerance)\
                        and pixel_color[3] > 0:

                    # add the color and transparency
                    temp_col = add_color(temp_col, pixel_color, False)
                    trans += pixel_color[3]
                    # count that we have added more color
                    p += 1

    temp_col = multiply_color(temp_col, (amount, amount, amount))

    # add the current pixel color
    temp_col = add_color(temp_col, current_pixel_color, False)

    # get the color average
    temp_col = div_color(temp_col, p+1)

    # add the current transparency
    trans += current_pixel_color[3]
    # and get its average
    trans //= p+1

    # clamp the color to 255
    temp_col = clamp255_color(temp_col)

    return int(temp_col[0]), int(temp_col[1]), int(temp_col[2]), trans


def transparency_by_color_distance(pixel_color, color_comparitor,
                                   tolerance, new_alpha):
    """
    Set the alpha if the pixel_color is in range of the color_comparitor.

    :param pixel_color:         current pixel color
    :param color_comparitor:    color to test against pixel color
    :param tolerance:           the tolerance (0 - 1)
    :param new_alpha:           the new alpha of the pixel if in range
    :return:                    returns new pixel color
    """
    if close_enough(pixel_color, color_comparitor, tolerance):
        return pixel_color[2], pixel_color[1], pixel_color[0], new_alpha
    else:
        return pixel_color[2], pixel_color[1], pixel_color[0], pixel_color[3]


def add_color(color_a, color_b, clamp=True):
    """
    Add two colors together (ignores alpha).

    :param color_a:
    :param color_b:
    :param clamp:       should the color be clamped to 0-255
    :return:            new color
    """
    color_a = list(color_a)
    color_a[0] += color_b[0]
    color_a[1] += color_b[1]
    color_a[2] += color_b[2]

    # return the color with each channel clamped between 0-255
    if clamp:
        return clamp0_color(clamp255_color(color_a))
    else:
        return color_a


def div_color(color_a, by):
    """
    Divide a color by.

    :param color_a:     the color
    :param by:          the amount to divide by
    :return:            new color
    """
    color_a = list(color_a)

    color_a[0] //= by
    color_a[1] //= by
    color_a[2] //= by

    return color_a


def multiply_color(pixel_color, color_weights):
    """
    Multiply the color chanel by color weight.

    :param pixel_color:     (r, g, b) color
    :param color_weights:   weights tuple (r, g, b)
    :return:                weighted color
    """
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        pixel_color[c] *= color_weights[c]
    return tuple(pixel_color)


def correct_color_value(color_value):
    """Make sure that the color values are ints."""
    return int(color_value[0]), int(color_value[1]), int(color_value[2])


def clamp255_color(pixel_color):
    """Clamp color channel to 255."""
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        if pixel_color[c] > 255:
            pixel_color[c] = 255
    return tuple(pixel_color)


def clamp0_color(pixel_color):
    """Clamp color channel to 0."""
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        if pixel_color[c] < 0:
            pixel_color[c] = 0
    return tuple(pixel_color)


def run_effect(effect_name, image_to_update,
               effect_inputs=None, loading_function=None):
    """
    Run a single effect.

    :param effect_name:         name of effect to run
    :param image_to_update:     image to be updated
    :param effect_inputs:       inputs for applied fx.
     See effect function for inputs. (must be tuple and in order)
    :param loading_function:    loading function, surface and rect position.
     tuple(function, surface, rect).
    if none then not displayed
    :return:                    None
    """
    # if the effect type is blur make a copy of the image to pass into the
    # blur function to prevent it from blurring from an already blurred pixel
    if effect_name == "blur" or effect_name == "blue_distance":
        blur_original = image_to_update.copy()

        # get the pixel array for the image we want to update
    pixel_array = pygame.PixelArray(image_to_update)

    # start an update pixel count for loading bar
    updated_pixel_count = 0
    # get the total amount of pixels for loading bar
    total_pixels = len(pixel_array) * len(pixel_array[0])

    # loop x and y pixels
    for x in range(0, len(pixel_array)):
        for y in range(0, len(pixel_array[x])):
            # get the color at the current pixel
            pixel_color = image_to_update.get_at((x, y))

            # find effect to run
            # gray scale
            if effect_name == "greyscale":
                pixel_color = gray_scale_image(pixel_color, effect_inputs)
            # change color
            elif effect_name == "change_color":
                color_comparator = multiply_color(
                    effect_inputs[0], [255, 255, 255]
                )
                tolerance = effect_inputs[1]
                replacement_color = multiply_color(
                    effect_inputs[2], [255, 255, 255]
                )
                pixel_color = change_color(pixel_color, color_comparator,
                                           tolerance, replacement_color)
            # posterization
            elif effect_name == "poster":
                color_amounts = multiply_color(effect_inputs, [255, 255, 255])
                color_amounts = correct_color_value(color_amounts)
                pixel_color = posterization(color_amounts, pixel_color)
            # posterization by color distance
            elif effect_name == "poster_dist":
                color_level_1 = correct_color_value(
                    multiply_color(effect_inputs[0][0], [255, 255, 255])
                )
                color_level_2 = correct_color_value(
                    multiply_color(effect_inputs[0][1], [255, 255, 255])
                )
                color_level_3 = correct_color_value(
                    multiply_color(effect_inputs[0][2], [255, 255, 255])
                )
                color_levels = color_level_1, color_level_2, color_level_3
                color_comparator = correct_color_value(
                    multiply_color(effect_inputs[1], [255, 255, 255])
                )
                tolerance = effect_inputs[2]
                pixel_color = posterization_color_distance(
                    color_levels, pixel_color, color_comparator, tolerance
                )
            # tint
            elif effect_name == "tint":
                tones = [effect_inputs[1][0] * 255, effect_inputs[1][1] * 255]
                color_weights = effect_inputs[0]
                pixel_color = tint_image(
                    pixel_color, color_weights, tones,  base_color_id=2
                )  # todo add base color
            elif effect_name == "blur":
                pixel_color = blur(x, y, 1, blur_original, effect_inputs)
            elif effect_name == "set_alpha_dist":
                color_comparator = correct_color_value(
                    multiply_color(effect_inputs[0], [255, 255, 255])
                )
                alpha = int(effect_inputs[2] * 255)
                pixel_color = transparency_by_color_distance(
                    pixel_color, color_comparator, effect_inputs[1], alpha
                )
            else:
                # print message in console if fx is not found
                print("[image_effects.run_effect]Error: effect not found ",
                      effect_name)

            # update the current pixel
            pixel_array[x, y] = pixel_color
            # count the update
            updated_pixel_count += 1

        # if there is a loading function display it
        if loading_function is not None:
            loading_function[0](
                loading_function[1], loading_function[2],
                (updated_pixel_count/total_pixels)
            )
    # remove the pixel_array so we can display the image
    del pixel_array
