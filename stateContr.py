"""STATE CONTROLLER."""


class StateController:
    """Main state controller class."""

    current_state = None

    states = {}

    def __init__(self):
        """Initialize."""
        self.current_state = None
        self.states = {}

    def add_state(self, state_name, state_value):
        """Add a state to the list of states."""
        self.states[state_name] = state_value

    def set_state(self, state_name):
        """Set the current state."""
        self.current_state = state_name

    def get_state(self):
        """Return the current state."""
        return self.states[self.current_state]
