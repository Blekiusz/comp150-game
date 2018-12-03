"""TIME MANAGER."""


class TimeManager:
    """Main time manager class."""

    last_time = 0
    delta_time = 0

    def __init__(self, current_time):
        """Initialize."""
        self.time = current_time

    def update_time(self, current_time):
        """Update the current time."""
        self.delta_time = current_time - self.last_time
        self.last_time = current_time
