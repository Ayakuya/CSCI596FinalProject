import GUI
import VTKReader
import flow2D
import flow3D


def main():
    data = GUI.GUI()
    if data["D"] == "2D":
        flow2D.execute(data)
        VTKReader.generateGif(data["D"])
    else:
        flow3D.execute(data)
        VTKReader.generateGif(data["D"])


if __name__ == '__main__':
    main()
