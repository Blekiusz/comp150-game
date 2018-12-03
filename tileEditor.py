"""Driver Ashley Sands; Navigator: None."""
# Todo...
# Search '__Add_new__' for places to add new menus, edit windows,
# buttons & button function

import pygame
import sys
import library
import UI
import loadSave
import os
import image_effects
import main
from pygame.locals import *


class EditorStore:
    """Stores the main editor variables."""

    # has the editor been initialized
    initialized = False
    game_state = None
    update_image_directory = False
    current_directory = "./Well Escape tiles"
    # stores the tile paths from the current directory
    directory_tiles = []
    # the current menu to display.
    current_menu = None
    current_menu_buttons = None

    # the surface of the tile we are editing
    edit_tile = None
    selected_fx_id = -1
    current_fx_options = 0

    # prevents the FX getting applied more than once on a single click
    next_options_pressed = False

    select_tile_start_position = 0

    tile_zoom = 1
    save_file_name_input = ""


TILE_SIZE = 93      # default preview tile size
WINDOW_HEIGHT, WINDOW_WIDTH = 750, 1334
WINDOW_MARGIN_X, WINDOW_MARGIN_Y = 50, 50
# set screen to None to force into standalone mode
# main display surface
screen = main.screen
standalone_mode = False

# if screen is set to none initialize py game (standalone mode)
if screen is None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # force to standalone
    standalone_mode = True

# Menus
MENU_START = 0
MENU_SELECT = 1
MENU_EDIT = 2
MENU_SAVE = 3

# FX panels
FX_GRAYSCALE = 0
FX_CHANGECOLOR = 1
FX_POSTER = 2
FX_POSTER_DIST = 3
FX_TINT = 4
FX_BLUR = 5
FX_SETALPHA_DIST = 6


# todo: remove and replace tile_text once cal has push his code.
# set font faces
header_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 55)
sub_header_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 35)
text_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 18)
# headers and sub-headers
header_text_surface = header_fontface.render("Tile Editor", True,
                                             library.BLACK)
# The text will get replaced with a surface containing the text.
sub_headers = {MENU_START: "Main Menu", MENU_SELECT: "Tile Select",
               MENU_EDIT: "Re-skin tool", MENU_SAVE: "Save To File"}

# define buttons
button = UI.UIButtons(None, None, None, (360, 75))
button_small = UI.UIButtons(None, None, None, (50, 50))
button_fx = UI.UIButtons(None, None, None, (175, 75))
image_select_button = UI.UIButtons(None, None, None, (750, 113))
button_type = {"default": button, "small": button_small, "fx": button_fx}

# list of tuples
# (
# label->str, position->tuple, x_position->int, action->str, button_type -> str
# )
# tuples with action == run_effect
# also has effect_ID -> int on the end of the tuple
# tuples with action == tile_select
# also has directory -> str on the end of the tuple
start_menu_button_data = []
tile_select_menu_button_data = []
edit_tile_button_data = []

# set muti purpose sliders
sliders = [None, None]
sliders[0] = UI.UISlider(None, "UI/temp_slider_handle.png", None,
                         "UI/temp_slider.png", (250, 50), 15, (950, 150))
sliders[1] = UI.UISlider(None, "UI/temp_slider_handle.png", None,
                         "UI/temp_slider.png", (250, 50), 15, (950, 250))

# set rgb sliders
sliders_r = UI.UISlider(None, "UI/temp_slider_handle.png", None,
                        "UI/temp_slider.png", (250, 50), 15, (950, 150))
sliders_g = UI.UISlider(None, "UI/temp_slider_handle.png", None,
                        "UI/temp_slider.png", (250, 50), 15, (950, 250))
sliders_b = UI.UISlider(None, "UI/temp_slider_handle.png", None,
                        "UI/temp_slider.png", (250, 50), 15, (950, 350))

# store the inputs for the effects
effect_input_values = []

save_text_input = UI.UIInput((400, 50), 30)


