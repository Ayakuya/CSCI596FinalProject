import cProfile
import io
import pstats

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import torch
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import lettuce as lt
from lettuce import Lattice, D2Q9, Obstacle2D
from lettuce import UnitConversion, BounceBackBoundary, EquilibriumBoundaryPU


class Obstacles:
    def __init__(self, lattice, x, y, r, m, l):
        self.flow = Obstacle2D(
            resolution_x=x,
            resolution_y=y,
            reynolds_number=r,
            mach_number=m,
            lattice=lattice,
            char_length_lu=l
        )
        x, y = self.flow.grid
        self.x = self.flow.units.convert_length_to_lu(x)
        self.y = self.flow.units.convert_length_to_lu(y)
        self.conditions = []

    def setSquareObstacle(self, xpos, ypos, length):
        # Square:
        square = np.zeros(self.x.shape, dtype=bool)
        N = self.x.shape[0]
        M = self.x.shape[1]
        for i in range(N):
            for j in range(M):
                if xpos <= i <= xpos + length and ypos <= j <= ypos + length:
                    square[i, j] = True
                else:
                    square[i, j] = False
        condition = square
        self.conditions.append(condition)

    def setCylinderObstacle(self, xpos, ypos, r):
        # Cylinder:
        condition = np.sqrt((self.x - xpos) ** 2 + (self.y - ypos) ** 2) <= r
        self.conditions.append(condition)

    def setRectObstacle(self, xpos, ypos, xlength, ylength):
        # Rectangle:
        rect = np.zeros(self.x.shape, dtype=bool)
        N = self.x.shape[0]
        M = self.x.shape[1]
        for i in range(N):
            for j in range(M):
                if xpos <= i <= xpos + xlength and ypos <= j <= ypos + ylength:
                    rect[i, j] = True
                else:
                    rect[i, j] = False
        condition = rect
        self.conditions.append(condition)

    def setPolygonObstacle(self, polygon):
        poly = np.zeros(self.x.shape, dtype=bool)
        N = self.x.shape[0]
        M = self.x.shape[1]
        for i in range(N):
            for j in range(M):
                point = Point(i, j)
                poly[i, j] = point.within(polygon)
        condition = poly
        self.conditions.append(condition)

    def setObstacle(self):
        for c in self.conditions:
            self.flow.mask[np.where(c)] = 1

    def getFlow(self):
        return self.flow


class Model:
    def __init__(self, d, l):
        self.lattice = None
        self.flow = None
        self.collision = None
        self.streaming = None
        self.simulation = None
        self.device = torch.device(d)
        self.stencil = l
        self.dtype = torch.float32
        self.obstacle = None

    def initialization(self, data):
        self.setupLattice()
        self.obstacle = Obstacles(self.lattice, data["X"], data["Y"], 100, 0.1, 10)
        # setup obstacle
        for c in data["Cylinder"]:
            self.obstacle.setCylinderObstacle(c[0], c[1], c[2])
        for c in data["Square"]:
            self.obstacle.setSquareObstacle(c[0], c[1], c[2])
        for c in data["Rectangle"]:
            self.obstacle.setRectObstacle(c[0], c[1], c[2], c[3])
        for c in data["Polygon"]:
            self.obstacle.setPolygonObstacle(Polygon(c))
        self.obstacle.setObstacle()
        flow = self.obstacle.flow
        self.setupFlow(flow)
        self.setupCollision("BGKCollision")
        self.setupStreaming()
        self.setupSimulation()

    def setupLattice(self):
        self.lattice = lt.Lattice(self.stencil, device=self.device, dtype=self.dtype)

    def setupCollision(self, type):
        if type == "BGKCollision":
            self.collision = lt.BGKCollision(self.lattice, tau=self.flow.units.relaxation_parameter_lu)
        if type == "RegularizedCollision":
            self.collision = lt.RegularizedCollision(self.lattice, tau=self.flow.units.relaxation_parameter_lu)
        if type == "KBCCollision2D":
            self.collision = lt.KBCCollision2D(self.lattice, tau=self.flow.units.relaxation_parameter_lu)

    def setupStreaming(self):
        self.streaming = lt.StandardStreaming(self.lattice)

    def setupSimulation(self):
        self.simulation = lt.Simulation(flow=self.flow, lattice=self.lattice, collision=self.collision,
                                        streaming=self.streaming)

    def setupFlow(self, flow):
        self.flow = flow

    def simulationOutput(self):
        Energy = lt.IncompressibleKineticEnergy(self.lattice, self.flow)
        reporter = lt.ObservableReporter(Energy, interval=1000, out=None)
        self.simulation.reporters.append(reporter)
        self.simulation.reporters.append(
            lt.VTKReporter(self.lattice, self.flow, interval=100, filename_base="./output"))
        self.simulation.initialize_f_neq()
        mlups = self.simulation.step(num_steps=10000)
        print("Performance in MLUPS:", mlups)

    def processEnergy(self):
        energy = np.array(self.simulation.reporters[0].out)

        # Kinetic Energy
        plt.rcParams.update({'font.size': 16})
        plt.rc('font', family='serif')
        plt.rc('axes', axisbelow=True)
        plt.grid(linestyle="--")
        plt.plot(energy[:, 1], energy[:, 2])
        plt.title('Kinetic energy')
        plt.xlabel('Time', labelpad=12)
        plt.ylabel('Energy in physical units', labelpad=12)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(12, 8)
        fig.savefig('Kinetic Energy.pdf')
        plt.show()

        # Plot
        plt.rcParams.update({'font.size': 16})
        plt.rc('font', family='serif')
        plt.rc('axes', axisbelow=True)
        u = self.flow.units.convert_velocity_to_pu(self.lattice.u(self.simulation.f)).numpy()
        u_norm = np.linalg.norm(u, axis=0)
        plt.imshow(u_norm)
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(12, 8)
        fig.savefig('Flow.pdf')
        plt.show()


def execute(data):
    pr = cProfile.Profile()
    pr.enable()
    s = Model(torch.device("cpu"), lt.D2Q9)
    s.initialization(data)
    # s.setupLattice()
    # o = Obstacles(s.lattice, 501, 301, 100, 0.1, 10)
    # o.setCylinderObstacle(150, 150, 20)
    # o.setCylinderObstacle(300, 150, 20)
    # o.setObstacle()
    # flow = o.getFlow()
    #
    # s.setupFlow(flow)
    # s.setupCollision("BGKCollision")
    # s.setupStreaming()
    # s.setupSimulation()
    #
    s.simulationOutput()
    s.processEnergy()

    pr.disable()
    s = io.StringIO()

    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())

    with open('profile.txt', 'w+') as f:
        f.write(s.getvalue())
