import matplotlib

import GUI
import VTKReader
import flow2D
import flow3D
import matplotlib.pyplot as plt
import numpy as np


def plot(cpu, gpu):
    data = [cpu, gpu]
    print(data)
    plt.rcParams.update({'font.size': 16})
    plt.rc('font', family='serif')
    plt.rc('axes', axisbelow=True)
    plt.grid(linestyle="--")

    X = np.arange(3)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 10)
    # fig = plt.figure()
    colors = ['indianred', 'darkseagreen']
    plt.bar(X - 0.12, data[0], color=colors[0], width=0.24, label="CPUs")
    plt.bar(X + 0.12, data[1], color=colors[1], width=0.24, label="GPUs")
    #
    fig.set_size_inches(16, 10)
    plt.xticks([0, 1, 2], ["Obstacle_1", "Obstacle_2", "Obstacle_3"])
    plt.ylabel("Time (seconds)")
    plt.legend()
    fig.savefig("cpu&gpu.pdf")
    plt.show()


def main():
    cpu = [[409.759, 405.922, 408.488], [403.077, 394.648, 394.496], [392.996, 394.119, 396.363]]
    gpu = [[49.039, 49.052, 49.407], [49.019, 49.628, 49.834], [49.682, 49.798, 49.678]]

    cpu = np.mean(cpu, axis=1)
    gpu = np.mean(gpu, axis=1)

    print(cpu, gpu)

    plot(cpu, gpu)
    #
    # filename = "profile1.txt"
    #
    # plot(filename, "CPU")


if __name__ == '__main__':
    main()
