import matplotlib

import GUI
import VTKReader
import flow2D
import flow3D
import matplotlib.pyplot as plt
import numpy as np


def main():
    times = [49.039, 69.635, 99.246, 108.474, 122.344]
    xlabels = [500, 750, 1000, 1250, 1500]

    plt.rcParams.update({'font.size': 16})
    plt.rc('font', family='serif')
    plt.rc('axes', axisbelow=True)
    plt.grid(linestyle="--")
    colors = dict()
    colors.update({"SO": 'tab:blue'})
    colors.update({"SE": 'darkseagreen'})
    colors.update({"PM": 'indianred'})
    plt.plot(xlabels, times, linestyle='solid', label=xlabels, linewidth=3.0,
             color='tab:blue')
    for i in range(5):
        plt.scatter(xlabels[i], times[i], color='tab:blue', s=70.0)
    plt.xticks(xlabels)
    plt.ylabel("Time (seconds)", labelpad=12)
    plt.xlabel("Width", labelpad=12)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(12, 8)
    fig.savefig('RQ3times.pdf')
    plt.show()

    plt.rcParams.update({'font.size': 16})
    plt.rc('font', family='serif')
    plt.rc('axes', axisbelow=True)
    plt.grid(linestyle="--")
    colors = dict()
    colors.update({"SO": 'tab:blue'})
    colors.update({"SE": 'darkseagreen'})
    colors.update({"PM": 'indianred'})

    for i in range(5):
        plt.scatter(xlabels[i], times[i], color='indianred', s=70.0)

    X_plot = np.linspace(500, 1500)
    m, b = np.polyfit(xlabels, times, 1)
    print(b, m)

    plt.plot(X_plot, b + m * X_plot, '-')

    plt.xticks(xlabels)
    plt.ylabel("Time (seconds)", labelpad=12)
    plt.xlabel("Width", labelpad=12)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(12, 8)
    fig.savefig('RQ3times_fit.pdf')
    plt.show()


if __name__ == '__main__':
    main()