def initialize():
    """
    Initialize the Editor.

    This should only be run once.
    :return: None.
    """
    print("Helloo World!!!!")

    # set current menu to start
    EditorStore.current_menu = MENU_START

    # set font surfaces
    sub_headers[MENU_START] = sub_header_fontface.render(
        sub_headers[MENU_START], True, library.BLACK
    )
    sub_headers[MENU_SELECT] = sub_header_fontface.render(
        sub_headers[MENU_SELECT], True, library.BLACK
    )
    sub_headers[MENU_EDIT] = sub_header_fontface.render(
        sub_headers[MENU_EDIT], True, library.BLACK
    )
    sub_headers[MENU_SAVE] = sub_header_fontface.render(
        sub_headers[MENU_SAVE], True, library.BLACK
    )

    # Set basic select tile button
    # Todo: turn into function
    # normal button
    image_select_button.button_normal = pygame.Surface((750, 113))
    image_select_button.button_normal.fill(library.BLACK)
    pygame.draw.rect(image_select_button.button_normal,
                     library.WHITE, (113, 10, 625, 93))
    # hover button
    image_select_button.button_hover = pygame.Surface((750, 113))
    image_select_button.button_hover.fill(library.DARK_GREY)
    pygame.draw.rect(image_select_button.button_hover,
                     library.WHITE, (113, 10, 625, 93))
    # pressed button
    image_select_button.button_pressed = pygame.Surface((750, 113))
    image_select_button.button_pressed.fill(library.LIGHT_GREY)
    pygame.draw.rect(image_select_button.button_pressed,
                     library.WHITE, (113, 10, 625, 93))

    # add start menu button data
    start_menu_button_data.append(
        ("Floor Tiles", (60, 180), 70, "tile_select",
         "default", "./Well Escape tiles/FloorTiles")
    )
    start_menu_button_data.append(
        ("Wall Tiles", (60, 280), 70, "tile_select",
         "default", "./Well Escape tiles/WallTiles")
    )
    start_menu_button_data.append(
        ("Player Tiles", (60, 380), 70, "tile_select",
         "default", "./Characters")
    )
    start_menu_button_data.append(
        ("Ghost Tiles", (60, 480), 70, "tile_select",
         "default", "./Well Escape tiles/ghostTiles")
    )
    start_menu_button_data.append(
        ("Return To Menu", (60, 580), 50, "return", "default")
    )

    # add select tile menu button data
    tile_select_menu_button_data.append(
        ("+", (1200, 100), 5, "scroll_images_-", "small")
    )
    tile_select_menu_button_data.append(
        ("-", (1200, 550), 5, "scroll_images_+", "small")
    )
    tile_select_menu_button_data.append(
        ("Return To Menu", (60, 580), 50, "return", "default")
    )

    # add edit tile button data
    edit_tile_button_data.append(("-", (390, 75), 20, "-_zoom", "small"))
    edit_tile_button_data.append(("+", (575, 75), 20, "+_zoom", "small"))
    # edit tile fx buttons
    edit_tile_button_data.append(
        ("Apply Grey Scale...", (60, 180), 5,
         "select_effect", "fx", FX_GRAYSCALE)
    )
    edit_tile_button_data.append(
        ("Change Color...", (60, 280), 5,
         "select_effect", "fx", FX_CHANGECOLOR)
    )
    edit_tile_button_data.append(
        ("Posterization...", (60, 380), 5,
         "select_effect", "fx", FX_POSTER)
    )
    edit_tile_button_data.append(
        ("Posterization By Distance Tolerance...", (60, 480), 5,
         "select_effect", "fx", FX_POSTER_DIST)
    )
    edit_tile_button_data.append(
        ("Tint...", (250, 180), 5,
         "select_effect", "fx", FX_TINT)
    )
    edit_tile_button_data.append(
        ("Blur...", (250, 280), 5,
         "select_effect", "fx", FX_BLUR)
    )
    edit_tile_button_data.append(
        ("Set Alpha by Color Tolerance...", (250, 380), 5,
         "select_effect", "fx", FX_SETALPHA_DIST)
    )
    edit_tile_button_data.append(
        ("Cancel", (250, 480), 5,
         "select_effect", "fx", -1)
    )
    # edit tile save button
    edit_tile_button_data.append(
        ("Save Image", (900, 600), 70,
         "save", "default")
    )
    # edit tile back button
    edit_tile_button_data.append(
        ("Return To Menu", (60, 580), 50,
         "return", "default")
    )

    # set the current button set to start menu
    EditorStore.current_menu_buttons = start_menu_button_data


def get_files_in_directory(directory, file_type):
    """
    Get a list of files in a directory. Do not include sub folders.

    Also un-set EditorStore.update_image_directory.
    :param directory:   the directory to search.
    :param file_type:   the extension so search for.
    :return:            list of files in directory with extension.
    """
    EditorStore.update_image_directory = False

    return loadSave.load_files_form_directory(directory, file_type)


