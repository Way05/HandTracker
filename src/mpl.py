import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(X, Y)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

Z = np.sin(np.sqrt(X**2 + Y**2))
surf = [ax.plot_surface(X, Y, Z, cmap="cool", edgecolor="none")]

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-2, 2)
ax.axis("off")


def animFrame(frame):
    ax.cla()
    Z = np.sin(np.sqrt(X**2 + Y**2) + frame * 0.05)
    ax.plot_surface(X, Y, Z, cmap="cool", edgecolor="none")
    ax.set_facecolor("black")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-2, 2)
    ax.axis("off")
    ax.view_init(elev=30, azim=frame)
    return [ax]


anim = FuncAnimation(fig, animFrame, frames=360, interval=1, blit=True)
plt.show()
