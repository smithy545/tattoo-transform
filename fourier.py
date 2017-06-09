import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("cropped.jpg")
points = np.load("perfect2.npy")

sorted(points, key=lambda x: x[0])

xs = [p[0] for p in points]
ys = [p[1] for p in points]

amps = np.fft.fft(ys)
freqs = np.fft.fftfreq(len(ys))

# generate waves from fourier transform
waves = []
samples = np.arange(0, xs[-1], 0.1)
for i, a in enumerate(amps):
    wave = []
    for t in samples: # for graphing
        wave.append(a*np.cos(freqs[i]*t))
    waves.append(wave)


# plot waves
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

# Real frequencies
ax1.set_title("Real")
for w in waves[1:]: #ignore the 0 frequency because its just a height adjustment
    ax1.plot(samples, w)

# Imaginary frequencies (they cancel out)
ax2.set_title("Imaginary (cancels out)")
for w in waves:
    ax2.plot(samples, np.imag(w))

# Sister tattoo and data
ax3.set_title("Tatoo")
ax3.imshow(img, cmap="gray")
ax3.scatter(xs, ys)
ylim = ax3.get_ylim()
ax3.set_ylim(ylim[1], ylim[0])


plt.show()