def display_select_tile():
    """Update the images form directory and call the button display."""
    if EditorStore.update_image_directory:
        EditorStore.directory_tiles = get_files_in_directory(
            EditorStore.current_directory, ".png"
        )

    # Todo move this into the if, when the optimize is
    # done in display_select_tile_button
    display_select_tile_button()


def display_select_tile_button():
    """
    Draw the tile select buttons to screen.

    Select the tile for edit if pressed.
    """
    # todo: optimize this so the buttons are called from the main button
    # function so they don't get draw every frame

    if EditorStore.select_tile_start_position < 1:
        EditorStore.select_tile_start_position = 0
    elif EditorStore.select_tile_start_position > (len(
            EditorStore.directory_tiles) - 4):
        EditorStore.select_tile_start_position = len(
            EditorStore.directory_tiles) - 4

    if EditorStore.select_tile_start_position + 3 < len(
            EditorStore.directory_tiles):
        select_tile_end_position = EditorStore.select_tile_start_position + 4
    else:
        select_tile_end_position = len(EditorStore.directory_tiles)

    button_row = 0
    # loop each image that can be edited
    for i in range(EditorStore.select_tile_start_position,
                   select_tile_end_position):
        # Add File name text
        temp_surface = label_button(image_select_button.draw_button(
            pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
            (450, 100 + (125 * button_row))), "File Name:"+os.path.basename(
            EditorStore.directory_tiles[i]), text_fontface, 117, 15
        )

        # Add path text
        temp_surface = label_button(
            temp_surface, EditorStore.directory_tiles[i],
            text_fontface, 117, 35
        )
        # display the image on the button
        temp_surface.blit(resize_preview_image(
            pygame.image.load(EditorStore.directory_tiles[i])), (10, 10)
        )

        # display the button
        screen_position = (450, 100 + (125 * button_row))
        screen.blit(temp_surface, screen_position)

        button_row += 1

        # select the tile to be edited if has been pressed.
        if image_select_button.is_pressed(
                pygame.mouse.get_pos(), screen_position,
                library.KEY_PRESSED["mouse"]
        ):
            select_tile(i)


def select_tile(image_path_id):
    """Load the preview tiles from current directory."""
    # todo this can also get move into display_select_tile once optimized
    EditorStore.edit_tile = pygame.image.load(
        EditorStore.directory_tiles[image_path_id]
    )

    button_action("edit_tile")


