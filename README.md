# CSCI596FinalProject
## Table of contents
* [General info](#general-info)
* [Visualization info](#visualization-info)
* [Proposal info](#proposal-info)
* [Technologies](#technologies-&-libraries)
* [Setup](#setup)
* [Reference](#reference)

## General info
The initial inspiration of this project is using not commonly used programming languages to do simulation and visualization, such as python, which is not as popular as C++ in visualization. 
This project is a CFD simulation and Visualization project. It used Lettuce to do the simulation and PyVista to do the visualization. The simulation part is based on Lettuce, which is a LBM based code with PyTorch implementation[^2]. PyVista is a module for the Visualization Toolkit (VTK), with a different approach on interfacing with VTK through NumPy and direct array access[^1].
This project contains two parts:
1. 2D and 3D simulation and visualization
2. A proposal based on efficiency analysis case study

## Visualization info
In this part, it starts with a simple GUI, which can use the file link to input Obstacle information or manually input the information (2D) into the code. Then it will calculate the simulation and output with 100 VTK files to save the simulation data. Then, PyVista will process all the VTK files (ending in .vtr) and generate a gif file named output.gif.
	![2D Visualization Example](example2D.gif) 
	![3D Visualization Example](example3D.gif) 

## Proposal info
This proposal is based on the profiling from following devices:
1. GPU: GTX1070
2. CPU: Intel(R) i7 CPU

Due to the time limitation and devices limitation, many texture parts and 3D data analysis haven't done much. The main reason is that I can only borrow the GTX1070 which is a relatively old one and 3D simulation takes a long time. It's possible to spend more than two weeks doing the running processes if we want to have accurate data, like letting them run under a similar environment. I also reduced many descriptions. The big plan is fulfilling all the descriptions, analyzing 3D data, and providing a more detailed and deeper analysis. There are so many things that can be expanded because of the time limitation. Introduction, research preparation, result presentation and conclusion can be more comprehensive. More ideas are in the proposal.

## Technologies & Libraries
Project is created with:
* Anaconda
* PyTorch
* Lettuce: https://github.com/lettucecfd/lettuce
* PyVista: https://docs.pyvista.org/
* pyevtk
	
## Setup
To run this project, setting up the environment locally by following https://github.com/lettucecfd/lettuce

```
$ conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
$ conda install -c conda-forge pyevtk
```

## Reference
[^1]: https://docs.pyvista.org/
[^2]: https://github.com/lettucecfd/lettuce
