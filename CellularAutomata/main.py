import os
import csv
from pprint import pprint
from random import randint

import numpy as np
from datetime import datetime
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import threading
import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk, ImageColor


window = Tk()
window.title('Cellular Automata')
# ************************************************************************
colors = {'0': "white",
          '1': "red",
          '2': "black",
          '3': "orange",
          '4': "purple",
          '5': "yellow",
          '6': "pink",
          '7': "blue",
          '8': "gray",
          '9': "crimson",
          '10': "deepskyblue",
          '11': "fuchsia",
          '12': "charteuse"
          }

# ************************************************************************

class FrontEnd:
    def __init__(self):
        self.rows = 100
        self.columns = 100
        self.data = np.zeros([self.rows, self.columns], dtype=int)

        self.w = Canvas(window, height=self.rows, width=self.columns)
        self.w.grid(row=5, column=0)
        self.refresh()




    def create_point(self, x, y, color):
        print(x, y, color)
        self.w.create_line(y, x, y + 1, x, fill=color)

    def refresh(self):
        # print(self.get())

        for r in range(self.rows):
            for c in range(self.columns-1):
                # print(str(self.get()[r][c]))
                self.create_point(r, c, colors[str(self.get()[r][c])])
        time.sleep(0.5)
        window.update_idletasks()
        window.update()


        # print(self.get())
        # print(self.get())

    def set(self, newData):
        self.data = newData
        self.rows = newData.shape[0]
        self.columns = newData.shape[1]
        self.w = Canvas(window, width=self.columns, height=self.rows)
        self.refresh()

    def get(self):
        return self.data

    def generateSeed(self):
        array = np.zeros([self.rows, self.columns], dtype=int)
        # print(f'\n\n Seed generation')
        for i in range(100):
            a = randint(1, 100)
            r = randint(0, self.rows - 1)
            c = randint(0, self.columns - 1)
            array[r][c] = a % 2 + 1
        self.set(array)

    def dilatate(self):
        array = self.data
        array_new = np.zeros([array.shape[0], array.shape[1]], dtype=int)
        for r in range(0, array.shape[0]):
            for c in range(0, array.shape[1]):
                main_new = array[r][c]

                if main_new == 0:
                    try:
                        UL = array[r - 1][c - 1]
                    except:
                        UL = 0
                    try:
                        UU = array[r - 1][c]
                    except:
                        UU = 0
                    try:
                        UR = array[r - 1][c + 1]
                    except:
                        UR = 0

                    try:
                        LL = array[r][c - 1]
                    except:
                        LL = 0
                    try:
                        RR = array[r][c + 1]
                    except:
                        RR = 0

                    try:
                        DL = array[r + 1][c - 1]
                    except:
                        DL = 0
                    try:
                        DD = array[r + 1][c]
                    except:
                        DD = 0

                    try:
                        DR = array[r + 1][c + 1]
                    except:
                        DR = 0

                    temp = [UL, UU, UR, LL, RR, DL, DD, DR]
                    if any(temp) != 0:
                        for x in temp:
                            if x == 0:
                                pass
                            else:
                                main_new = x  # powinno brać to z największą ilością

                    else:
                        main_new = 0
                else:
                    main_new = main_new

                array_new[r][c] = main_new
        self.data = array_new
        self.refresh()

    def dilatate_ALL(self):
        while 1:
            # plt.imshow(self.data)
            if self.data.all() == 0:
                self.dilatate()
                self.get()
            else:
                # plt.show()
                break


class Functionalities:
    FE = FrontEnd()

    def __init__(self):
        self.operation = None
        self.timeNow = None
        self.fileName = None
        self.currentPath = os.path.dirname(__file__)


    def command_line_executioner(self):
        if self.operation == "Save":
            print('Saving')
            # print(self.FE.get())
            self.saveFile(self.FE.get())
        elif self.operation == "Open":
            print('Opening')
            self.FE.set(self.openFile())
        elif self.operation == "Seed":
            print("Seeeeding")
            print(f'OLD\n{self.FE.get()}')
            self.FE.generateSeed()
            print(f'NEW\n{self.FE.get()}')
        else:
            raise NameError

    def saveFile(self, data):
        self.timeNow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        if window.PATH_SAVE.get() == '':
            self.fileName = f'CellularAutomata_{self.timeNow}'
        else:
            self.fileName = window.PATH_SAVE.get()
        with open(str(self.currentPath + r'\\' + str(self.fileName) + '.csv'), 'w', newline='') as file_s:
            np.savetxt(file_s, data, delimiter=',', fmt='%d')

    def openFile(self):
        path = filedialog.askopenfilename(filetypes=(("*.csv", "*.csv"), ("All files", "*.*")))
        self.fileName = os.path.split(path)[-1]
        PATH_OPEN_value.set(self.fileName)
        return np.loadtxt(path, delimiter=',', dtype=int)

class ButtonCreator(Functionalities):
    def __init__(self, name, r, c):
        super().__init__()
        self.operation = name
        self.button = Button(window, text=self.operation, command=self.command_line_executioner, height=1, width=7)
        self.button.grid(row=r, column=c)


ButtonCreator("Save", 0, 1)
window.PATH_SAVE = Entry(window, textvariable=None)
window.PATH_SAVE.grid(row=0, column=0)

ButtonCreator("Open", 1, 1)
PATH_OPEN_value = StringVar()
PATH_OPEN_value.set("New")
window.PATH_OPEN = Label(window, textvariable=PATH_OPEN_value)
window.PATH_OPEN.grid(row=1, column=0)

ButtonCreator("Seed", 2, 1)

fig = Figure(figsize=(5,5), dpi=100)
a = fig.add_subplot(111)





'''
# array = np.ones([500, 500], dtype=int)
# rows = 500
# columns = 500
# array = np.zeros([rows, columns], dtype=int)
# a=0
# for i in np.arange(0, rows-1):
#     for j in np.arange(0, columns-1):
#         for k in range(8):
#             array[i+1, j+1] = a
#             a += 1
#
# print(array)
#
# plt.imshow(array[:, 0:columns+1], interpolation='nearest')
# plt.show()


# array = np.zeros([100, 100], dtype=int)
# for i, item in enumerate(array):
#     array[i] = 0xFF0000
# img = ImageTk.PhotoImage(image=Image.fromarray(array))
#
# canvas = tk.Canvas(window, width=500, height=500)
# canvas.grid(row=2, column=0)
# canvas.create_image(20, 20, anchor="nw", image=img)


# f = Figure(figsize=(10, 10), dpi=100)
# rows = 8
# columns = 8
# canvas = tk.Canvas(window, width=5, height=5, background="white")
# canvas.grid(row=2, column=0)
# canvas[0,0] = "black"


# a = f.add_subplot(111)
# a.plot(array)
# canvas = FigureCanvasTkAgg(f, master=window)
# canvas.draw()
# canvas.get_tk_widget().grid(row=5, column=0)
'''



f = Functionalities()

while 1:
    a.plot(f.FE.get())
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=10, column=0)
    f.FE.dilatate()
    # f.FE.generateSeed()
    # time.sleep(0.2)
    # f.FE.dilatate_ALL()







