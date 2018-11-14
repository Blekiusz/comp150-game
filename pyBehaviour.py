
class PyBehaviour:

    def update(self, inputs):
        """Update PyBehaviour

        :param inputs: user inputs
        """
        
        if inputs["forwards"]:
            self.forwards()

        if inputs["right"]:
            self.right()

        if inputs["down"]:
            self.down()

        if inputs["left"]:
            self.left()

    def forwards(self):
        pass

    def right(self):
        pass

    def down(self):
        pass

    def left(self):
        pass