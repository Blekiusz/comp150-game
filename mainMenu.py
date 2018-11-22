import menuUi
import library
import dungeonGenerator as dunGen


class Menu:

    exit_funct = None
    menu_state = None
    menu_ui = None
    game_state = None

    def set_functions_by_name(self, name, funct):
        print(name)
        if name == "exit":
            self.exit_funct = funct
        elif name == "game state":
            self.game_state = funct
        elif name == "menu_state":
            self.menu_state = funct

    # button functions
    def test_button_function(self):
        print("Buttons Pressed")

    def back_action(self):
        self.menu_state.set_state("main menu")
        self.menu_ui.set_current_menu("Main Menu")

    def start_game_action(self):
        if library.HAD_FIRST_RUN:
            dunGen.reset(True)

        library.HAD_FIRST_RUN = True
        self.game_state.set_state("game")

    def controls_action(self):
        self.menu_state.set_state("Controls")
        self.menu_ui.set_current_menu("Controls")

    def initialize_menu(self):
        # define buttons
        menu_ui = menuUi.UiMenu()
        self.menu_ui = menu_ui

        menu_ui.add_button_type("default", None, None, None, (450, 50))
        menu_ui.add_button_type("back", None, None, None, (200, 50))


        menu_ui.add_menu("Main Menu")
        menu_ui.add_button("Main Menu", "default", "Start Game", (150, 250), self.start_game_action)
        menu_ui.add_button("Main Menu", "default", "Controls", (150, 350), self.controls_action)
        menu_ui.add_button("Main Menu", "default", "Quit", (150, 450), self.exit_funct)

        menu_ui.add_menu("Controls")
        menu_ui.add_button("Controls", "back", "Back", (75, 500), self.back_action)


        # set the menu to the default menu
        menu_ui.set_current_menu("Main Menu")

        return menu_ui
