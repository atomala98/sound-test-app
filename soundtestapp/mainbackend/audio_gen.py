import numpy as np
from time import strftime, gmtime
import wavio
from random import randint

SETTINGS = {
    'BASE_FREQ': 150,
    'FS': 44100,
    "FADE_LEN": 1000
}

BASE_FREQ = SETTINGS.get('BASE_FREQ')
FS = SETTINGS.get('FS')
FADE_LEN = SETTINGS.get('FADE_LEN')

# linear fade in/out

def randomise_delta(delta):
    return (2 * randint(0, 1) - 1) * delta

def linear_fade_in(note):
    samples = FADE_LEN
    for i in range(samples):
        note[i] = note[i]*(i/samples)
    return note

def linear_fade_out(note):
    samples = FADE_LEN
    for i in range(samples):
        note[-i + 1] = note[-i + 1]*(i/samples)
    return note

# two sine waves with DELTA_F difference

def frequency_difference_test(delta_freq, username, time):
    frequency = BASE_FREQ
    seconds = 1  
    
    t = np.linspace(0, seconds, seconds * FS, False)
    note = np.sin(frequency * t * 2 * np.pi)
    note = linear_fade_in(note)
    note = linear_fade_out(note)
    
    notes_break = np.zeros(FS//2)
    
    pitched_note = np.sin((frequency + delta_freq) * t * 2 * np.pi)

    pitched_note = linear_fade_in(pitched_note)
    pitched_note = linear_fade_out(pitched_note)

    audio = np.concatenate((note, notes_break, pitched_note, notes_break))
    return save_to_file(username, audio, time)

# saving wave to file

def save_to_file(username, audio, time):
    filename = f"mainbackend/static/mainbackend/{username}---{time}.wav"
    wavio.write(filename, audio, FS, sampwidth=2)
    
    return filename


if __name__ == "__main__":
    dt_gmt = strftime("%Y-%m-%d %H-%M-%S", gmtime())
    frequency_difference_test(5, "Andrzej", dt_gmt)