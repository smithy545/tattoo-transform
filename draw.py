import cv2, threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

img = cv2.imread('cropped.jpg',0)

class Draw:
    def __init__(self):
        self.recording = False
        self.prevx = 0

        self.xs = []
        self.ys = []
        
        fig = self.fig = plt.figure()
        ax = self.ax = fig.add_subplot(111)
        ax.imshow(img, cmap="gray")
        plt.gca().invert_yaxis()
        self.xlim = ax.get_xlim()
        self.ylim = ax.get_ylim()

        cid1 = fig.canvas.mpl_connect('button_press_event', self.onclick)
        cid2 = fig.canvas.mpl_connect('button_release_event', self.onrelease)
        cid3 = fig.canvas.mpl_connect('motion_notify_event', self.onmove)

        self.ani = animation.FuncAnimation(fig, self.animate, interval=1000)
        plt.show()
        
    def onclick(self, event):
        if event.button == 3 and len(self.xs) + len(self.ys) > 1:
            self.xs.pop()
            self.ys.pop()
            self.ax.clear()
            self.ax.imshow(img, cmap="gray")
            self.ax.scatter(self.xs, self.ys, s=100)
            self.ax.set_xlim(self.xlim)
            self.ax.set_ylim(self.ylim)
        elif event.xdata != None and event.ydata != None:
            self.xs.append(int(event.xdata))
            self.ys.append(int(event.ydata))
            self.recording = True
            self.prevx = int(event.xdata)

    def onrelease(self, event):
        self.recording = False

    def onmove(self, event):
        x = event.xdata
        y = event.ydata
        if self.recording and x != None and y != None and x-self.prevx > 1 and int(x)%4 == 0:
            self.xs.append(int(x))
            self.ys.append(int(y))
            self.prevx = int(x)
    
    def animate(self, i):
        self.ax.scatter(self.xs, self.ys, s=100)
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        

m = Draw()

filename = raw_input("Filename to store in (no extension): ")
np.save(filename, [(x,y) for x, y in zip(m.xs, m.ys)])
