"""PLAYER."""
import pyBehaviour
import library
import pygame
from animator import Animator


class Player(pyBehaviour.Transform):
    """Main player class."""

    previous_position = (0, 0)

    # Player Setup
    move_speed = 0
    idle = True
    current_direction = library.BACKWARDS

    blocked_move_direct = {
        "forwards": False,
        "right": False,
        "backwards": False,
        "left": False
    }

    # Game Components
    time_manager = None
    get_world_position_funct = None

    # Animation setup
    SPRITE_SPACING = 3          # px
    SPRITES_COUNT = 7           # Per Sheet
    UPDATE_LENGTH = 0.75        # sec
    UPDATE_LENGTH_IDLE = 1.5    # sec

    # Move animations
    animation = ["", "", "", ""]
    animation[library.LEFT] = Animator(
        "Characters/girl_sideLeft_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH
    )

    animation[library.RIGHT] = Animator(
        "Characters/girl_sideRight_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH
    )

    animation[library.FORWARDS] = Animator(
        "Characters/girl_back_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH
    )

    animation[library.BACKWARDS] = Animator(
        "Characters/girl_front_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH
    )

    # idle animations
    idle_animation = ["", "", "", ""]
    idle_animation[library.LEFT] = Animator(
        "Characters/girl_sideLeftIdle_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH_IDLE
    )

    idle_animation[library.RIGHT] = Animator(
        "Characters/girl_sideRightIdle_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH_IDLE
    )

    idle_animation[library.FORWARDS] = Animator(
        "Characters/girl_backIdle_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH_IDLE
    )

    idle_animation[library.BACKWARDS] = Animator(
        "Characters/girl_frontIdle_spriteSheet.png",
        library.scaleNum,
        SPRITE_SPACING,
        SPRITES_COUNT,
        UPDATE_LENGTH_IDLE
    )

    def __init__(self, move_speed, scale, time_manager):
        """Initialize."""
        self.move_speed = move_speed
        self.scale = scale
        self.time_manager = time_manager
        self.get_world_position_funct = None

    def block_move_direction(self, forwards, right, backwards, left):
        """Block movement based on the passed directions."""
        self.blocked_move_direct["forwards"] = forwards
        self.blocked_move_direct["right"] = right
        self.blocked_move_direct["backwards"] = backwards
        self.blocked_move_direct["left"] = left

    def change_direction(self, last_dir, current_dir):
        """
        Reset the players animator if the direction changes.

        :param last_dir:        players direction from last frame
        :param current_dir:     players direction this frame
        :return:                current direction
        """
        if last_dir != current_dir:
            self.animation[last_dir].reset()
        return current_dir

    @staticmethod
    def animation_direction(last_direction, inputs):
        """
        Get the next animation direction.

        this prevents it from resetting
        if two keys are pressed at the same time!
        :param last_direction:  players last direction
        :param inputs:          user inputs.
        :return:                (Direction, idle)
        """
        # find if no keys are pressed and set it to idle
        idle = not inputs["left"] and not \
            inputs["right"] and not \
            inputs["forwards"] and not \
            inputs["backwards"]

        # if there's no keys pressed return early as there's nothing to test
        if idle:
            return last_direction, idle

        # set direction to last direction
        # in case there is opposite keys being pressed
        direction = last_direction

        # set to idle if both left and right keys are pressed
        if inputs["left"] and inputs["right"]:
            idle = True
        elif inputs["left"]:  # set left direction
            direction = library.LEFT
        elif inputs["right"]:  # set right direction
            direction = library.RIGHT

        # do forwards and backwards in separate if
        # as the animation trumps left and right
        # set to idle if both forwards and backwards keys are pressed
        if inputs["forwards"] and inputs["backwards"]:
            # set to idle if neither left or right is pressed
            idle = not inputs["left"] and not \
                inputs["right"]
        elif inputs["forwards"]:
            direction = library.FORWARDS  # set forwards direction
            idle = False
        elif inputs["backwards"]:
            direction = library.BACKWARDS  # set backwards direction
            idle = False

        return direction, idle

    def update(self, inputs):
        """Update."""
        self.previous_position = self.position

        next_animation_direction, self.idle = self.animation_direction(
            self.current_direction,
            inputs
        )

        self.current_direction = self.change_direction(
            self.current_direction,
            next_animation_direction
        )

        pyBehaviour.Transform.update(self, inputs)

    '''
            if self.current_direction == library.FORWARDS:
                self.forwards()
            elif self.current_direction == library.RIGHT:
                self.right()
            elif self.current_direction == library.BACKWARDS:
                self.backwards()
            elif self.current_direction == library.LEFT:
                self.left()
    '''
    # Key Actions (up, down, left, right)

    def forwards(self):
        """Up key action."""
        if self.blocked_move_direct["forwards"]:
            return

        self.position[1] -= self.time_manager.delta_time * self.move_speed

    def right(self):
        """Right key action."""
        if self.blocked_move_direct["right"]:
            return

        self.position[0] += self.time_manager.delta_time * self.move_speed

    def backwards(self):
        """Down key action."""
        if self.blocked_move_direct["backwards"]:
            return

        self.position[1] += self.time_manager.delta_time * self.move_speed

    def left(self):
        """Left key action."""
        if self.blocked_move_direct["left"]:
            return

        self.position[0] -= self.time_manager.delta_time * self.move_speed

    def draw(self, tile_size, surface):
        """Draw the player."""
        if self.idle:
            current_animation = self.idle_animation[self.current_direction]
        else:
            current_animation = self.animation[self.current_direction]

        current_animation.update_time(self.time_manager.delta_time)

        current_sprite = current_animation.get_current_sprite()
        # resize the object by scale
        current_sprite = pygame.transform.scale(
            current_sprite,
            (int(tile_size * self.scale[0]), int(tile_size * self.scale[1]))
        )

        pos_x, pos_y = self.get_world_position_funct(
            self.position[0],
            self.position[1]
        )

        surface.blit(current_sprite, (pos_x, pos_y))
