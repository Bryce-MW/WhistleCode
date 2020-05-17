import pyaudio
import numpy as np
from morse import codons
from pynput.keyboard import Key, Controller

np.set_printoptions(suppress=True)  # don't use scientific notation

CHUNK = 4096 * 2  # number of data points to read at a time
RATE = 44100  # time resolution of the recording device (Hz)
maxValue = 2**16

p = pyaudio.PyAudio()  # start the PyAudio class
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK)  # uses default input device


def ave_freq(cycles):
    freqs, vols = zip(*(get_freq() for _ in range(cycles)))
    return sum(freqs)/cycles, sum(vols)/cycles


def get_freq():
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    data = data * np.hanning(len(data))  # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft) / 2)]  # keep only first half
    freq = np.fft.fftfreq(CHUNK, 1.0 / RATE)
    freq = freq[:int(len(freq) / 2)]  # keep only first half
    freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
    volume = np.abs(np.max(data) - np.min(data)) / maxValue
    return freqPeak, volume


def read_char():
    char_comp = []
    done = 0
    last = False
    while done < 10:
        freqPeak, volume = get_freq()
        high = freqPeak > avef
        loud = volume >= avev * 0.5
        if loud and not last:
            print(high, freqPeak)
            char_comp.append("." if high else "-")
            last = True
            done = 0
        else:
            last = loud
            if not last:
                done += 1
    return "".join(char_comp)


print("High")
highf, highv = ave_freq(5)
print(highf)
print("Low")
lowf, lowv = ave_freq(5)
print(lowf)
avef = (highf + lowf) / 2
avev = (highv + lowv) / 2
print("Start")

keyboard = Controller()
ignore = True
caps = False

try:
    while True:
        codon = ""
        try:
            codon = read_char()
            if not ignore:
                if codons[codon] == "shift":
                    caps = not caps
                else:
                    if caps:
                        keyboard.type(codons[codon].upper())
                    else:
                        keyboard.type(codons[codon])
            print(codons[codon])
        except KeyError:
            if codon:
                print("\n" + codon)
        ignore = False

except KeyboardInterrupt:
    # close the stream gracefully
    stream.stop_stream()
    stream.close()
    p.terminate()
