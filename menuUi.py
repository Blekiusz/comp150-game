"""MENU UI."""
import pygame
import UI


class UiMenu:
    """
    Create a set of menus controlled by a state.

    Driver: Ashley.
    """

    active = False      # needed??
    current_menu = None
    # default fontfaces. use set_font_face to change.
    header_fontface = None
    button_fontface = None
    menus = {}
    buttons = {}

    HEADER_Y_POSITION = -40
    HEADER_X_OFFSET = -237
    HEADER_SIZE = (1100, 300)

    def __init__(self):
        """Initialize the fontfaces."""
        self.header_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 105)
        self.button_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 50)

    def set_font_face(self, header_fontface, button_fontface):
        """Set the fontface, params are ignored if None."""
        if header_fontface is not None:
            self.header_fontface = header_fontface

        if button_fontface is not None:
            self.button_fontface = button_fontface

    def add_button_type(self, type_name,  normal, hover, pressed, size):
        """
        Add a new button type.

        :param type_name:       the button type/group name
        :param normal:          src to normal button image  (can be none)
        :param hover:           src to hover button image   (can be none)
        :param pressed:         src to pressed button image (can be none)
        :param size:            button size (width, height)
        :return:                None
        """
        self.buttons[type_name] = UI.UIButtons(hover, normal, pressed, size)

    def add_menu(self, menu_title):
        """Add a new menu to list of menus."""
        self.menus[menu_title] = []

    def add_button(self, menu_title, button_type,
                   button_label, position_rect, action_funct):
        """
        Add a button to a menu group.

        :param menu_title:      name of the group to add a button to
        :param button_type:     name of the button type to use
        :param button_label:    the label to display on the button.
        :param position_rect:   position and size rect -> (x, y)
        :param action_funct:    the function with the button action
        :return:                None
        """
        self.menus[menu_title].append(
            [button_type, button_label, position_rect, action_funct]
        )

    def set_current_menu(self, menu_name):
        """Set the menu to be displayed."""
        self.current_menu = menu_name

    @staticmethod
    def center_surface(hold_surface_size, inner_surface_size):
        """
        Get the position to center the inner surface inside the hold surface.

        :param hold_surface_size: Size of the surface holding the inner surface
        :param inner_surface_size: size of the inner surface
        :return: x, y offset to center center inner surface
        """
        offset_x = (hold_surface_size[0] - inner_surface_size[0]) // 2
        offset_y = (hold_surface_size[1] - inner_surface_size[1]) // 2

        return offset_x, offset_y

    def get_button(self, button, label, fontface, font_color=(0, 0, 0)):
        """Get the button to be displayed with a label prefixed."""
        temp_surface = button.copy()
        text_surface = fontface.render(label, True, font_color)

        # draw the text to the center of the button.
        offset_x, offset_y = self.center_surface(
            temp_surface.get_size(), text_surface.get_size()
        )
        temp_surface.blit(text_surface, (offset_x, offset_y))

        return temp_surface

    def get_header(self, label, fontface, label_size,
                   font_color=(140, 140, 140, 103),
                   background_color=(132, 249, 230, 0)
                   ):
        """Get the menu header."""
        temp_surface = pygame.Surface(label_size, pygame.SRCALPHA)
        temp_surface.fill(background_color)
        text_surface = fontface.render(label, True, font_color)

        # draw the text to the center of the header label.
        offset_x, offset_y = self.center_surface(temp_surface.get_size(),
                                                 text_surface.get_size())
        temp_surface.blit(text_surface, (offset_x, offset_y))

        return temp_surface

    def draw_buttons(self, surface, mouse_pos, key_pressed, menu_title=None,
                     menu_name=None):
        """Draw all the buttons and menu header to the surface."""
        # note to self: button_type, button_label, position_rect, action_funct

        if menu_name is None:
            menu_name = self.current_menu

        if menu_title is None:
            menu_title = menu_name

        # display the header in the hoz center of the screen
        header_surface = self.get_header(menu_title,
                                         self.header_fontface,
                                         self.HEADER_SIZE)
        offset_x, offset_y = self.center_surface(surface.get_size(),
                                                 header_surface.get_size())

        offset_x += self.HEADER_X_OFFSET

        surface.blit(header_surface, (offset_x, self.HEADER_Y_POSITION))

        # display all the buttons for the current menu.
        for button in self.menus[menu_name]:
            surface.blit(
                self.get_button(
                    self.buttons[button[0]].draw_button(
                        mouse_pos, key_pressed, button[2]),
                    button[1], self.button_fontface),
                button[2]
            )

    def is_button_pressed(self, mouse_position, mouse_is_pressed,
                          menu_name=None):
        """Find if any of the buttons on the current menu are being pressed."""
        if menu_name is None:
            menu_name = self.current_menu

        # See if any of the buttons are being pressed on the current menu.
        for button in self.menus[menu_name]:
            if self.buttons[button[0]].is_pressed(mouse_position,
                                                  button[2], mouse_is_pressed
                                                  ):
                button[3]()
