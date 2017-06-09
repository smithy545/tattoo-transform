import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("cropped.jpg")

class Fourier:
    def __init__(self):
        self.points = points = np.load("perfect2.npy")

        sorted(points, key=lambda x: x[0])

        self.xs = np.array([p[0] for p in points])
        self.ys = np.array([p[1] for p in points])

        self.amps = np.fft.fft(self.ys)
        self.freqs = np.fft.fftfreq(self.ys.shape[-1])

        # generate waves from fourier transform
        self.waves = []
        self.samples = np.arange(0, self.xs[-1], 0.1)
        for i, a in enumerate(self.amps):
            wave = []
            for t in self.samples: # for graphing
                wave.append(a*np.cos(self.freqs[i]*t))
            self.waves.append(wave)

        self.recreate()
        plt.show()

    def recreate(self):
        N = len(self.amps)
        ys = []
        for n, x in enumerate(self.xs):
            y = 0
            for k, a in enumerate(self.amps):
                y += a*np.exp((1j)*2*np.pi*k*n/N)
            ys.append(y/N)

        plt.plot(ys, 'bo')

    def graph(self):
        ax = plt.gca()
        n = len(self.amps)
        graph = [(x,y/n) for x,y in zip(self.freqs, self.amps)]
        sorted(graph, key=lambda x: x[0])
        x = [p[0] for p in graph]
        y = [p[1] for p in graph]
        ax.plot(x, y, 'k-')

    def draw(self):        
        # plot waves
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

        # Real frequencies
        self.drawReal(ax1)

        # Imaginary frequencies (they cancel out)
        self.drawImag(ax2)

        # Sister tattoo and data
        self.drawTattoo(ax3)

        plt.show()

    def drawReal(self, ax=None):
        if ax == None:
            ax = plt.gca()
        ax.set_title("Real")
        for w in self.waves[1:]: #ignore the 0 frequency because its just a height adjustment
            ax.plot(self.samples, w)

    def drawImag(self, ax=None):
        if ax == None:
            ax = plt.gca()
        ax.set_title("Imaginary (cancels out)")
        for w in self.waves:
            ax.plot(self.samples, np.imag(w))

    def drawTattoo(self, ax=None):
        if ax == None:
            ax = plt.gca()
        ax.set_title("Tatoo")
        ax.imshow(img, cmap="gray")
        ax.scatter(self.xs, self.ys)
        ylim = ax.get_ylim()
        ax.set_ylim(ylim[1], ylim[0])

f = Fourier()
