"""USER INTERFACE."""
import pygame
import library


class UIButtons:
    """
    UI Button Class.

    # Driver: Callum; Navigator: Ashley
    # Edited: Ashley
    """

    button_hover = None
    button_normal = None
    button_pressed = None

    button_size = (0, 0)

    def __init__(self, button_hover_src, button_normal_src,
                 button_pressed_src, size):
        """
        Button sources can be none.

        This can be useful if you want to set
        the value to an image that is already a surface. Beware if it is
        none it will cause an error if you try to blit it to screen!
        :param button_hover_src:    File path for hover button
        (can be none)
        :param button_normal_src:   File path for normal button
        (can be none)
        :param button_pressed_src:  File path for pressed button
        (can be none)
        :param size:                The size of the button
        (width, height)
        """
        self.button_size = size
        self.button_hover = self.set_button_image(
            button_hover_src, size, library.LIGHT_GREY
        )
        self.button_normal = self.set_button_image(
            button_normal_src, size, library.GREY
        )
        self.button_pressed = self.set_button_image(
            button_pressed_src, size, library.DARK_GREY
        )

    def set_button_image(self, image_src, size, color):
        """
        Set the button to image.

        if there is no image it gets set to a white surface.
        :param image_src:   image source
        :param size:        Size of button
        :param color:       color to set button to if there is no src
        :return:            button surface
        """
        # set to white surface if None is passed to image_src
        if image_src is None:
            temp_surface = pygame.Surface(size)
            temp_surface.fill(color)
            return temp_surface
        else:
            return pygame.transform.scale(
                pygame.image.load(image_src), size
            )

    def is_hover(self, cursor_pos, screen_pos):
        """Find if the cursor is over the button."""
        top_left = (cursor_pos[0] > screen_pos[0] and
                    cursor_pos[1] > screen_pos[1])
        bottom_right = cursor_pos[0] < (
                screen_pos[0] + self.button_size[0]
        ) and cursor_pos[1] < (screen_pos[1] + self.button_size[1])

        return top_left and bottom_right

    def is_pressed(self, cursor_pos, screen_pos, button_click):
        """Find if the user has pressed the button."""
        return self.is_hover(cursor_pos, screen_pos) and button_click

    def draw_button(self, cursor_pos, button_click, screen_pos):
        """Draw the button."""
        if self.is_pressed(cursor_pos, screen_pos, button_click):
            return self.button_pressed
        elif self.is_hover(cursor_pos, screen_pos):
            return self.button_hover
        else:
            return self.button_normal


class UISlider(UIButtons):
    """
    UI slider class.

    # Driver: Callum; Navigator: Ashley
    # Edited: Ashley
    """

    slider_handle = None
    handle_position = [0, 0]

    slider_width = 100
    slider_pos = [0, 0]
    value = 0  # value = 0 - 1

    def __init__(self, button_hover_src, button_normal_src,
                 button_pressed_src, slider_bar_src, slider_size,
                 handle_width, slider_pos, start_value=0.5):
        """
        Initialize.

        :param button_hover_src:        hover image source
        :param button_normal_src:       normal image source
        :param button_pressed_src:      pressed image source
        :param slider_bar_src:          slider bar src
        :param slider_size:             size of slider -> (x, y)
        :param handle_width:            with of handle
        :param slider_pos:              slider screen pos
        :param start_value:             start value
        """
        UIButtons.__init__(self, slider_bar_src, slider_bar_src,
                           slider_bar_src, slider_size)
        self.slider_handle = pygame.transform.scale(
            (pygame.image.load(button_normal_src)),
            (handle_width, slider_size[1])
        )
        self.slider_pos = slider_pos
        self.slider_width = slider_size[0]
        self.handle_position = [slider_pos[0] + (slider_size[0] * start_value),
                                slider_pos[1]]
        self.value = start_value

    def set_value(self, value):
        """Set the value and puts the handle into position."""
        self.value = value
        self.handle_position[0] = (self.slider_pos[0] +
                                   (self.slider_width * value))

    def draw_slider(self, cursor_pos, button_click, surface):
        """Draw the slider to surface."""
        if self.is_pressed(cursor_pos, self.slider_pos, button_click):
            self.handle_position = list(cursor_pos)
            self.handle_position[0] -= 8
            self.handle_position[1] = self.slider_pos[1]
            self.value = (
                    (self.handle_position[0] - self.slider_pos[0]) /
                    (self.slider_width - self.slider_handle.get_width())
            )
            self.value = library.clamp(0, 1, self.value)

        surface.blit(
            self.draw_button(
                cursor_pos, button_click, self.slider_pos
            ), self.slider_pos
        )
        surface.blit(self.slider_handle, self.handle_position)

        return self.value


