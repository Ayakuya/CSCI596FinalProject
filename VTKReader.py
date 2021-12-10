import vtk
import pyvista
import numpy as np


def generateGif():
    filename = "output_00000000.vtr"
    reader = pyvista.get_reader(filename)

    plotter = pyvista.Plotter()

    plotter.open_gif("output.gif")
    pos = [(0.0, 0.0, 1.0),
           (0.0, 0.0, 0.0),
           (0.0, 1.0, 0.0)]

    # plotter.camera_set = True
    # plotter.camera.zoom(0.00001)
    # plotter.camera_position = 'xy'
    # plotter.camera.view_frustum = 3
    mesh = reader.read()
    plotter.add_mesh(mesh)

    nframe = 100
    for i in range(1, nframe):
        st = ""
        if len(str(i * 100)) <= len("00000000"):
            for j in range(8 - len(str(i * 100))):
                st += "0"
            st += str(i * 100)
        filename = "output_" + st + ".vtr"
        reader = pyvista.get_reader(filename)
        mesh = reader.read()

        # print(mesh.point_arrays)
        # x = mesh.point_arrays["ux"]
        # y = mesh.point_arrays["uy"]
        # print(x, y)
        # plotter.update_coordinates(np.meshgrid(x, y), render=False)
        # plotter.update_scalars(mesh.active_scalars["xy"], render=False)
        #
        # plotter.mesh.compute_normals(cell_normals=False, inplace=True)
        plotter.clear()
        plotter.add_mesh(mesh)
        plotter.render()
        plotter.write_frame()
    plotter.close()
    # def reader():
    #     filenames = ['output_{}.vtr'.format(i) for i in range(4)]
    #
    #     reader = vtk.vtkXMLRectilinearGridReader()
    #
    #     update_reader(filenames[0])
    #     grid = vtki.wrap(reader.GetOutput())
    #
    #     # Create a plotter object and set the scalars to the Z height
    #     plotter = vtki.Plotter()
    #     plotter.add_mesh(grid, name='foo')
    #
    #     # setup camera and close
    #     plotter.plot(auto_close=False)
    #
    #     # Open a gif
    #     plotter.open_gif('frames.gif')
    #
    #     # Update Z and write a frame for each updated position
    #     nframe = 15
    #     for fname in filenames:
    #         update_reader(fname)
    #         print(fname)
    #         grid = vtki.wrap(reader.GetOutput())
    #         plotter.add_mesh(grid, name='foo')
    #         plotter.write_frame()
    #
    #     # Close movie and delete object
    #     plotter.close()
    #
    #
    # def update_reader(fname):
    #     reader.SetFileName(fname)
    #     reader.Modified()
    #     reader.Update()
    #
    #
    #
