import pygame
import library
import wave
import struct
import math
from pygame.locals import *


class SoundFX:
    """
    load and save wav files and soundEffects library
    """
    playing = False
    footstep_sound = None # pygame.mixer.Sound('./Game Sounds/Foot Steps.wav')
    volume = 0
    sample_data = []
    SAMPLE_RATE = 44100
    MAX_VOLUME = 32767

    def __init__(self, vol=0.7):
        self.playing = False
        self.footstep_sound = pygame.mixer.Sound('Game Sounds/Foot Steps.wav')
        self.volume = vol

    def normalise(self, mutiplyer):
        """
        normalise sample data
        :return:
        """
        largest = 0
        for s in self.sample_data:
            s = int(s)
            if self.abs(self.sample_data[s]) > largest:
                largest = self.abs(self.sample_data[s])

        amplification = (self.MAX_VOLUME / largest) * mutiplyer
        print(largest, amplification)
        print("Largest sample value in the original sound was ", largest)
        print("Amplification multiplier is ", amplification)

        for s in range(len(self.sample_data)):
            louder = amplification * self.sample_data[s]
            self.sample_data[s] = louder

    def abs(self, value):

        if value < 0:
            return - value

        return value

    def save_wav_file(self, filename):
        """
        saves sample data to wav file
        :param filename: the wav file name
        :return:
        """
        sample_bytes = []
        self.normalise(0.5)
        for i in range(len(self.sample_data)):
            print(self.sample_data[i])
            sample_bytes.append(struct.pack('h', int(self.sample_data[i])))
        byte_string = b''.join(sample_bytes)
        save_file = wave.open(filename + ".wav", "w")
        save_file.setparams((1, 2, self.SAMPLE_RATE, len(self.sample_data), "NONE", "not compressed"))
        save_file.writeframesraw(byte_string)
        save_file.close()
        print(filename, " file saved")

    def read_wav_file(self, filename):
        """
        reads wav file into sample data
        :param filename: the wav filename
        :return:
        """
        self.sample_data = []
        read_file = wave.open(filename+".wav", "r")
        total_samples = read_file.getnframes()

        for i in range(total_samples):
            sample_byte = read_file.readframes(1)
            self.sample_data.append(struct.unpack_from('h', sample_byte)[0])

        read_file.close()

    def generate_echo(self, volume, start_sample, sample_len, delay):
        """
        :param volume: Echo volume
        :param start_sample: sample to start echoing from
        :param sample_len: length of the echo
        :param delay: delay until echo starts
        :return: None
        """
        self.SAMPLE_RATE
        echo_samples = self.sample_data[start_sample: start_sample + (sample_len * self.SAMPLE_RATE)]
        echo_samp_index = 0
        for i in range(start_sample + delay, len(self.sample_data)):
            self.sample_data[i] += echo_samples[echo_samp_index] * volume
            echo_samp_index += 1
            if echo_samp_index >= len(echo_samples):
                echo_samp_index = 0
                volume -= 0.3

            if volume <= 0:
                break

    def apply_echo(self):
        self.read_wav_file('Game Sounds/Foot Steps')
        self.generate_echo(0.6, 2590, 1, self.SAMPLE_RATE)
        self.save_wav_file('Game Sounds/Foot Steps Echo')

    def play_footprint(self):
        """
        checks whether the keys are being pressed and plays the sound
        checks if the keys are no longer being pressed and stops the sound
        :return:
        """
        if not self.playing and (library.KEY_PRESSED["backwards"] or library.KEY_PRESSED["forwards"] or library.KEY_PRESSED["right"]
                                 or library.KEY_PRESSED["left"]):
            self.footstep_sound.play(0)
            self.footstep_sound.set_volume(self.volume)
            self.playing = True
        elif self.playing and not (library.KEY_PRESSED["backwards"] or library.KEY_PRESSED["forwards"] or library.KEY_PRESSED["right"]
                                   or library.KEY_PRESSED["left"]):
            self.footstep_sound.stop()
            self.playing = False
