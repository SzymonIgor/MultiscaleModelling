import os
import csv
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


# ************************************************************************



class CellularAutomata:
    def __init__(self):
        self.data = np.zeros([50, 50], dtype=int)

    def get(self):
        return self.data

    def refresh(self):
        pass

    def set(self, newData):
        self.data = newData
        self.refresh()




class FileOps:
    def __init__(self):
        self.timeNow = None
        self.fileName = None
        self.currentPath = os.path.dirname(__file__)
        # super().__init__()

    def saveFile(self, data):
        self.timeNow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        print(window.PATH_SAVE.get())
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
        print(np.loadtxt(path, delimiter=',', dtype=int))
        CellularAutomata.get(self)
        return np.loadtxt(path, delimiter=',', dtype=int)



class Functionalities(CellularAutomata, FileOps):
    def __init__(self):
        CellularAutomata.__init__(self)
        FileOps.__init__(self)
        self.operation = None

    def command_line_executioner(self):
        if self.operation == "Save":
            self.saveFile(self.data)
            print('Saving')
        elif self.operation == "Open":
            self.data = self.openFile()
            print('Opening')
        else:
            raise NameError


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



def create_point(x, y, color):
    # mapping kolorów z ID na hex
    w.create_line(y, x, y + 1, x, fill=color)


rows = 50
columns = 50
a = 0
array = np.zeros([rows, columns], dtype=int)
w = Canvas(window, width=columns, height=rows)
w.grid(row=5, column=0)
w.bind("<B1-Motion>")
a = 0
b = 0
c = 0


for i in np.arange(0, rows-1):
    for j in np.arange(1, columns-1):
        create_point(i, j, '#0000' + str(a%10) + '0')

    a += 1
    b += 2
    c += 3




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
    pass
    # PATH_OPEN_value.set("a")


while 1:
    time.sleep(0.01)
    t1 = threading.Thread(target=update_of_CA())
    t2 = threading.Thread(target=GUI())

    t1.start()
    t2.start()
    t1.join()
    t2.join()
