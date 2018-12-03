"""SOUND EFFECTS."""
import pygame
import library
import wave
import struct


class SoundFX:
    """Load and save wav files and soundEffects library."""

    playing = False
    echo_playing = False
    # pygame.mixer.Sound('./Game Sounds/Foot Steps.wav')
    footstep_sound = None
    echo_footprint_sound = None
    volume = 0
    sample_data = []
    SAMPLE_RATE = 44100
    MAX_VOLUME = 32767

    def __init__(self, vol=0.7):
        """Initialize."""
        
        if library.SOUND_HAS_INITIALIZED is None:
            return

        self.playing = False
        self.echo_footprint_sound = pygame.mixer.Sound(
            'Game Sounds/Foot Steps Echo.wav')
        self.footstep_sound = pygame.mixer.Sound(
            'Game Sounds/Foot Steps.wav')
        self.volume = vol

    def normalise(self, mutiplyer):
        """
        Normalise sample data.

        :return:
        """
        largest = 0
        for s in self.sample_data:
            s = int(s)
            if self.abs(self.sample_data[s]) > largest:
                largest = self.abs(self.sample_data[s])

        amplification = (self.MAX_VOLUME / largest) * mutiplyer
        print("largest: ", largest, "amplification", amplification)

        for s in range(len(self.sample_data)):
            louder = amplification * self.sample_data[s]
            self.sample_data[s] = louder

    def abs(self, value):
        """Force a positive value."""
        if value < 0:
            return - value

        return value

    def save_wav_file(self, filename):
        """
        Save sample data to wav file.

        :param filename: the wav file name
        :return:
        """
        sample_bytes = []
        self.normalise(0.5)
        for i in range(len(self.sample_data)):
            sample_bytes.append(struct.pack('h', int(self.sample_data[i])))
        byte_string = b''.join(sample_bytes)
        save_file = wave.open(filename + ".wav", "w")
        save_file.setparams((1, 2, self.SAMPLE_RATE, len(self.sample_data),
                             "NONE", "not compressed"))
        save_file.writeframesraw(byte_string)
        save_file.close()
        print(filename, " file saved")

    def read_wav_file(self, filename):
        """
        Read wav file into sample data.

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
        Generate an echo.

        :param volume: Echo volume
        :param start_sample: sample to start echoing from
        :param sample_len: length of the echo
        :param delay: delay until echo starts
        :return: None
        """
        self.SAMPLE_RATE
        echo_samples = self.sample_data[start_sample: start_sample + (
                sample_len * self.SAMPLE_RATE)]
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
        """
        Apply the echo to the .wav file.

        :return:
        """
        self.read_wav_file('Game Sounds/Foot Steps')
        self.generate_echo(0.6, 2590, 1, self.SAMPLE_RATE)
        self.save_wav_file('Game Sounds/Foot Steps Echo')

    def play_echo_sound(self):
        """
        Play the echo wav file that was created.

        :return:
        """
        if self.echo_playing is False:
            self.echo_footprint_sound.play(0)

    def play_footprint(self):
        """
        Check whether the keys are being pressed and play the sound.

        Check if the keys are no longer being pressed and stop the sound.
        :return:
        """
        if library.SOUND_HAS_INITIALIZED is None:
            return

        if not self.playing and (library.KEY_PRESSED["backwards"]
                                 or library.KEY_PRESSED["forwards"]
                                 or library.KEY_PRESSED["right"]
                                 or library.KEY_PRESSED["left"]):
            self.footstep_sound.play(-1)
            self.footstep_sound.set_volume(self.volume)
            self.playing = True
        elif self.playing and not (library.KEY_PRESSED["backwards"]
                                   or library.KEY_PRESSED["forwards"]
                                   or library.KEY_PRESSED["right"]
                                   or library.KEY_PRESSED["left"]):
            self.footstep_sound.stop()
            self.playing = False
