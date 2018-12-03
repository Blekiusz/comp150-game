"""BEHAVIOURS."""


class PyBehaviour:
    """Main behaviour class."""

    def update(self, inputs):
        """Update PyBehaviour.

        :param inputs: user inputs
        """
        if inputs["forwards"]:
            self.forwards()

        if inputs["right"]:
            self.right()

        if inputs["backwards"]:
            self.backwards()

        if inputs["left"]:
            self.left()

    def forwards(self):
        """Forwards."""
        pass

    def right(self):
        """Right."""
        pass

    def backwards(self):
        """Backwards."""
        pass

    def left(self):
        """Left."""
        pass


class Transform(PyBehaviour):
    """Transform behaviour class."""

    position = [0, 0]
    rotation = 0
    scale = [0, 0]
