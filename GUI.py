import tkinter as tk
from tkinter import *

top = tk.Tk()
frame = Frame(top)
frame.pack()
entry_filename = None
e1, e2, e3, e4, e5, e6 = None, None, None, None, None, None

result_dict = dict()
result_dict.update({"D": ""})
result_dict.update({"X": 0})
result_dict.update({"Y": 0})
result_dict.update({"Z": 0})
result_dict.update({"Cylinder": []})
result_dict.update({"Square": []})
result_dict.update({"Rectangle": []})
result_dict.update({"Polygon": []})


def useFile():
    global frame, top, entry_filename
    frame.destroy()
    frame = Frame(top)
    frame.pack()
    tk.Label(frame,
             text="Filename").grid(row=0)
    entry_filename = tk.Entry(frame)
    entry_filename.grid(row=0, column=1)
    tk.Button(frame,
              text='Submit', command=toFileName).grid(row=2,
                                                      column=0,
                                                      sticky=tk.W,
                                                      pady=4)


def toFileName():
    global frame, top, entry_filename
    filename = entry_filename.get()
    print(filename)
    file = open(filename, encoding='utf-8')
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    dimension = ""
    if "2D" in lines[0]:
        dimension = "2D"
    if "3D" in lines[0]:
        dimension = "2D"
    shape = lines[2]
    width = int(shape.split(",")[0])
    height = int(shape.split(",")[1])
    z = 0
    if dimension == "3D":
        z = int(shape.split(",")[2])
    cylinder = []
    square = []
    rectangle = []
    polygon = []
    i = 3

    while i < len(lines):
        line = lines[i]
        if "Cylinder" in line:
            count = int(line.split(" ")[1])
            for j in range(count):
                i += 1
                l = lines[i].split(",")
                x = int(l[0])
                y = int(l[1])
                r = int(l[2])
                cylinder.append((x, y, r))
            i += 1
        if "Square" in line:
            count = int(line.split(" ")[1])
            for j in range(count):
                i += 1
                l = lines[i].split(",")
                x = int(l[0])
                y = int(l[1])
                r = int(l[2])
                square.append((x, y, r))
            i += 1
        if "Rectangle" in line:
            count = int(line.split(" ")[1])
            for j in range(count):
                i += 1
                l = lines[i].split(",")
                x = int(l[0])
                y = int(l[1])
                lx = int(l[2])
                ly = int(l[3])
                rectangle.append((x, y, lx, ly))
            i += 1
        if "Polygon" in line:
            count = int(line.split(" ")[1])
            for j in range(count):
                i += 1
                l = lines[i].split(",")
                print(l)
                p = []
                for k in range(int(len(l) / 2)):
                    p.append((int(l[k * 2][1:]), int(l[k * 2 + 1][:len(l[k * 2 + 1]) - 1])))
                polygon.append(p)
            i += 1
    result_dict.update({"D": dimension})
    result_dict.update({"X": width})
    result_dict.update({"Y": height})
    if dimension == "3D":
        result_dict.update({"Z": z})
    result_dict.update({"Cylinder": cylinder})
    result_dict.update({"Square": square})
    result_dict.update({"Rectangle": rectangle})
    result_dict.update({"Polygon": polygon})
    top.destroy()


def useWindows():
    global frame, top, e1, e2, e3, e4, e5, e6
    frame.destroy()
    frame = Frame(top)
    frame.pack()
    tk.Label(frame,
             text="Width").grid(row=0)
    tk.Label(frame,
             text="Height").grid(row=1)
    e1 = tk.Entry(frame)
    e2 = tk.Entry(frame)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    tk.Label(frame,
             text="Cylinder").grid(row=2)
    tk.Label(frame,
             text="Square").grid(row=3)
    e3 = tk.Entry(frame)
    e4 = tk.Entry(frame)

    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)

    tk.Label(frame,
             text="Rectangle").grid(row=4)
    tk.Label(frame,
             text="Polygon").grid(row=5)
    e5 = tk.Entry(frame)
    e6 = tk.Entry(frame)

    e5.grid(row=4, column=1)
    e6.grid(row=5, column=1)

    tk.Button(frame,
              text='Submit', command=readData).grid(row=6,
                                                    column=0,
                                                    sticky=tk.W,
                                                    pady=4)


def readData():
    global frame, top, e1, e2, e3, e4, e5, e6
    X = int(e1.get())
    Y = int(e2.get())
    cylinder = []
    if len(e3.get()) > 0:
        for j in e3.get().split("|"):
            print(j)
            l = j.split(",")
            x = int(l[0])
            y = int(l[1])
            r = int(l[2])
            cylinder.append((x, y, r))

    square = []
    if len(e4.get()) > 0:
        for j in e4.get().split("|"):
            l = j.split(",")
            x = int(l[0])
            y = int(l[1])
            r = int(l[2])
            square.append((x, y, r))

    rectangle = []
    if len(e5.get()) > 0:
        for j in e5.get().split("|"):
            l = j.split(",")
            x = int(l[0])
            y = int(l[1])
            lx = int(l[2])
            ly = int(l[3])
            rectangle.append((x, y, lx, ly))

    polygon = []
    if len(e6.get()) > 0:
        for j in e6.get().split("|"):
            l = j.split(",")
            p = []
            for k in range(int(len(l) / 2)):
                p.append((int(l[k * 2][1:]), int(l[k * 2 + 1][:len(l[k * 2 + 1]) - 1])))
            polygon.append(p)

    result_dict.update({"X": X})
    result_dict.update({"Y": Y})
    result_dict.update({"Cylinder": cylinder})
    result_dict.update({"Square": square})
    result_dict.update({"Rectangle": rectangle})
    result_dict.update({"Polygon": polygon})
    top.destroy()


def GUI():
    tk.Button(frame,
              text='Use GUI',
              command=useWindows).grid(row=3,
                                       column=0,
                                       sticky=tk.W,
                                       pady=4)
    tk.Button(frame,
              text='Use file', command=useFile).grid(row=3,
                                                     column=1,
                                                     sticky=tk.W,
                                                     pady=4)
    # tk.Button(top,
    #           text='', command=submitFile).grid(row=3,
    #                                                     column=3,
    #                                                     sticky=tk.W,
    #                                                     pady=4)
    # canvas = Canvas(top, width=100, height=100)
    # canvas.bind("<Key>", key)
    # canvas.bind("<Button-1>", callback)
    # canvas.pack()
    top.mainloop()
    print(result_dict)
    return result_dict
