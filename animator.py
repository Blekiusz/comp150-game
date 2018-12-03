"""SPRITE SHEET ANIMATOR."""
import pygame


class Animator:
    """Stop-motion animator from sprite sheets."""

    # sprite sheet use for the animation
    animation_sheet = ""
    # size of the sprite within the sprite sheet (px)
    sprite_size = 45
    # space in-between sprites (px)
    sprite_spacing = 0
    # total sprite in sprite sheet
    sprites = 4
    # length of animation (seconds)
    animation_length = 1
    # length of a single frame in the animation (seconds)
    frame_length = animation_length / sprites
    # current frame id
    current_frame_id = 0
    # current time of the frame
    current_frame_time = 0

    def __init__(self, animation_sheet_src, size, spacing,
                 sprite_count, length):
        """
        Initialize the animator.

        Args
        :param animation_sheet_src:    Sprite directory
        :param size:                   size of the sprite
         to extract from the sprite sheet (px)
        :param spacing:                space in-between sprites
         in sprite sheet (px)
        :param sprite_count:            amount of sprites in sprite sheet
        :param length:                 total animation length (seconds)
        """
        # load the sprite sheet
        self.animation_sheet = pygame.image.load(animation_sheet_src)
        # set the extracted sprite size
        self.sprite_size = size
        # set the space in-between sprites
        self.sprite_spacing = spacing
        # set the amount of sprites in the sprite sheet
        self.sprites = sprite_count
        # set total animation length
        self.animation_length = length
        # set the frame length
        self.frame_length = length / sprite_count

    def update_time(self, delta_time):
        """
        Update the animator timer and current frame id.

        :param delta_time:      The amount of time that has passed
         since the last update
        """
        # update the frame time
        self.current_frame_time += delta_time

        # if the timer has exceeded or is equal to the frame length
        # increase the current frame id
        if self.current_frame_time >= self.frame_length:
            self.current_frame_id += 1
            # if the current frame is more than the amount of sprite
            # go back to the start
            if self.current_frame_id >= self.sprites:
                self.current_frame_id = 0

            # take the frame length away from the current frame time
            # to keep it as accurate as possible
            self.current_frame_time -= self.frame_length

    def reset(self):
        """Reset the animator back to its start state."""
        # reset the current frame id
        self.current_frame_id = 0
        # reset the current frame time.
        self.current_frame_time = 0

    def get_current_sprite(self):
        """Return the current sprite from the sprite sheet."""
        return self.animation_sheet.subsurface(((self.sprite_size *
                                                 self.current_frame_id) +
                                                (self.sprite_spacing *
                                                 self.current_frame_id),
                                                0, self.sprite_size,
                                                self.sprite_size))
