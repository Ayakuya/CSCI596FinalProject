import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import GUI
import flow2D, flow3D
import VTKReader


def main():
    data = GUI.GUI()
    if data["D"] == "2D":
        flow2D.execute(data)
    else:
        flow3D.execute(data)
    VTKReader.generateGif()


if __name__ == '__main__':
    main()
