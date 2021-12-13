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


def profile(filename, files):
    fcall = []
    ml = []
    times = []
    for f in files:
        file = open(filename + "profile" + f + ".txt", encoding='utf-8')
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        ml.append(float(lines[0].replace("Performance in MLUPS: ", "")))
        sp = lines[1].replace(" ", "")

        i = 0
        s = 0
        while sp[i] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            s = s * 10 + int(sp[i])
            i += 1
        sp = sp[sp.index(")in"):]
        i = 3
        s2 = 0
        k = 0
        while sp[i] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            s2 = s2 * 10 + int(sp[i])
            i += 1
            if sp[i] == '.':
                i += 1
                k = len(str(s2))
        times.append(s2 / (np.power(10, len(str(s2)) - k)))
        fcall.append(s)
    print(np.mean(ml), np.mean(times), np.mean(fcall))


def main():
    filename = "C:\\Users\\yukar\\Desktop\\Github\\CSCI596\\origin_data\\cpu\\"
    files = ["1_1", "1_2", "1_3"]
    profile(filename, files)
    files = ["2_1", "2_2", "2_3"]
    profile(filename, files)
    files = ["3_1", "3_2", "3_3"]
    profile(filename, files)

    filename = "C:\\Users\\yukar\\Desktop\\Github\\CSCI596\\origin_data\\gpu\\"

    files = ["1_1", "1_2", "1_3"]
    profile(filename, files)
    files = ["2_1", "2_2", "2_3"]
    profile(filename, files)
    files = ["3_1", "3_2", "3_3"]
    profile(filename, files)


if __name__ == '__main__':
    main()
