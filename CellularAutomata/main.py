import os

from random import randint
import numpy as np
from datetime import datetime
from tkinter import *
from tkinter import filedialog
import cv2
from scipy import ndimage



import matplotlib
matplotlib.use("TkAgg")



window = Tk()
window.title('Cellular Automata Controls')
# ************************************************************************
colors = {'0': [255, 255, 255],  # white

          '1':  [255,  45, 150],
          '2':  [240,  60, 135],
          '3':  [225,  75, 120],
          '4':  [210,  90, 105],
          '5':  [195, 105,  90],
          '6':  [180, 120,  75],
          '7':  [165, 135,  60],
          '8':  [150, 150,  45],
          '9':  [135, 165, 255],
          '10': [120, 180, 240],
          '11': [105, 195, 225],
          '12': [ 90, 210, 210],
          '13': [ 75, 225, 195],
          '14': [ 60, 240, 180],
          '15': [ 45, 255, 165],

          '16': [ 150, 255,  45],
          '17': [ 135, 240,  60],
          '18': [ 120, 225,  75],
          '19': [ 105, 210,  90],
          '20': [  90, 195, 105],
          '21': [  75, 180, 120],
          '22': [  60, 165, 135],
          '23': [  45, 150, 150],
          '24': [ 255, 135, 165],
          '25': [ 240, 120, 180],
          '26': [ 225, 105, 195],
          '27': [ 210,  90, 210],
          '28': [ 195,  75, 225],
          '29': [ 180,  60, 240],
          '30': [ 165,  45, 255],

          '31': [ 45,  150, 255],
          '32': [ 60,  135, 240],
          '33': [ 75,  120, 225],
          '34': [ 90,  105, 210],
          '35': [105,   90, 195],
          '36': [120,   75, 180],
          '37': [135,   60, 165],
          '38': [150,   45, 150],
          '39': [165,  255, 135],
          '40': [180,  240, 120],
          '41': [195,  225, 105],
          '42': [210,  210,  90],
          '43': [225,  195,  75],
          '44': [240,  180,  60],
          '45': [255,  165,  45],

          '46': [222,  44,  11],
          '47': [ 90,  6,  90],
          '48': [190,  0,  33],
          '49': [ 15,  66, 150],
          '50': [ 99, 225,   8],
          '51': [ 19, 210, 255],

          }

# ************************************************************************
class CellularAutomata:
    KERNEL_MOOR = np.ones([3, 3], dtype=np.uint8)
    KERNEL_CROSS = np.array([[0, 1, 0],
                             [1, 1, 1],
                             [0, 1, 0]])
    KERNEL_PENTA_LEFT = np.array([[0, 1, 1],
                                  [0, 1, 1],
                                  [0, 1, 1]])
    KERNEL_PENTA_RIGHT = np.array([[1, 1, 0],
                                   [1, 1, 0],
                                   [1, 1, 0]])
    KERNEL_HEXA_LEFT = np.array([[0, 1, 1],
                                 [1, 1, 1],
                                 [1, 1, 0]])
    KERNEL_HEXA_RIGHT = np.array([[1, 1, 0],
                                  [1, 1, 1],
                                  [0, 1, 1]])
    KERNEL = [KERNEL_MOOR, KERNEL_CROSS, KERNEL_PENTA_LEFT, KERNEL_PENTA_RIGHT, KERNEL_HEXA_LEFT, KERNEL_HEXA_RIGHT]
    ROWS_NO = 500
    COLUMNS_NO = 500

    def __init__(self):
        self.rows = self.ROWS_NO
        self.columns = self.COLUMNS_NO
        self.kernel = self.KERNEL_MOOR
        self.data = np.zeros([self.rows, self.columns], dtype=np.uint8)
        self.is_procedure = False
        self.grain_quantity = 50
        self.is_random = 0

    def set(self, newData):
        self.data = newData
        self.rows = newData.shape[0]
        self.columns = newData.shape[1]

    def get(self):
        return self.data

    def reset(self):
        self.rows = self.ROWS_NO
        self.columns = self.COLUMNS_NO
        self.data = np.zeros([self.rows, self.columns], dtype=np.uint8)

    def updateKernel(self):
        if self.is_random == 1:
            i = randint(0, 100)
            i %= 4
            i %= 2

            if np.array_equal(self.kernel, self.KERNEL_MOOR) or np.array_equal(self.kernel, self.KERNEL_CROSS):
                self.kernel = self.kernel
            elif np.array_equal(self.kernel, self.KERNEL_PENTA_LEFT):
                self.kernel = self.KERNEL[2+i]
            elif np.array_equal(self.kernel, self.KERNEL_PENTA_RIGHT):
                self.kernel = self.KERNEL[3-i]
            elif np.array_equal(self.kernel, self.KERNEL_HEXA_LEFT):
                self.kernel = self.KERNEL[4+i]
            elif np.array_equal(self.kernel, self.KERNEL_HEXA_RIGHT):
                self.kernel = self.KERNEL[5-i]
            else:
                print("ERROR")
        else:
            self.kernel = self.kernel

    def generateSeed(self, grains):
        self.is_procedure = False
        self.grain_quantity = int(grains)
        array = np.zeros([self.rows, self.columns], dtype=np.uint8)
        # print(f'\n\n Seed generation')
        for color in range(self.grain_quantity):
            r = randint(0, self.rows - 1)
            c = randint(0, self.columns - 1)
            array[r][c] = color % 51 + 1
        self.set(array)

    def dilatate_is_procedure(self):
        self.is_procedure = not self.is_procedure

    def dilatate(self):
        array = self.get()

        dilation = ndimage.grey_dilation(array, footprint=self.kernel)
        self.updateKernel()
        array_new = np.array([[array[x][y] if array[x][y] != 0 else dilation[x][y] for y in range(array.shape[1])] for x in range(array.shape[0])])

        if np.array_equal(np.array(array_new), np.array(self.get())):
            self.is_procedure = 0
            print("END")
        else:
            self.is_procedure = self.is_procedure

        self.set(array_new)


