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
import cv2

from numpy.lib.stride_tricks import as_strided


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk, ImageColor


window = Tk()
window.title('Cellular Automata Controls')
# ************************************************************************
colors = {'0': [255, 255, 255],  # white
          '1': [255, 0, 0],
          '2': [240, 5, 10],
          '3': [225, 10, 20],
          '4': [210, 15, 30],
          '5': [195, 20, 40],
          '6': [180, 25, 50],
          '7': [165, 35, 60],
          '8': [150, 40, 70],
          '9': [135, 45, 80],
          '10': [120, 50, 90],
          '11': [105, 55, 100],
          '12': [90, 60, 110],
          '13': [75, 65, 120],
          '14': [60, 70, 130],
          '15': [45, 75, 140],

          '16': [0, 255, 0],
          '17': [10, 240, 5],
          '18': [20, 225, 10],
          '19': [30, 210, 15],
          '20': [40, 195, 20],
          '21': [50, 180, 25],
          '22': [60, 165, 35],
          '23': [70, 150, 40],
          '24': [80, 135, 45],
          '25': [90, 120, 50],
          '26': [100, 105, 55],
          '27': [110, 90, 60],
          '28': [120, 75, 65],
          '29': [130, 60, 70],
          '30': [140, 45, 75],

          '31': [0, 0, 255],
          '32': [5, 10, 240],
          '33': [10, 20, 225],
          '34': [15, 30, 210],
          '35': [20, 40, 195],
          '36': [25, 50, 180],
          '37': [35, 60, 165],
          '38': [40, 70, 150],
          '39': [45, 80, 135],
          '40': [50, 90, 120],
          '41': [55, 100, 105],
          '42': [60, 110, 90],
          '43': [65, 120, 75],
          '44': [70, 130, 60],
          '45': [75, 140, 45],

          '46': [44, 44, 44],
          '47': [90, 60, 90],
          '48': [33, 33, 33],
          '49': [66, 66, 66],
          '50': [99, 99, 99],
          '51': [19, 210, 255],

          }

# ************************************************************************
class CellularAutomata:
    def __init__(self):
        self.rows = 500
        self.columns = 500
        self.data = np.zeros([self.rows, self.columns], dtype=np.uint8)

    def set(self, newData):
        self.data = newData
        self.rows = newData.shape[0]
        self.columns = newData.shape[1]

    def get(self):
        return self.data




class FrontEnd:
    CA = CellularAutomata()

    def __init__(self):
        self.is_procedure = False
        self.grain_quantity = 50

    def set(self, newData):
        self.CA.set(newData)
        self.w = Canvas(window, width=self.CA.columns, height=self.CA.rows)

    def get(self):
        return self.CA.get()

    def dilatate(self):
        array = self.get()
        array_new = np.zeros([array.shape[0], array.shape[1]], dtype=np.uint8)

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
        self.set(array_new)

    def dilatate_is_procedure(self):
        self.is_procedure = not self.is_procedure

    def generateSeed(self, grains):
        self.is_procedure = False
        self.grain_quantity = int(grains)
        array = np.zeros([self.CA.rows, self.CA.columns], dtype=np.uint8)
        # print(f'\n\n Seed generation')
        for color in range(self.grain_quantity):
            r = randint(0, self.CA.rows - 1)
            c = randint(0, self.CA.columns - 1)
            array[r][c] = color
        self.set(array)

    def mappingToImage(self):
        img = np.zeros([self.get().shape[0], self.get().shape[1], 3], dtype=np.uint8)
        array = self.get()
        for r in range(0, array.shape[0]):
            for c in range(0, array.shape[1]):
                id = array[r][c]
                img[r][c] = [0, 0, 0]
                # print("OK")
                # print(img[r][c])
                img[r][c] = colors[str(id)]
        cv2.imshow("Callular Automata Image", img)

    def refresh(self):
        if self.is_procedure is True:
            self.dilatate()
        else:
            pass

        self.mappingToImage()
        window.update_idletasks()
        window.update()
        # time.sleep(0.05)


        # print(self.get())
        # print(self.get())





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
            self.saveFile(self.FE.get())
        elif self.operation == "Export":
            print('Exporting')
            self.exportFile(self.FE.get())
        elif self.operation == "Open":
            print('Opening')
            self.FE.set(self.openFile())
        elif self.operation == "Seed":
            print("Seeding")
            self.FE.generateSeed(window.GRAIN.get())
        elif self.operation == "Once":
            print("Doing Once")
            self.FE.dilatate()
        elif self.operation == "Start/Pause":
            print("Starting/Pausing the Procedure")
            self.FE.dilatate_is_procedure()
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

    def exportFile(self, data):
        self.timeNow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        if window.PATH_EXPORT.get() == '':
            self.fileName = f'Export_{self.timeNow}'
        else:
            self.fileName = window.PATH_EXPORT.get()

        array = []
        with open(str(self.currentPath + r'\\' + str(self.fileName) + '.csv'), 'w', newline='') as file_s:
            for r in range(data.shape[0]):
                for c in range(data.shape[1]):
                    new = [r, c, data[r][c]]
                    array.append(new)
            np.savetxt(file_s, array, delimiter=',', fmt='%d')

    def openFile(self):
        path = filedialog.askopenfilename(filetypes=(("*.csv", "*.csv"), ("All files", "*.*")))
        self.fileName = os.path.split(path)[-1]
        PATH_OPEN_value.set(self.fileName)
        return np.loadtxt(path, delimiter=',', dtype=np.uint8)

class ButtonCreator(Functionalities):
    def __init__(self, name, r, c):
        super().__init__()
        self.operation = name
        self.button = Button(window, text=self.operation, command=self.command_line_executioner, height=1, width=8)
        self.button.grid(row=r, column=c)


ButtonCreator("Save", 0, 1)
window.PATH_SAVE = Entry(window, textvariable=None)
window.PATH_SAVE.grid(row=0, column=0)

ButtonCreator("Export", 1, 1)
window.PATH_EXPORT = Entry(window, textvariable=None)
window.PATH_EXPORT.grid(row=1, column=0)

ButtonCreator("Open", 2, 1)
PATH_OPEN_value = StringVar()
PATH_OPEN_value.set("New")
window.PATH_OPEN = Label(window, textvariable=PATH_OPEN_value)
window.PATH_OPEN.grid(row=2, column=0)

GRAIN_value = IntVar()
GRAIN_value.set(50)
window.GRAIN = Entry(window, textvariable=GRAIN_value)
window.GRAIN.grid(row=0, column=2)

ButtonCreator("Seed", 0, 3)
ButtonCreator("Once", 1, 3)
ButtonCreator("Start/Pause", 2, 3)






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
    f.FE.refresh()








