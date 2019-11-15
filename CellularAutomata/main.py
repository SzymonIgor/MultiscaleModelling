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

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk, ImageColor


window = Tk()
window.title('Cellular Automata')
# ************************************************************************
colors = {'0': 'white',
          '1': 'red',
          '2': 'black',
          '3': 'orange',
          '4': 'purple',
          '5': 'yellow',
          '6': 'pink',
          '7': 'blue',
          }

# ************************************************************************

class CellularAutomata:
    def __init__(self):
        self.rows = 50
        self.columns = 50
        self.data = np.zeros([self.rows, self.columns], dtype=int)
        self.generateSeed()

    def get(self):
        return self.data

    def set(self, newData):
        self.data = newData

    def generateSeed(self):
        for i in range(990):
            a = randint(0, 7)
            r = randint(0, self.rows - 1)
            c = randint(0, self.columns - 1)
            self.data[r][c] = a


class FrontEnd(CellularAutomata):
    def __init__(self):
        super().__init__()
        self.w = Canvas(window, width=self.columns, height=self.rows)
        self.w.grid(row=5, column=0)
        self.refresh()

    def create_point(self, x, y, color):
        self.w.create_line(y, x, y + 1, x, fill=color)

    def refresh(self):
        for r in range(self.data.shape[0]):
            for c in range(self.data.shape[1]):
                self.create_point(r, c, colors[str(self.data[r][c])])

    def set(self, data):
        self.data = data
        self.refresh()

    def get(self):
        return self.data


class Functionalities(CellularAutomata):
    def __init__(self):
        CellularAutomata.__init__(self)
        self.operation = None
        self.timeNow = None
        self.fileName = None
        self.currentPath = os.path.dirname(__file__)


    def command_line_executioner(self):
        if self.operation == "Save":
            print('Saving')
            self.saveFile(CellularAutomata.get(self))
        elif self.operation == "Open":
            print('Opening')
            CellularAutomata.set(self, self.openFile())
        elif self.operation == "Seed":
            print("Seeeeding")
            CellularAutomata.generateSeed(self)
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

class ALL(Functionalities, FrontEnd, CellularAutomata):
    def __init__(self):
        Functionalities.__init__()
        FrontEnd.__init__()
        CellularAutomata.__init__()

    def doStuuf(self):
        pass
ButtonCreator("Save", 0, 1)
window.PATH_SAVE = Entry(window, textvariable=None)
window.PATH_SAVE.grid(row=0, column=0)

ButtonCreator("Open", 1, 1)
PATH_OPEN_value = StringVar()
PATH_OPEN_value.set("New")
window.PATH_OPEN = Label(window, textvariable=PATH_OPEN_value)
window.PATH_OPEN.grid(row=1, column=0)

ButtonCreator("Seed", 2, 1)


CA = CellularAutomata()
disp = FrontEnd()








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




def GUI():
    window.update_idletasks()
    window.update()


def update_of_CA():
    disp.refresh()
    # pprint(disp.data)
    print("refreshing")


while 1:
    time.sleep(0.2)
    t2 = threading.Thread(target=GUI())

    t1 = threading.Thread(target=update_of_CA())

    t2.start()
    t1.start()
    t2.join()
    t1.join()
