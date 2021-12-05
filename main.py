import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import GUI
import flow2D


def main():
    data = GUI.GUI()
    flow2D.execute(data)


if __name__ == '__main__':
    main()
