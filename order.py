import cv2, threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

img = cv2.imread('cropped.jpg',0)

class Order:
    def __init__(self, points=None):
        self.selected = None
        
        fig = self.fig = plt.figure()
        ax = self.ax = fig.add_subplot(111)
        ax.imshow(img, cmap="gray")
        plt.gca().invert_yaxis()
        xlim = self.xlim = ax.get_xlim()
        ylim = self.ylim = ax.get_ylim()

        if points != None:
            self.points = points
        else:
            samples = range(int(xlim[0]), int(xlim[1]), 5)
            self.points = [[x, y] for x, y in zip(samples, [int(ylim[1]/2) for i in samples])]
        self.xs = []
        self.ys = []
        for p in self.points:
            self.xs.append(p[0])
            self.ys.append(p[1])

        cid1 = fig.canvas.mpl_connect('button_press_event', self.onclick)
        cid2 = fig.canvas.mpl_connect('button_release_event', self.onrelease)
        cid3 = fig.canvas.mpl_connect('motion_notify_event', self.onmove)

        self.ani = animation.FuncAnimation(fig, self.animate, interval=50)
        plt.show()
        
    def onclick(self, event):
        x = event.xdata
        y = event.ydata

        if x != None and y != None:
            for i, p in enumerate(self.points):
                if (x-p[0])**2 + (y-p[1])**2 < 25:
                    self.selected = i
                    return

    def onmove(self, event):
        y = event.ydata
        if y != None and self.selected != None:
            self.points[self.selected][1] = int(y)
            self.ys[self.selected] = int(y)

    def onrelease(self, event):
        y = event.ydata
        if y != None and self.selected != None:
            if event.button == 3:
                del self.points[self.selected]
                del self.xs[self.selected]
                del self.ys[self.selected]
            else:
                self.points[self.selected][1] = int(y)
                self.ys[self.selected] = int(y)

            self.selected = None

    def animate(self, i):
        self.ax.clear()
        self.ax.imshow(img, cmap="gray")
        self.ax.scatter(self.xs, self.ys, s=100)
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)

filename = raw_input("Filename to load(empty for new file): ")
points = None
if len(filename) > 0:
    points = np.load(filename)

m = Order(points)

filename = raw_input("Filename to save(without extension): ")
if len(filename) > 0:
    np.save(filename, m.points)

