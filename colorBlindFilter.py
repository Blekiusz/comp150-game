"""COLOUR BLIND FILTER."""
import pygame
import main


class CBFilterStore:
    """Storage class."""

    surface = None


def greyscale_pixel(pixel_color):
    """Change the colour of the screenshot to the grey scale filter."""
    red = pixel_color[0]
    green = pixel_color[1]
    blue = pixel_color[2]

    greyscale = (red + green + blue) // 3

    return greyscale, greyscale, greyscale


def protanopia_pixel(pixel_color):
    """Change the colour of the screenshot to the protanopia filter."""
    red = pixel_color[0]
    green = pixel_color[1]
    blue = pixel_color[2]

    protanopia = ((red * 0), green, blue)

    return protanopia


def deuteranopia_pixel(pixel_color):
    """Change the colour of the screenshot to the deuteranopia filter."""
    red = pixel_color[0]
    green = pixel_color[1]
    blue = pixel_color[2]

    deuteranopia = (red, (green * 0), blue)

    return deuteranopia


def tritanopia_pixel(pixel_color):
    """Change the colour of the screenshot to the tritanopia filter."""
    red = pixel_color[0]
    green = pixel_color[1]
    blue = pixel_color[2]

    tritanopia = (red, green, (blue * 0))

    return tritanopia


# Press "P" and it'll load 4 pictures in the Screenshot folder
def loop_image():
    """Loop through all the images and colour them accordingly."""
    image = pygame.image.load("ColorBlind.png")
    tritan_image = pygame.image.load("ColorBlind.png")
    deuter_image = pygame.image.load("ColorBlind.png")
    protan_image = pygame.image.load("ColorBlind.png")
    grey_scale = pygame.PixelArray(image)
    tritanopia = pygame.PixelArray(tritan_image)
    deuteranopia = pygame.PixelArray(deuter_image)
    protanopia = pygame.PixelArray(protan_image)
    for x in range(0, len(grey_scale)):
        for y in range(0, len(grey_scale[x])):
            pixel_color = image.get_at((x, y))
            grey_scale_col = greyscale_pixel(pixel_color)
            grey_scale[x, y] = grey_scale_col
    for x in range(0, len(tritanopia)):
        for y in range(0, len(tritanopia[x])):
            tritan_pixel_color = tritan_image.get_at((x, y))
            tritan_col = tritanopia_pixel(tritan_pixel_color)
            tritanopia[x, y] = tritan_col
    for x in range(0, len(protanopia)):
        for y in range(0, len(protanopia[x])):
            pixel_color = protan_image.get_at((x, y))
            protanopia_col = protanopia_pixel(pixel_color)
            protanopia[x, y] = protanopia_col
    for x in range(0, len(deuteranopia)):
        for y in range(0, len(deuteranopia[x])):
            pixel_color = deuter_image.get_at((x, y))
            deuteranopia_col = deuteranopia_pixel(pixel_color)
            deuteranopia[x, y] = deuteranopia_col

    del grey_scale
    del tritanopia
    del protanopia
    del deuteranopia
    pygame.image.save(image, "./Screenshots/grey_scale.png")
    pygame.image.save(protan_image, "./Screenshots/protanopia.png")
    pygame.image.save(deuter_image, "./Screenshots/deuteranopia.png")
    pygame.image.save(tritan_image, "./Screenshots/tritanopia.png")


def initialization():
    """Initialize the image surface."""
    CBFilterStore.surface = pygame.Surface(
        (main.WINDOW_WIDTH, main.WINDOW_HEIGHT))


def color_blind_filter():
    """Apply the color blind filter."""
    CBFilterStore.surface.blit(main.screen, (0, 0))
    save(".", "ColorBlind", CBFilterStore.surface)


def save(path, file_name, surf):
    """Save the screenshot."""
    pygame.image.save(surf, path + "/" + file_name + ".png")
    print("saving image")
