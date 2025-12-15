import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import time  # For time-based animation
from PyQt5 import QtCore  # For QTimer


class Graph:
    def __init__(self):
        # Create the application and main window
        self.app = pg.mkQApp("Basic 3D Plot Example")
        self.w = gl.GLViewWidget()
        self.w.show()
        self.w.setWindowTitle("PyQtGraph 3D Surface Plot")
        # Set the camera position for a better initial view
        self.w.setCameraPosition(distance=50, elevation=20, azimuth=45)

        # Add a grid item to the view
        self.grid = gl.GLGridItem()
        self.w.addItem(self.grid)

        # Add X, Y, Z axes
        self.axis = gl.GLAxisItem()
        # Scale axes for better visibility if needed
        # axis.scale(2, 2, 2)
        self.w.addItem(self.axis)

        # Generate test data (a 2D numpy array)
        # Z values form a sine wave pattern
        self.X = np.linspace(-10, 10, 40)
        self.Y = np.linspace(-10, 10, 40)
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        self.Z = np.sin(np.sqrt(self.X**2 + self.Y**2))

        # Create the surface plot item
        # The 'shader' argument adds basic shading
        self.surface = gl.GLSurfacePlotItem(
            x=self.X[0, :],
            y=self.Y[:, 0],
            z=self.Z,
            shader="shaded",
            color=(0.5, 0.5, 1, 0.8),
        )
        self.w.addItem(self.surface)

        self.scalar = 1

    def updateScalar(self, scalar):
        self.scalar = scalar

    def updateCamera(self, distScalar, aziScalar, elevScalar):
        self.w.setCameraPosition(
            distance=distScalar, elevation=elevScalar, azimuth=aziScalar
        )

    # Animation setup
    def update_wave(self):
        # Update Z with a time-based phase shift for animation
        phase = time.time() * 1  # Adjust speed by changing the multiplier
        self.Z = self.scalar * np.sin(np.sqrt(self.X**2 + self.Y**2) + phase)
        self.surface.setData(z=self.Z)  # Refresh the surface with new Z data

    def start_anim(self):
        # Create a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_wave)
        QtCore.QTimer.singleShot(10, lambda: self.timer.start(50))
        # self.timer.start(50)  # Update every 50 ms (adjust for speed)
        pg.exec()
