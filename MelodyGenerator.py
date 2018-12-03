"""
Tinkering audio contract 3 by Joachim Rayski.

Driver - Joachim Rayski
Navigator - None
"""

import pygame
import sys
import wave
import math
import struct
import random
import shutil
import os
from pygame.locals import *

pygame.init()
pygame.display.set_mode((250, 250), 0, 32)


class MusicGenerator:
    """Generate the procedural music track using sine waves."""

    current_track = 0

    # create the music folder
    if not os.path.exists("Music"):
        os.makedirs("Music")
    else:
        shutil.rmtree("Music")
        os.makedirs("Music")

    filename = "Music/melody"
    filetype = ".wav"

    D_MINOR_SCALE = {"D": 587.33, "E": 659.25,
                     "F": 698.46, "G": 783.99, "A": 880.00,
                     "Bflat": 932.33, "C": 1046.50}

    D_MINOR_CHORDS = {1: [D_MINOR_SCALE["A"],
                          D_MINOR_SCALE["F"],
                          D_MINOR_SCALE["D"]],

                      2: [D_MINOR_SCALE["Bflat"],
                          D_MINOR_SCALE["G"],
                          D_MINOR_SCALE["E"]],

                      3: [D_MINOR_SCALE["C"],
                          D_MINOR_SCALE["A"],
                          D_MINOR_SCALE["F"]],

                      4: [D_MINOR_SCALE["D"],
                          D_MINOR_SCALE["Bflat"],
                          D_MINOR_SCALE["G"]],

                      5: [D_MINOR_SCALE["E"],
                          D_MINOR_SCALE["C"],
                          D_MINOR_SCALE["A"]],

                      6: [D_MINOR_SCALE["F"],
                          D_MINOR_SCALE["D"],
                          D_MINOR_SCALE["Bflat"]],

                      7: [D_MINOR_SCALE["G"],
                          D_MINOR_SCALE["E"],
                          D_MINOR_SCALE["C"]]}

    current_chord = 1
    melody_frequency_1 = random.choice(D_MINOR_CHORDS[current_chord])
    melody_frequency_2 = random.choice(D_MINOR_CHORDS[current_chord]) * 2

    snare_frequency = 1
    hi_hat_frequency = 1

    currentProgress = 0

    currentNote = 2
    currentNote2 = 1

    multiplier = 6
    sample_rate = 44100
    songRate = sample_rate * multiplier

    volume = 0.1

    song_point = 0.1

    values = []

    def chord_progression(self, i):
        """
        Change the used chords when the song reaches a certain point.

        It then repeats the process creating a progression.
        :param i: current sample iteration
        :return:
        """
        if i >= self.songRate * self.song_point:
            self.song_point += 0.1
            if self.current_chord < len(self.D_MINOR_CHORDS.values()):
                self.current_chord += 2
            else:
                self.current_chord = 1

    def snare(self):
        """
        Generate a snare sound using noise and play it every 4th note.

        :return:
        """
        snare_speed = 20
        if self.currentNote == 4:
            self.snare_frequency = random.randint(100, 1000)
            if self.currentProgress == self.songRate / (snare_speed
                                                        * self.multiplier):
                self.snare_frequency = 1
                self.currentNote = 0

    def hi_hat(self):
        """
        Generate a hi-hat sound using noise and play it every note.

        :return:
        """
        hi_hat_speed = 150
        if self.currentNote2 == 1:
            self.hi_hat_frequency = random.randint(5000, 10000)
            if self.currentProgress == self.songRate / (hi_hat_speed
                                                        * self.multiplier):
                self.hi_hat_frequency = 1
                self.currentNote2 = 0

    def melody(self):
        """
        Generate a melody using the current chord notes.

        :return:
        """
        tempo = 6
        if self.currentProgress == self.songRate / (tempo * self.multiplier):

            self.melody_frequency_1 = random.choice(
                self.D_MINOR_CHORDS[self.current_chord])

            self.melody_frequency_2 = random.choice(
                self.D_MINOR_CHORDS[self.current_chord]) * 2

            self.currentNote += 1
            self.currentNote2 += 1
            self.currentProgress = 0

    def create_value(self, i, frequency, volume):
        """
        Create the sine wave value to write into the .wav file.

        :param i: current sample iteration
        :param frequency: frequency we want the sine wave to be
        :param volume: volume of the sound
        :return:
        """
        max_sample_value = 2**15 - 1
        sample_value = math.sin(
            2.0 * math.pi * frequency * (
                    i / float(self.sample_rate))) * (
                    volume * max_sample_value)
        return sample_value

    @staticmethod
    def square_wave(sine_wave):
        """Return values of a square wave."""
        if sine_wave > 0:
            return 1
        else:
            return -1

    def fade_out(self, i):
        """
        Lower the volume at the end of the song.

        :param i: current sample iteration
        :return:
        """
        if i >= self.songRate * 0.9:
            if self.volume > 0:
                self.volume -= 0.00005

    def fade_in(self):
        """
        Increase the volume at the start of the song.

        :return:
        """
        if self.volume <= 0.9:
            self.volume += 0.000005

    def generate_track(self):
        """
        Generate the music track.

        :return:
        """
        self.current_track += 1
        # Create the .wav file with all of it's parameters
        wav_write = wave.open(self.filename + str(self.current_track)
                              + self.filetype, 'w')
        wav_write.setparams((1, 2, self.sample_rate,
                             0, 'NONE', 'not compressed'))

        for i in range(0, self.songRate):
            self.currentProgress += 1

            # use the previous algorithms to create the track
            self.chord_progression(self, i)
            self.snare(self)
            self.hi_hat(self)
            self.melody(self)

            number_of_values = 5

            # create the sine wave values for each sound
            sample_value = self.create_value(self, i, self.melody_frequency_1,
                                             self.volume / number_of_values)
            sample_value2 = self.create_value(self, i, self.melody_frequency_2,
                                              self.volume / number_of_values)
            sample_value3 = self.create_value(self, i, self.snare_frequency,
                                              self.volume / number_of_values)
            sample_value4 = self.create_value(self, i, self.hi_hat_frequency,
                                              self.volume / number_of_values)

            square_wave_sample_value = sample_value * 2 * self.square_wave(
                sample_value) * 0.5

            # pack all of the values together
            packed_value = struct.pack('i', int(sample_value
                                                + sample_value2
                                                + sample_value3
                                                + sample_value4
                                                + square_wave_sample_value))

            # append the packed value into the values list
            for j in range(0, wav_write .getnchannels()):
                self.values.append(packed_value)

        # write the values list into the .wav files using a byte string
        value_str = b"".join(self.values)
        wav_write.writeframesraw(value_str)

        wav_write.close()
        self.values.clear()


def main():
    """
    Initialize the program and start the event loop.

    :return:
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                # delete the music folder
                if os.path.exists("Music"):
                    shutil.rmtree("Music")
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Generate and play the track
                    MusicGenerator.generate_track(MusicGenerator)
                    pygame.mixer.music.load(str(MusicGenerator.filename
                                            + str(MusicGenerator.current_track)
                                            + MusicGenerator.filetype))
                    pygame.mixer.music.play(-1)


if __name__ == "__main__":
    main()
