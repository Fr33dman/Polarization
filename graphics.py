import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy.plotting import plot_implicit
from sympy.parsing.sympy_parser import parse_expr

def roots(Ex_Ey):
    E = 1
    Ey = (E/(Ex_Ey**2 + 1))**0.5
    Ex = Ey*Ex_Ey
    return Ex, Ey


class Graph:

    def __init__(self):
        self.frames = 60
        self.interval = 1000
        self.light_speed = 299792458 / 1000
        self.lamda = 380
        self.omega = 2 * np.pi * self.light_speed / self.lamda
        self.delta_fi = 0.5 * np.pi
        self.E = 1
        self.Ex_Ey = 1
        self.Ex, self.Ey = roots(self.Ex_Ey)
        self.elev = 10
        self.azim = 15
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.grid(False)
        self.ax.axis('off')
        self.ax.view_init(self.elev, self.azim)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 5)
        self.ax.set_zlim(-1, 1)
        self.ax.text(0, 0, 1, 'Ey')
        self.ax.text(0, 1, 0, 'Ex')
        self.ax.text(15, 0, 0, 'z')
        self.quivers = self.ax.quiver([0, 0, 0], [0, 0, 0], [0, 0, 0], [20, 0, 0], [0, 1, 0], [0, 0, 1], colors='b')

    def set_Ex_Ey(self, Ex_Ey):
        self.Ex_Ey = Ex_Ey
        self.Ex, self.Ey = roots(Ex_Ey)

    def set_delta_fi(self, delta_fi):
        self.delta_fi = delta_fi * np.pi

    def set_lambda(self, lamda):
        self.lamda = lamda
        self.omega = 2 * np.pi * self.light_speed / self.lamda

    def save(self):
        pass

    def refresh(self):
        self.save()


class Spiral(Graph):

    def __init__(self, file):
        super(Spiral, self).__init__()
        self.line, = self.ax.plot([], [], [], color='r')
        self.file = file
        self.ax.set_position([-0.20, 0, 1, 1])
        self.save()

    def init(self):
        self.line.set_data(np.asarray([]), np.asarray([]))
        self.line.set_3d_properties(np.asarray([]))
        return self.line,

    def animate(self, i):
        x = np.linspace(0, 15, 500)
        y = self.Ex * np.cos(2 * x - self.omega * 0.0001*i)
        z = self.Ey * np.cos(2 * x - self.omega * 0.0001*i - self.delta_fi)
        self.line.set_data(np.asarray(x), np.asarray(y))
        self.line.set_3d_properties(np.asarray(z))
        return self.line,

    def save(self):
        anim = FuncAnimation(self.fig, self.animate, init_func=self.init,
                             frames=200, interval=300, blit=True)
        anim.save(self.file, writer='imagemagick', fps=60)


class Waves(Graph):

    def __init__(self, file):
        super(Waves, self).__init__()
        self.ax.set_position([-0.20, 0, 1, 1])
        self.line_x, = self.ax.plot([], [], [], color='r')
        self.line_y, = self.ax.plot([], [], [], color='g')
        self.file = file
        self.save()

    def init(self):
        self.line_x.set_data(np.asarray([]), np.asarray([]))
        self.line_x.set_3d_properties(np.asarray([]))
        self.line_y.set_data(np.asarray([]), np.asarray([]))
        self.line_y.set_3d_properties(np.asarray([]))
        return self.line_x, self.line_y

    def animate(self, i):
        x = np.linspace(0, 15, 500)
        y1 = self.Ex * np.cos(2 * x - self.omega * 0.0001*i)
        z2 = self.Ey * np.cos(2 * x - self.omega * 0.0001*i - self.delta_fi)
        z1 = x * 0
        y2 = x * 0
        self.line_x.set_data(np.asarray(x), np.asarray(y1))
        self.line_x.set_3d_properties(np.asarray(z1))
        self.line_y.set_data(np.asarray(x), np.asarray(y2))
        self.line_y.set_3d_properties(np.asarray(z2))
        return self.line_x, self.line_y

    def save(self):
        anim = FuncAnimation(self.fig, self.animate, init_func=self.init,
                       frames=self.frames, interval=self.interval, blit=True)
        anim.save(self.file, writer='imagemagick', fps=60)


class Circle(Graph):

    def __init__(self, file, Ex_Ey, delta_fi, lamda):
        super(Circle, self).__init__()
        self.lamda = lamda
        self.delta_fi = delta_fi * np.pi
        self.Ex_Ey = Ex_Ey
        self.Ex, self.Ey = roots(self.Ex_Ey)
        self.file = file
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
        self.ax.grid(False)
        self.ax.axis('off')
        self.ax.set_ylim(-2, 2)
        self.ax.set_xlim(-2, 2)
        self.ax.text(0, 1, 'Ey')
        self.ax.text(1, 0, 'Ex')
        t = np.linspace(0, 3, 100)
        x1 = self.Ex * np.cos(-self.omega * t)
        y1 = lambda xx: self.Ey * np.cos(-np.arccos(xx/self.Ex) - self.delta_fi)
        self.ax.plot(x1, y1(x1), color='r')
        x2 = self.Ex * np.cos(-self.omega * t)
        y2 = lambda xx: self.Ey * np.cos(np.arccos(xx / self.Ex) - self.delta_fi)
        self.ax.plot(x2, y2(x2), color='r')
        x_pos = [-1, 0]
        y_pos = [0, -1]
        x_direct = [2.5, 0]
        y_direct = [0, 2]
        self.ax.quiver(x_pos, y_pos, x_direct, y_direct, scale=5)
        self.ax.set_position([-0.25, -0.02, 1, 1])
        self.line_arrow, = self.ax.plot(np.asarray([]), np.asarray([]),  color='r')
        self.save()

    def init(self):
        self.line_arrow.set_data(np.asarray([]), np.asarray([]))
        return self.line_arrow,

    def animate(self, i):
        x = self.Ex * np.cos(-self.omega * 0.0001 * i)
        y = self.Ey * np.cos(-self.omega * 0.0001 * i - self.delta_fi)
        self.line_arrow.set_data(np.asarray([0, x]), np.asarray([0, y]))
        return self.line_arrow,

    def save(self):
        anim = FuncAnimation(self.fig, self.animate, init_func=self.init,
                             frames=self.frames, interval=self.interval, blit=True)
        anim.save(self.file, writer='imagemagick', fps=60)
