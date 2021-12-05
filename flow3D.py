import lettuce as lt
import torch
import numpy as np
import matplotlib.pyplot as plt
from lettuce import Lattice, D2Q9, Obstacle2D, Obstacle3D, Observable
from lettuce import UnitConversion, BounceBackBoundary, EquilibriumBoundaryPU


class Setup:
    def __init__(self, d, l):
        self.device = torch.device(d)
        self.stencil = l
        self.dtype = torch.float32

    def setupLattice(self):
        lattice = lt.Lattice(self.stencil, device=self.device, dtype=self.dtype)
        return lattice


class Map:
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
        condition = (self.x - xpos) <= length and (self.y - ypos) <= length
        self.conditions.append(condition)

    def setCylinderObstacle(self, xpos, ypos, r):
        # Cylinder:
        condition = np.sqrt((self.x - xpos) ** 2 + (self.y - ypos) ** 2) <= r
        self.conditions.append(condition)

    def setRectObstacle(self, xpos, ypos, xlength, ylength):
        # Rectangle:
        condition = (self.x - xpos) <= xlength and (self.y - ypos) <= ylength
        self.conditions.append(condition)

    def setObstacle(self):
        for c in self.conditions:
            self.flow.mask[np.where(c)] = 1


class Collision:
    def __init__(self, lattice, flow):
        self.BGKCollision = lt.BGKCollision(lattice, tau=flow.units.relaxation_parameter_lu)
        self.RegularizedCollision = lt.RegularizedCollision(lattice, tau=flow.units.relaxation_parameter_lu)
        self.KBCCollision2D = lt.KBCCollision2D(lattice, tau=flow.units.relaxation_parameter_lu)


def plot(datas):
    X = np.arange(1, 10)
    Y = np.arange(1, 10)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


class IncompressibleKineticEnergy(Observable):
    """Total kinetic energy of an incompressible flow."""

    def __call__(self, f):
        dx = self.flow.units.convert_length_to_pu(1.0)
        kinE = self.flow.units.convert_incompressible_energy_to_pu(torch.sum(self.lattice.incompressible_energy(f)))
        kinE *= dx ** self.lattice.D
        return kinE


def main():
    s = Setup(torch.device("cpu"), lt.D3Q27)
    lattice = s.setupLattice()
    # flow = lt.TaylorGreenVortex3D(resolution=256, reynolds_number=100, mach_number=0.05, lattice=lattice)
    # flow = lt.TaylorGreenVortex3D(resolution=256, reynolds_number=1600, mach_number=0.05, lattice=lattice)

    flow = Obstacle3D(
        resolution_x=101,
        resolution_y=81,
        resolution_z=11,
        reynolds_number=100,
        mach_number=0.1,
        lattice=lattice,
        char_length_lu=10
    )
    x, y, z = flow.grid
    x = flow.units.convert_length_to_lu(x)
    y = flow.units.convert_length_to_lu(y)
    z = flow.units.convert_length_to_lu(z)
    condition = np.sqrt((x - 50) ** 2 + (y - 30) ** 2) < 20
    flow.mask[np.where(condition)] = 1

    collision = lt.BGKCollision(lattice, tau=flow.units.relaxation_parameter_lu)
    streaming = lt.StandardStreaming(lattice)
    simulation = lt.Simulation(flow=flow, lattice=lattice, collision=collision, streaming=streaming)

    Energy = IncompressibleKineticEnergy(lattice, flow)
    reporter = lt.ObservableReporter(Energy, interval=1000, out=None)
    simulation.reporters.append(reporter)
    simulation.reporters.append(lt.VTKReporter(lattice, flow, interval=100, filename_base="./output"))

    simulation.initialize_f_neq()
    mlups = simulation.step(num_steps=10000)
    print("Performance in MLUPS:", mlups)

    energy = np.array(simulation.reporters[0].out)
    print(energy.shape)
    plt.plot(energy[:, 1], energy[:, 2])
    plt.title('Kinetic energy')
    plt.xlabel('Time')
    plt.ylabel('Energy in physical units')
    plt.show()

    u = flow.units.convert_velocity_to_pu(lattice.u(simulation.f)).numpy()
    u_norm = np.linalg.norm(u, axis=0)
    # plt.imshow(u_norm)
    print(u_norm.shape)


if __name__ == '__main__':
    main()