class FrontEnd(CellularAutomata):
    def __init__(self):
        super().__init__()
        self.img = np.zeros([self.get().shape[0], self.get().shape[1], 3], dtype=np.uint8)

    def mappingToImage(self):
        img = np.zeros([self.get().shape[0], self.get().shape[1], 3], dtype=np.uint8)
        array = self.get()
        for r in range(0, array.shape[0]):
            for c in range(0, array.shape[1]):
                id = array[r][c]
                img[r][c] = [0, 0, 0]
                img[r][c] = colors[str(id)]
        self.img = img

    def showImage(self):
        cv2.imshow("Callular Automata Image", self.img)

    def refresh(self):
        # print(f'0 {datetime.now()}')
        if self.is_procedure is True:
            self.dilatate()
        else:
            self.mappingToImage()
            self.showImage()
        window.update_idletasks()
        window.update()


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
            print(window.LIST.curselection()[0])
            self.FE.generateSeed(window.GRAIN.get())
        elif self.operation == "Once":
            print("Doing Once")
            self.FE.kernel = self.FE.KERNEL[window.LIST.curselection()[0]]
            self.FE.is_random = RANDOM_BOX_VALUE.get()
            self.FE.dilatate()
        elif self.operation == "Start/Pause":
            print("Starting/Pausing the Procedure")
            self.FE.kernel = self.FE.KERNEL[window.LIST.curselection()[0]]
            self.FE.is_random = RANDOM_BOX_VALUE.get()
            self.FE.dilatate_is_procedure()
        elif self.operation == "RST":
            print("Resetting data")
            self.FE.reset()
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


window.EMPTY1 = Label(window, width=15)
window.EMPTY1.grid(row=0, column=3)


GRAIN_value = IntVar()
GRAIN_value.set(50)
window.GRAIN = Entry(window, textvariable=GRAIN_value)
window.GRAIN.grid(row=0, column=4)

window.LIST = Listbox(window, height=6, bd=1)
window.LIST.insert(0, "MOOR")
window.LIST.insert(1, "VON_NEUMANN")
window.LIST.insert(2, "PENTA_LEFT")
window.LIST.insert(3, "PENTA_RIGHT")
window.LIST.insert(4, "HEXA_LEFT")
window.LIST.insert(5, "HEXA_RIGHT")
window.LIST.select_set(0)
window.LIST.grid(row=3, column=4, rowspan=20)


ButtonCreator("Seed", 0, 5)

ButtonCreator("RST", 1, 5)

window.EMPTY2 = Label(window, height=1)
window.EMPTY2.grid(row=2, column=5)

ButtonCreator("Once", 3, 5)

ButtonCreator("Start/Pause", 4, 5)

RANDOM_BOX_VALUE = IntVar()
window.RANDOM_BOX = Checkbutton(window, text="Random", variable=RANDOM_BOX_VALUE)
window.RANDOM_BOX.grid(row=5, column=5)


f = Functionalities()

while 1:
    f.FE.refresh()


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