def display_tile_editor():
    """Display the main tile editor."""
    # get the tile size and work out the new size when zoomed
    zoomed_size_x, zoomed_size_y = EditorStore.edit_tile.get_size()
    zoomed_size_x = int(zoomed_size_x * EditorStore.tile_zoom)
    zoomed_size_y = int(zoomed_size_y * EditorStore.tile_zoom)

    # center the X axis
    x_center = ((WINDOW_WIDTH-100) // 2) - (zoomed_size_x // 2)
    y_center = ((WINDOW_HEIGHT-300) // 2) - (zoomed_size_y // 2)

    # display the zoom text at top of screen
    zoom_text = text_fontface.render(
        "Zoom: "+str(EditorStore.tile_zoom*100)+"%", True, library.BLACK
    )

    # display text input
    save_text_input.draw_text_input(
        pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (450, 615),
        EditorStore.save_file_name_input, screen
    )

    screen.blit(zoom_text, (450, 75))
    # display the image being edited
    screen.blit(
        pygame.transform.scale(
            EditorStore.edit_tile, (zoomed_size_x, zoomed_size_y)
        ),
        (100+x_center, 200+y_center)
    )

    screen.blit(
        get_label(
            "Save File Name", text_fontface, (150, 30),
            background_color=(255, 255, 255, 255)
        ), (450, 585)
    )

    display_fx_panel(EditorStore.selected_fx_id)


def display_fx_panel(panel_id):
    """
    Display the FX panel for the selected fx.

    :param panel_id:    fx id
    :return:            None
    """
    # total amount of panels (varies depending on fx)
    total_options = 1
    # stores the effect input values
    option_value = None

    # grayscale panel
    if panel_id == FX_GRAYSCALE:
        option_value = rgb_sliders("Color Weights", False)
    # change color panel
    elif panel_id == FX_CHANGECOLOR:
        total_options = 3
        if EditorStore.current_fx_options == 0:
            option_value = rgb_sliders("Color Comparator", True)
        elif EditorStore.current_fx_options == 1:
            fx_panel_header("Color Tolerance")
            option_value = draw_slider(0, "Amount")
        elif EditorStore.current_fx_options == 2:
            option_value = rgb_sliders("Replacement colour", True)
    # posterize panel
    elif panel_id == FX_POSTER:
        option_value = rgb_sliders(
            "New Color Ratio", False,
            ("lower value", "mid value", "higher value")
        )
    # posterize by color distance panel
    elif panel_id == FX_POSTER_DIST:
        total_options = 6
        if EditorStore.current_fx_options == 0:
            option_value = rgb_sliders("Color Comparator", True)
        elif EditorStore.current_fx_options == 1:
            option_value = rgb_sliders("Color Replacement One", True)
        elif EditorStore.current_fx_options == 2:
            fx_panel_header("Color Tolerance One")
            option_value = draw_slider(0, "Amount", 0, 1)
        elif EditorStore.current_fx_options == 3:
            option_value = rgb_sliders("Color Replacement Two", True)
        elif EditorStore.current_fx_options == 4:
            fx_panel_header("Color Tolerance Two")
            option_value = draw_slider(0, "Amount", effect_input_values[2], 1)
        elif EditorStore.current_fx_options == 5:
            option_value = rgb_sliders("Color Replacement Three", True)
    # tint image color panel
    elif panel_id == FX_TINT:
        total_options = 3
        if EditorStore.current_fx_options == 0:
            option_value = rgb_sliders("Color Weights", False)
        elif EditorStore.current_fx_options == 1:
            fx_panel_header("Tones")
            option_value = [0, 0]
            option_value[0] = draw_slider(0, "shadows")
            option_value[1] = draw_slider(1, "mid tones")
        elif EditorStore.current_fx_options == 2:
            fx_panel_header("Base Color")
            # todo add base colors
    # blur panel
    elif panel_id == FX_BLUR:
        fx_panel_header("Blend Tolerance")
        option_value = draw_slider(0, "Amount")
    # set alpha by color distance panel
    elif panel_id == FX_SETALPHA_DIST:
        total_options = 3
        if EditorStore.current_fx_options == 0:
            option_value = rgb_sliders("Color Comparator", True)
        elif EditorStore.current_fx_options == 1:
            fx_panel_header("Tolerance")
            option_value = draw_slider(0, "Amount")
        elif EditorStore.current_fx_options == 2:
            fx_panel_header("New Alpha")
            option_value = draw_slider(0, "Amount")

    # add appropriate text to the apply button
    button_position = 1025, 500
    if total_options - (EditorStore.current_fx_options + 1) <= 0:
        fx_button = label_button(
            button_fx.draw_button(
                pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                button_position
            ),
            "Apply FX", sub_header_fontface, 15, 15
        )
    else:
        fx_button = label_button(
            button_fx.draw_button(
                pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                button_position
            ),
            "Next", sub_header_fontface, 15, 15
        )

    if panel_id > -1:

        # display the action (next/apply) button if in a valid panel
        screen.blit(fx_button, button_position)
        if button_fx.is_pressed(
                pygame.mouse.get_pos(), button_position,
                library.KEY_PRESSED["mouse"]
        ) and not EditorStore.next_options_pressed:

            # add the effect input to the list
            effect_input_values.append(option_value)

            # run fx if apply button is pressed and reset the selected FX
            if total_options - (EditorStore.current_fx_options + 1) <= 0:
                run_effect(panel_id)
                # reset the panels
                EditorStore.selected_fx_id = -1
                EditorStore.current_fx_options = -1

            # increase the current menu
            EditorStore.current_fx_options += 1
            # prevent the button being pressed a second time
            EditorStore.next_options_pressed = True
            # reset the slider value on panel change
            reset_slider_values()
        elif not button_fx.is_pressed(

                pygame.mouse.get_pos(), button_position,
                library.KEY_PRESSED["mouse"]
        ) and not library.KEY_PRESSED["mouse"]:

            # enable the action button
            EditorStore.next_options_pressed = False


def rgb_sliders(header, display_color_box, label=("Red", "Green", "Blue")):
    """
    Draw the RGB sliders.

    :param header:              pannel header.
    :param display_color_box:   should the color preview be displayed.
    :param label:               slider labels=("red, "green", "blue").
    :return:                    color (r, g, b).
    """
    # display panel header as rgb is a single panel
    fx_panel_header(header)

    # red slider
    screen.blit(
        get_label(
            label[0], text_fontface, (75, 30), library.BLACK, library.WHITE
        ), (950, 125)
    )
    sliders_r.draw_slider(
        pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen
    )

    screen.blit(
        get_label(
            str(sliders_r.value), text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (1200, 160)
    )

    # green slider
    screen.blit(
        get_label(
            label[1], text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (950, 225)
    )
    sliders_g.draw_slider(
        pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen
    )
    screen.blit(
        get_label(
            str(sliders_g.value), text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (1200, 260)
    )

    # blue slider
    screen.blit(
        get_label(
            label[2], text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (950, 325)
    )
    sliders_b.draw_slider(
        pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen
    )
    screen.blit(
        get_label(
            str(sliders_b.value), text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (1200, 360)
    )

    if display_color_box:
        screen.blit(
            get_label(
                "Colour", text_fontface, (75, 30),
                library.BLACK, library.WHITE
            ), (1050, 415)
        )
        pygame.draw.rect(
            screen, (int(sliders_r.value * 255), int(sliders_g.value * 255),
                     int(sliders_b.value * 255)), (1065, 445, 50, 50)
        )

    return sliders_r.value, sliders_g.value, sliders_b.value


def draw_slider(slider_id, label, min_value=0, max_value=1):
    """
    Draw a slider from the slider list.

    :param slider_id:   slider list id.
    :param label:       slider label.
    :param min_value:   min value=0.
    :param max_value:   max value=1.
    :return:            slider value -> int.
    """
    screen.blit(
        get_label(
            label, text_fontface, (100, 30), library.BLACK, library.WHITE
        ), (950, 125 + (100 * slider_id))
    )
    sliders[slider_id].draw_slider(
        pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen
    )

    slider_min_max_value = min_value + (
            (max_value-min_value)*sliders[slider_id].value
    )

    screen.blit(
        get_label(
            str(slider_min_max_value), text_fontface, (75, 30),
            library.BLACK, library.WHITE
        ), (1200, 160+(100*slider_id))
    )

    return slider_min_max_value


def reset_slider_values():
    """Reset all the slider values to the default 0.5."""
    sliders_r.set_value(0.5)
    sliders_g.set_value(0.5)
    sliders_b.set_value(0.5)

    for slider in sliders:
        slider.set_value(0.5)


def fx_panel_header(header):
    """Display the fx panel header."""
    screen.blit(
        get_label(
            header, sub_header_fontface, (250, 50),
            library.BLACK, library.WHITE
        ), (950, 55)
    )


def label_button(button_surface, text, fontface, x_position, y_position):
    """
    Add labels to buttons.

    :param button_surface:  Button template to copy.
    :param text:            Test to display on button.
    :param fontface:        Font face to use.
    :param x_position:      X position.
    :param y_position:      Y position.
    :return:                New button image.
    """
    # copy the button surface so it can be re-used
    temp_surface = button_surface.copy()
    temp_surface.blit(
        fontface.render(
            text, True, library.BLACK
        ), (x_position, y_position)
    )

    return temp_surface


def get_label(text, fontface, size,
              text_color=(0, 0, 0, 255), background_color=(255, 255, 255, 0)):
    """
    Create a text label.

    :param text:                Label text.
    :param fontface:            Fontface.
    :param text_color:          font color (r, g, b, a).
    :param background_color:    background color (r, g, b, a).
    :param size:                label size (x, y).
    :return:                    label surface.
    """
    label_surface = pygame.Surface(size, pygame.SRCALPHA)
    label_surface.fill(background_color)
    label_surface.blit(fontface.render(text, True, text_color), (5, 5))

    return label_surface


def draw_menu_buttons():
    """Draw buttons for the current menu."""
    # loop button for the current menu
    for bt in list(button_type):
        for b in EditorStore.current_menu_buttons:
            # skip if this is not the correct button time
            if bt != b[4]:
                continue
            # draw buttons
            screen.blit(
                label_button(
                    button_type[bt].draw_button(
                        pygame.mouse.get_pos(),
                        library.KEY_PRESSED["mouse"], b[1]
                    ), b[0], get_button_type_fontface(bt), b[2], 15
                ), b[1]
            )


def get_button_type_fontface(button_type_name):
    """
    Get the font face for a button type.

    :param button_type_name:    type of button.
    :return:                    fontface for button type.
    """
    # __Add_new__
    # Add font face for button types to if statement
    if button_type_name == "fx":
        return text_fontface
    else:
        return sub_header_fontface


def button_pressed():
    """Find if any buttons are pressed in the current menu."""
    # tile select buttons are in display_select_tile_button()

    # loop events to look for mouse up on button 1
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            quit()
        elif event.type == KEYUP:
            # text box input
            EditorStore.save_file_name_input = text_input(
                event, EditorStore.save_file_name_input, save_text_input
            )
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            library.KEY_PRESSED["mouse"] = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            # loop buttons to find if any are pressed
            for bt in list(button_type):
                for b in EditorStore.current_menu_buttons:
                    # skip if this is not the correct button time
                    if bt != b[4]:
                        continue
                    if button_type[bt].is_pressed(
                            pygame.mouse.get_pos(), b[1],
                            library.KEY_PRESSED["mouse"]
                    ):
                        # run the button action
                        button_action(b[3], b)

            # un-set the mouse press
            library.KEY_PRESSED["mouse"] = False


def button_action(action_type, button_data=None):
    """Run the pressed buttons action."""
    # __Add_new__
    # Add new button actions to if statement
    if action_type == "return":
        # return to main menu if we are on the editor start menu
        # else return to start menu
        if EditorStore.current_menu == MENU_START:
            # just quit if in standalone mode
            if standalone_mode:
                quit()
            # un-set the editor
            EditorStore.game_state.set_state("main menu")
            # Set buttons back to start menu so
            # if we return to editor its good to go.
            EditorStore.current_menu_buttons = start_menu_button_data
        elif EditorStore.current_menu == MENU_EDIT:
            # when going back to the select image
            # menu force the button directory to the current directory
            button_data = list(button_data)
            if len(button_data) < 6:
                button_data.append(EditorStore.current_directory)
            else:
                button_data[5] = EditorStore.current_directory
            # set to update the file list
            EditorStore.update_image_directory = True
            button_action("tile_select", button_data)
        else:
            set_menu(MENU_START, start_menu_button_data)
    elif action_type == "tile_select":
        # set tile select menu + buttons
        set_menu(MENU_SELECT, tile_select_menu_button_data)
        # Set floor tile diectory
        set_directory(button_data[5])
    elif action_type == "edit_tile":
        # set edit tile menu + buttons
        set_menu(MENU_EDIT, edit_tile_button_data)
    elif action_type == "+_zoom":
        if EditorStore.tile_zoom < 5:
            EditorStore.tile_zoom += 0.25
    elif action_type == "-_zoom":
        if EditorStore.tile_zoom > 0.5:
            EditorStore.tile_zoom -= 0.25
    elif action_type == "select_effect":
        EditorStore.selected_fx_id = button_data[5]
        # clear effect input values as we are change effect panel
        # and reset the current panel id
        effect_input_values.clear()
        EditorStore.current_fx_options = 0
        # make shore all the sliders are at default value
        reset_slider_values()
    elif action_type == "save":
        save_tile(
            EditorStore.edit_tile, EditorStore.current_directory,
            EditorStore.save_file_name_input
        )
        EditorStore.save_file_name_input = ""
    elif action_type == "scroll_images_+":
        EditorStore.select_tile_start_position += 1
    elif action_type == "scroll_images_-":
        EditorStore.select_tile_start_position -= 1
    else:
        print("Error button action", action_type, "not found")


def set_menu(menu_id, buttons=None):
    """
    Set the current menu.

    :param menu_id:     menu id to set to.
    :param buttons:     the menus buttons (if none button remain the same).
    :return:            None.
    """
    EditorStore.current_menu = menu_id
    if buttons is not None:
        EditorStore.current_menu_buttons = buttons


def run_effect(effect_id):
    """Call the effect in image_effects."""
    # and sorts the effect input data out
    # effect data in inputted into the effect_input_data in the order of the
    # effects option panel

    effect_inputs = None

    if effect_id == FX_GRAYSCALE:
        # extract the color weights
        effect_inputs = effect_input_values[0]
        effect_id = "greyscale"
    elif effect_id == FX_CHANGECOLOR:
        effect_inputs = effect_input_values
        effect_id = "change_color"
    elif effect_id == FX_POSTER:
        # extract the color amounts
        effect_inputs = effect_input_values[0]
        effect_id = "poster"
    elif effect_id == FX_POSTER_DIST:
        effect_inputs = list()
        # extract the replacement colors
        effect_inputs.append((
            effect_input_values[1], effect_input_values[3],
            effect_input_values[5]
        ))
        # extract the color_comparator
        effect_inputs.append(effect_input_values[0])
        # extract the tolerance
        effect_inputs.append((effect_input_values[2], effect_input_values[4]))
        effect_id = "poster_dist"
    elif effect_id == FX_TINT:
        effect_inputs = effect_input_values
        effect_id = "tint"
    elif effect_id == FX_BLUR:
        # extract tolerance
        effect_inputs = effect_input_values[0]
        effect_id = "blur"
    elif effect_id == FX_SETALPHA_DIST:
        effect_inputs = effect_input_values
        effect_id = "set_alpha_dist"
    else:
        # display error message if effect is not found
        print("[tileEditor.run_effect] Error: effect not found ", effect_id)

    image_effects.run_effect(
        effect_id, EditorStore.edit_tile, effect_inputs,
        (library.loading_bar, screen, (0, 0, WINDOW_WIDTH, 50)
         )
    )

    # Clear the effect value list ready for the next fx to be applied
    effect_input_values.clear()


def resize_preview_image(preview_image):
    """
    Get the size of an image when shrunk to TILE_SIZE.

    Keep the aspect ratio.
    :param preview_image:   surface size (width, height).
    :return:                new resized surface size.
    """
    image_size = preview_image.get_size()

    if image_size[0] >= image_size[1]:
        multiplier = TILE_SIZE / image_size[0]
    else:
        multiplier = TILE_SIZE / image_size[1]

    return pygame.transform.scale(
        preview_image, (int(image_size[0] * multiplier),
                        int(image_size[1] * multiplier)
                        )
    )


def set_directory(directory):
    """Set the directory."""
    EditorStore.current_directory = directory
    EditorStore.update_image_directory = True


def text_input(event, current_text, ui_text_input):
    """Get text input event."""
    if not ui_text_input.has_focus(
            pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (50, 100)
    ):
        return current_text

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    if event.key == K_BACKSPACE:
        new_str = ""
        for s in range(0, len(current_text)-1):
            new_str += current_text[s]
        return new_str
    elif event.key == K_SPACE:
        return current_text + " "

    # numbers
    if event.key >= 48 < 48 + len(numbers):
        for n in range(len(numbers)):
            if event.key == 48 + n:
                return current_text + numbers[n]

    # letters
    if event.key >= 97 < 97 + len(letters):
        for l in range(len(letters)):
            if event.key == 97 + l:
                return current_text + letters[l]

    return current_text


def display():
    """
    Main Editor Loop.

    Driver: Ashley Sands, Navigator: N/A.
    """
    # initialize the editor
    if not EditorStore.initialized:
        initialize()
        # prevent from initializing again
        EditorStore.initialized = True

    screen.fill(library.BLACK)
    pygame.draw.rect(screen, library.LIGHT_GREY,
                     [WINDOW_MARGIN_X, WINDOW_MARGIN_Y,
                      WINDOW_WIDTH - (WINDOW_MARGIN_X * 2),
                      WINDOW_HEIGHT - (WINDOW_MARGIN_Y * 2)])

    pygame.draw.rect(screen, library.WHITE, [90, 65, 285, 100])
    screen.blit(header_text_surface, (100, 75))
    screen.blit(sub_headers[EditorStore.current_menu], (130, 120))

    if EditorStore.current_menu == MENU_SELECT:
        display_select_tile()
    elif EditorStore.current_menu == MENU_EDIT:
        display_tile_editor()

    draw_menu_buttons()
    button_pressed()

    pygame.display.flip()


def save_tile(surface, path, file_name):
    """Save the image as a png."""
    # todo check if file already exist
    if len(file_name) == 0:
        print("Error: Unable to save no file name")
        return

    path = path + "/" + file_name + ".png"
    pygame.image.save(surface, path)
    print("Image save to ", path)


def standalone():
    """Run the editor as a standalone."""
    while True:
        display()


def quit():
    """Quit Editor."""
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    standalone()
