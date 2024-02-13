#!/home/ilkin/Documents/GitHub/other/.venv/bin/python3

# Importing necessary libraries
from PIL import Image, ImageFont, ImageDraw, ImageOps 
import numpy as np
import matplotlib.pyplot as plt
import sys
import pyaudio

# Retrieving string from command-line arguments
string = sys.argv[1]
length = len(string)

# Audio parameters
f = 100
duration = length
volume = 0.00
fs = 44100

# Image parameters
xsize = 640 * length
ysize = 1100

# Creating a black and white image with PIL
image = Image.new('RGB', (xsize, ysize), (0, 0, 0)).convert('1')
fn = lambda x: 255 if x > 100 else 0
image = image.convert('L').point(fn, mode='1')

# Drawing text on the image
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(".font.ttf", 1000)
draw.text((0, -250), string, 255, font=font)

# Converting image to numpy array for audio generation
mat = np.array(image)
arr = np.sum(mat, axis=0)
mx = np.max(arr)
arr = arr / mx
arr = np.repeat(arr, int(44100 / xsize * duration))

# Generating audio samples
xlim = len(arr)
arr = (np.hstack((arr, np.zeros(duration * fs - len(arr))))) * f
ids = 1 - (arr < 0.01)


p = pyaudio.PyAudio()
samples = (np.sin(np.pi * np.arange(fs * duration) * f * (arr - 0.5) / fs)).astype(np.float32) * ids
output_bytes = (volume * samples).tobytes()

# Initializing and configuring PyAudio stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Playing audio
stream.write(output_bytes)

# Closing stream and terminating PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Plotting audio waveform and displaying the inverted image
fig, (a0, a1) = plt.subplots(2)
fig.set_figwidth(xsize * 0.002)
a0.plot(samples, 'k', linewidth=0.01)
a0.plot(arr / f - .5, 'k')
a0.set_axis_off()
a0.set_xlim(0, xlim)
a1.imshow(ImageOps.invert(image), aspect="auto")
a1.margins(x=0)
a1.set_axis_off()
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
