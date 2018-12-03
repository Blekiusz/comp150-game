"""MAIN MENU."""
import menuUi
import library
import dungeonGenerator as dunGen


class Menu:
    """The main menu class."""

    exit_funct = None
    menu_state = None
    menu_ui = None
    game_state = None

    def set_functions_by_name(self, name, funct):
        """Set a function by name."""
        print(name)
        if name == "exit":
            self.exit_funct = funct
        elif name == "game state":
            self.game_state = funct
        elif name == "menu_state":
            self.menu_state = funct

    def return_to_menu_action(self):
        """Return to menu."""
        self.game_state.set_state(self.game_state.get_state())
        self.menu_state.set_state(self.game_state.get_state())
        self.menu_ui.set_current_menu(self.game_state.get_state())

    def return_to_main_menu_action(self):
        """Return to main menu."""
        self.game_state.set_state("main menu")
        self.menu_state.set_state("main menu")
        self.menu_ui.set_current_menu("main menu")

    def resume_game_action(self):
        """Resume the game."""
        self.game_state.set_state("game")

    def start_game_action(self):
        """Start the game."""
        if library.HAD_FIRST_RUN:
            dunGen.DungeonGenerator.reset(dunGen.DungeonGenerator, True, True)

        library.HAD_FIRST_RUN = True
        self.game_state.set_state("game")

    def tile_editor_action(self):
        """Open the tile editor."""
        self.game_state.set_state("editor")

    def controls_action(self):
        """Open the controls menu."""
        self.menu_state.set_state("Controls")
        self.menu_ui.set_current_menu("Controls")

    def initialize_menu(self):
        """Initialize the menu."""
        # define buttons
        menu_ui = menuUi.UiMenu()
        self.menu_ui = menu_ui

        menu_ui.add_button_type("default", None, None, None, (450, 50))
        menu_ui.add_button_type("back", None, None, None, (200, 50))

        menu_ui.add_menu("Game Over")
        menu_ui.add_button("Game Over", "default", "Restart", (150, 288),
                           self.start_game_action)
        menu_ui.add_button("Game Over", "default", "Exit To Menu", (150, 399),
                           self.return_to_main_menu_action)
        menu_ui.add_button("Game Over", "default", "Quit", (150, 488),
                           self.exit_funct)

        menu_ui.add_menu("paused")
        menu_ui.add_button("paused", "default", "Resume", (150, 228),
                           self.resume_game_action)
        menu_ui.add_button("paused", "default", "Restart", (150, 328),
                           self.start_game_action)
        menu_ui.add_button("paused", "default", "Controls", (150, 428),
                           self.controls_action)
        menu_ui.add_button("paused", "default", "Exit To Menu", (150, 528),
                           self.return_to_main_menu_action)
        menu_ui.add_button("paused", "default", "Quit", (150, 628),
                           self.exit_funct)

        menu_ui.add_menu("main menu")
        menu_ui.add_button("main menu", "default", "Start Game", (150, 250),
                           self.start_game_action)
        menu_ui.add_button("main menu", "default", "Tile Editor", (150, 350),
                           self.tile_editor_action)
        menu_ui.add_button("main menu", "default", "Controls", (150, 450),
                           self.controls_action)
        menu_ui.add_button("main menu", "default", "Quit", (150, 550),
                           self.exit_funct)

        menu_ui.add_menu("Controls")
        menu_ui.add_button("Controls", "back", "Back", (75, 500),
                           self.return_to_menu_action)

        # set the menu to the default menu
        menu_ui.set_current_menu("main menu")

        return menu_ui
