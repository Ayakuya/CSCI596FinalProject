import matplotlib

import GUI
import VTKReader
import flow2D
import flow3D
import matplotlib.pyplot as plt
import numpy as np

sum = 0


def my_fmt(x):
    print(x)
    return '{:.2f}%'.format(x)


def plot(filename, type, labels):
    file = open(filename, encoding='utf-8')
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

    data = []
    tottime = []
    for i in range(6, 16):
        c = lines[i].split(" ")
        row = []
        for j in c:
            if len(j) != 0:
                row.append(float(j))
            if len(row) >= 5:
                break
        data.append(row)
        tottime.append(row[1])
    global sum
    sum = np.sum(tottime)
    # Pie
    plt.rcParams.update({'font.size': 16})
    plt.rc('font', family='serif')
    plt.rc('axes', axisbelow=True)
    # plt.grid(linestyle="--")
    plt.pie(tottime,
            labels=labels, autopct=my_fmt)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(16, 10)

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig.savefig("pie_" + type + ".pdf")
    plt.show()


def main():
    filename = "profile.txt"

    labels = ["lettuce/boundary", "method einsum", "lettuce/equilibrium", "pyevtk", "lettuce/streaming", "method where",
              "method roll", "method tensor", "method pow", "method tensordot"]
    plot(filename, "GPU", labels)

    filename = "profile1.txt"

    labels = ["lettuce/equilibrium", "lettuce/collision", "method where", "method einsum", "lettuce/simulation",
              "method sum", "lettuce/boundary", "method pow", "method tensordot", "lettuce/lattices"]

    plot(filename, "CPU", labels)


if __name__ == '__main__':
    main()