class UIInput(UIButtons):
    """
    UI Text input class.

    # Driver: Ashley; Navigator: None
    """

    focus = False
    fontface = None
    input_size = [0, 0]
    input_surface = None
    font_size = 15

    def __init__(self, input_size, font_size):
        """
        Initialize.

        :param input_size:      size of text input (x, y)
        :param font_size:       font size
        """
        input_surface = pygame.Surface(input_size)
        self.input_surface = pygame.Surface(input_size)
        pygame.draw.rect(input_surface, library.BLACK,
                         (0, 0, input_size[0], input_size[1])
                         )
        pygame.draw.rect(input_surface, library.WHITE,
                         (5, 5, (input_size[0]-10), (input_size[1]-10))
                         )

        UIButtons.__init__(self, None, None, None, input_size)
        UIButtons.button_normal = input_surface
        UIButtons.button_pressed = input_surface
        UIButtons.button_hover = input_surface
        self.fontface = pygame.font.Font("UI/AMS hand writing.ttf", font_size)
        self.input_size = list(input_size)
        self.font_size = font_size

    def has_focus(self, cursor_pos, button_click, screen_position):
        """Check if the text input has focus."""
        if button_click and not self.is_pressed(
                cursor_pos, screen_position, button_click):
            return False
        elif button_click and self.is_pressed(
                cursor_pos, screen_position, button_click):
            return True

        return self.focus

    def draw_text_input(self, cursor_pos, button_click,
                        screen_position, text, surface):
        """
        Draw text input to surface.

        :param cursor_pos:          cursor position
        :param button_click:        mouse button down
        :param screen_position:     screen position
        :param text:                text to display in text input
        :param surface:             surface to draw to
        :return:                    focus
        """
        self.focus = self.has_focus(cursor_pos, button_click, screen_position)

        self.input_surface.blit(
            self.draw_button(
                cursor_pos, button_click, screen_position
            ), (0, 0)
        )

        if self.focus:
            pygame.draw.rect(
                self.input_surface, library.BLACK, (
                    25 + (
                            (self.font_size/2) * (len(text)-1)
                    ), 5, 4, self.input_size[1]-16)
            )

        self.input_surface.blit(
            self.fontface.render(text, True, library.BLACK), (10, 10)
        )

        surface.blit(self.input_surface, screen_position)

        return self.focus


# Todo Test and doc.
class UIToggle(UIButtons):
    """UI Toggle class."""

    tick_image = None
    checked = False

    def __init__(self, button_hover_src, button_normal_src,
                 button_pressed_src, tick_src, size):
        """Initialize."""
        UIButtons.__init__(self, button_hover_src, button_normal_src,
                           button_pressed_src, size)

        # set the size of the tick to be 25% smaller than the button.
        toggle_size = (size[0]*0.75, size[1]*0.75)

        self.tick_image = self.set_button_image(tick_src, toggle_size,
                                                library.BLACK)

    def is_pressed(self, cursor_pos, screen_pos, button_click):
        """Check if the toggle has been pressed."""
        self.checked = not self.checked

        return UIButtons.is_pressed(self, cursor_pos, screen_pos, button_click)
