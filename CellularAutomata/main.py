import os

from random import randint
import numpy as np
from datetime import datetime, time
from tkinter import *
from tkinter import filedialog
import cv2
from scipy import ndimage
from PIL import Image, ImageTk
import collections
from threading import Thread
from collections import defaultdict
import time

window = Tk()
window.title('Cellular Automata Controls')
# ************************************************************************
colors = {0: [255, 255, 255],  # white
          1: [0, 0, 0],  # inclusion
          2: [0, 0, 0],  # boundary
          3: [0, 0, 255],
          4: [109, 29, 196],
          5: [148, 30, 189],
          6: [211, 53, 255],
          7: [249, 22, 158],
          8: [196, 66, 216],
          9: [98, 93, 132],
          10: [61, 34, 247],
          11: [130, 143, 63],
          12: [50, 64, 173],
          13: [145, 27, 141],
          14: [233, 138, 94],
          15: [243, 78, 54],
          16: [105, 95, 205],
          17: [240, 11, 119],
          18: [230, 102, 94],
          19: [117, 134, 106],
          20: [233, 44, 99],
          21: [159, 65, 75],
          22: [152, 2, 196],
          23: [230, 52, 71],
          24: [171, 115, 178],
          25: [61, 7, 226],
          26: [232, 25, 147],
          27: [199, 34, 92],
          28: [96, 121, 210],
          29: [233, 73, 243],
          30: [86, 71, 192],
          31: [92, 1, 245],
          32: [245, 65, 148],
          33: [203, 66, 146],
          34: [232, 104, 154],
          35: [155, 135, 83],
          36: [53, 13, 83],
          37: [192, 98, 96],
          38: [80, 37, 233],
          39: [108, 29, 200],
          40: [116, 118, 119],
          41: [108, 54, 198],
          42: [84, 141, 210],
          43: [219, 64, 182],
          44: [249, 121, 235],
          45: [155, 144, 206],
          46: [82, 55, 139],
          47: [103, 116, 128],
          48: [181, 89, 237],
          49: [60, 39, 158],
          50: [70, 27, 226],
          51: [131, 17, 227],
          52: [120, 114, 112],
          53: [121, 27, 204],
          54: [242, 130, 202],
          55: [159, 76, 192],
          56: [71, 103, 71],
          57: [67, 4, 142],
          58: [89, 105, 98],
          59: [119, 87, 71],
          60: [171, 53, 121],
          61: [85, 7, 112],
          62: [142, 19, 59],
          63: [76, 131, 112],
          64: [164, 27, 242],
          65: [112, 15, 73],
          66: [84, 104, 93],
          67: [117, 6, 59],
          68: [115, 128, 148],
          69: [75, 115, 157],
          70: [245, 106, 242],
          71: [128, 150, 113],
          72: [220, 134, 76],
          73: [192, 14, 73],
          74: [57, 69, 178],
          75: [137, 43, 229],
          76: [182, 59, 207],
          77: [232, 81, 141],
          78: [228, 32, 89],
          79: [142, 21, 123],
          80: [237, 7, 63],
          81: [53, 97, 228],
          82: [148, 134, 66],
          83: [149, 59, 202],
          84: [51, 9, 67],
          85: [194, 22, 125],
          86: [58, 6, 107],
          87: [54, 115, 122],
          88: [106, 68, 118],
          89: [95, 24, 197],
          90: [56, 139, 145],
          91: [112, 43, 88],
          92: [248, 82, 164],
          93: [117, 33, 245],
          94: [76, 112, 118],
          95: [153, 121, 96],
          96: [62, 0, 193],
          97: [155, 148, 167],
          98: [61, 115, 107],
          99: [175, 123, 136],
          100: [140, 64, 191],
          101: [86, 52, 134],
          102: [180, 14, 91],
          103: [242, 109, 177],
          104: [236, 141, 217],
          105: [236, 83, 147],
          106: [120, 13, 89],
          107: [226, 121, 158],
          108: [184, 41, 220],
          109: [52, 110, 79],
          110: [52, 113, 113],
          111: [147, 53, 110],
          112: [89, 70, 216],
          113: [104, 94, 234],
          114: [240, 134, 96],
          115: [243, 86, 106],
          116: [68, 83, 114],
          117: [68, 128, 190],
          118: [138, 59, 250],
          119: [147, 3, 90],
          120: [174, 125, 191],
          121: [120, 52, 119],
          122: [244, 116, 237],
          123: [172, 81, 141],
          124: [242, 20, 189],
          125: [74, 100, 175],
          126: [64, 143, 191],
          127: [175, 1, 89],
          128: [123, 149, 58],
          129: [172, 129, 58],
          130: [192, 73, 60],
          131: [131, 142, 56],
          132: [174, 59, 85],
          133: [229, 143, 165],
          134: [68, 14, 74],
          135: [204, 91, 230],
          136: [109, 25, 249],
          137: [190, 145, 179],
          138: [221, 3, 182],
          139: [202, 76, 70],
          140: [53, 51, 229],
          141: [220, 67, 246],
          142: [202, 118, 51],
          143: [90, 133, 110],
          144: [77, 142, 71],
          145: [209, 93, 95],
          146: [117, 57, 231],
          147: [145, 17, 251],
          148: [179, 143, 77],
          149: [191, 30, 220],
          150: [101, 121, 70],
          151: [85, 122, 187],
          152: [170, 11, 199],
          153: [132, 133, 243],
          154: [233, 79, 241],
          155: [216, 27, 162],
          156: [114, 80, 112],
          157: [196, 36, 179],
          158: [170, 46, 176],
          159: [72, 132, 99],
          160: [195, 50, 121],
          161: [241, 95, 197],
          162: [136, 95, 150],
          163: [162, 26, 158],
          164: [180, 52, 143],
          165: [199, 71, 227],
          166: [178, 131, 182],
          167: [129, 144, 147],
          168: [137, 97, 222],
          169: [56, 22, 248],
          170: [229, 15, 231],
          171: [238, 126, 192],
          172: [111, 103, 80],
          173: [99, 148, 101],
          174: [161, 102, 115],
          175: [147, 73, 79],
          176: [237, 63, 210],
          177: [87, 63, 114],
          178: [196, 104, 80],
          179: [109, 5, 249],
          180: [106, 1, 123],
          181: [127, 29, 204],
          182: [232, 67, 98],
          183: [239, 128, 146],
          184: [213, 84, 215],
          185: [158, 70, 77],
          186: [248, 38, 238],
          187: [155, 136, 197],
          188: [238, 80, 89],
          189: [159, 29, 234],
          190: [81, 144, 80],
          191: [122, 64, 67],
          192: [239, 132, 186],
          193: [154, 32, 225],
          194: [149, 142, 142],
          195: [255, 111, 181],
          196: [144, 35, 242],
          197: [146, 31, 105],
          198: [92, 11, 226],
          199: [101, 57, 214],
          200: [79, 142, 117],
          201: [229, 22, 214],
          202: [65, 79, 55],
          203: [97, 136, 69],
          204: [92, 113, 208],
          205: [232, 87, 126],
          206: [203, 98, 234],
          207: [212, 54, 189],
          208: [50, 53, 148],
          209: [69, 58, 203],
          210: [53, 25, 237],
          211: [170, 143, 85],
          212: [88, 70, 243],
          213: [214, 131, 176],
          214: [230, 111, 100],
          215: [66, 111, 54],
          216: [160, 36, 164],
          217: [163, 67, 132],
          218: [83, 43, 112],
          219: [82, 89, 211],
          220: [98, 129, 252],
          221: [130, 76, 173],
          222: [224, 49, 128],
          223: [130, 116, 218],
          224: [158, 131, 204],
          225: [99, 96, 99],
          226: [213, 10, 56],
          227: [190, 46, 85],
          228: [220, 64, 151],
          229: [126, 28, 177],
          230: [82, 89, 106],
          231: [223, 85, 79],
          232: [253, 89, 147],
          233: [69, 8, 157],
          234: [152, 64, 219],
          235: [83, 53, 204],
          236: [172, 21, 166],
          237: [164, 5, 155],
          238: [189, 112, 168],
          239: [213, 82, 109],
          240: [106, 0, 197],
          241: [165, 9, 181],
          242: [209, 46, 177],
          243: [254, 120, 63],
          244: [136, 39, 58],
          245: [246, 141, 188],
          246: [80, 146, 109],
          247: [163, 55, 252],
          248: [138, 74, 180],
          249: [235, 86, 226],
          250: [74, 58, 131],
          251: [205, 128, 111],
          252: [160, 31, 216],
          253: [178, 35, 232],
          254: [186, 56, 128],
          255: [50, 10, 79],
          256: [246, 88, 213],
          257: [128, 144, 83],
          258: [77, 15, 212],
          259: [136, 116, 168],
          260: [57, 128, 50],
          261: [233, 132, 105],
          262: [233, 5, 145],
          263: [208, 125, 236],
          264: [101, 6, 89],
          265: [183, 17, 101],
          266: [244, 48, 196],
          267: [77, 15, 149],
          268: [135, 6, 152],
          269: [116, 1, 248],
          270: [239, 12, 238],
          271: [142, 72, 203],
          272: [201, 45, 197],
          273: [127, 85, 215],
          274: [124, 138, 200],
          275: [154, 137, 55],
          276: [126, 128, 160],
          277: [99, 141, 78],
          278: [243, 112, 93],
          279: [52, 61, 147],
          280: [84, 96, 95],
          281: [132, 134, 132],
          282: [168, 70, 129],
          283: [247, 33, 51],
          284: [76, 83, 180],
          285: [153, 8, 175],
          286: [112, 72, 221],
          287: [227, 107, 240],
          288: [119, 39, 63],
          289: [173, 141, 246],
          290: [150, 107, 174],
          291: [250, 109, 207],
          292: [136, 8, 111],
          293: [186, 69, 174],
          294: [250, 45, 200],
          295: [129, 32, 110],
          296: [141, 15, 101],
          297: [75, 85, 149],
          298: [82, 145, 192],
          299: [79, 87, 152],
          300: [186, 36, 212],
          301: [88, 26, 167]
          }

KERNELS = {0: "MOORE",
           1: "VON_NEUMANN",
           2: "PENTA_LEFT",
           3: "PENTA_RIGHT",
           4: "HEXA_LEFT",
           5: "HEXA_RIGHT"
           }
# ************************************************************************


class CellularAutomata:
    ROWS_NO = 500
    COLUMNS_NO = 500

    KERNEL_FULL = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 0), (0, 1),
                    (1, -1), (1, 0), (1, 1)]
    KERNEL_MOORE = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 1),
                    (1, -1), (1, 0), (1, 1)]
    KERNEL_CROSS = [(-1, 0),
                    (0, -1), (0, 1),
                    (1, 0)]
    KERNEL_PENTA_LEFT = [(-1, -1), (-1, 0),
                         (0, -1),
                         (1, -1), (1, 0)]
    KERNEL_PENTA_RIGHT = [(-1, 0), (-1, 1),
                          (0, 1),
                          (1, 0), (1, 1)]
    KERNEL_HEXA_LEFT = [(-1, -1), (-1, 0),
                        (0, -1), (0, 1),
                        (1, 0), (1, 1)]
    KERNEL_HEXA_RIGHT = [(-1, 0), (-1, 1),
                         (0, -1), (0, 1),
                         (1, -1), (1, 0)]
    KERNEL_NEAREST_MOORE = KERNEL_CROSS
    KERNEL_FURTHER_MOORE = [(-1, -1), (-1, 1),
                            (1, -1), (1, 1)]
    KERNEL = [KERNEL_MOORE, KERNEL_CROSS, KERNEL_PENTA_LEFT, KERNEL_PENTA_RIGHT, KERNEL_HEXA_LEFT, KERNEL_HEXA_RIGHT]
    TYPES = ["constant", "wrap"]

    def __init__(self):
        self.rows = self.ROWS_NO
        self.columns = self.COLUMNS_NO
        self.kernel = self.KERNEL_MOORE
        self.data = np.zeros([self.rows, self.columns], dtype=np.uint8)
        self.type = self.TYPES[0]
        self.is_procedure = False
        self.grain_quantity = 50
        self.is_random = 0
        self.GBC = 0
        self.GBC_threshold = 0
        self.no_changes_counter = 0
        self.inclusions_q = 1
        self.inclusions_r_min = 1
        self.inclusions_r_max = 10
        self.frozen = []
        self.firstPhase = np.zeros([self.rows, self.columns], dtype=np.uint8)
        self.boundary = np.zeros([self.rows, self.columns], dtype=np.bool)
        self.avg_grain_size = None
        self.border_length = {}


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
        self.is_procedure = False

    def init(self):
        self.set(np.zeros([self.rows, self.columns], dtype=np.uint8))
        self.is_procedure = False
        self.firstPhase = np.zeros([self.rows, self.columns], dtype=np.uint8)
        self.frozen = []
        self.boundary = np.zeros([self.rows, self.columns], dtype=np.bool)

    def update_kernel(self):
        if self.is_random == 1:
            i = randint(0, 100)
            i %= 4
            i %= 2

            if np.array_equal(self.kernel, self.KERNEL_MOORE) or np.array_equal(self.kernel, self.KERNEL_CROSS):
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

    def only_inclusions(self):
        a = self.data
        a = np.array([[a[r][c] if a[r][c] == 1 else 0 for c in range(self.columns)] for r in range(self.rows)])
        return a

    def only_grains(self):
        a = self.data
        a = np.array([[a[r][c] if a[r][c] >= 3 else 0 for c in range(self.columns)] for r in range(self.rows)])
        return a

    def only_first_phase(self):
        a = self.data
        a = np.array([[a[r][c] if self.firstPhase[r][c] == 1 else 0 for c in range(self.columns)] for r in range(self.rows)])
        return a

    def only_boundaries(self):
        a = self.data
        a = np.array([[a[r][c] if self.boundary[r][c] else 0 for c in range(self.columns)] for r in range(self.rows)])
        return a

    def create_circular_mask(self, h, w, center=None, radius=None):

        if center is None:  # use the middle of the image
            center = [int(w / 2), int(h / 2)]
        if radius is None:  # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w - center[0], h - center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

        mask = dist_from_center <= radius
        return mask

    def gen_circle(self, cx, cy, radius=None):
        a = self.get()
        if radius == 0.5:
            a[cy, cx] = 1
        else:
            radius = int(radius)
            a[self.create_circular_mask(self.rows, self.columns, [cy, cx], radius)] = 1
            # y, x = np.ogrid[-radius: radius, -radius: radius]
            # index = x ** 2 + y ** 2 <= radius ** 2
            # a[max(cy - radius, 0):min(cy + radius, self.rows), max(cx - radius, 0):min(cx + radius, self.columns)][index] = 1
        self.set(np.array(a))

    def generate_inclusions(self):
        array = self.only_grains()
        self.set(array)
        for i in range(self.inclusions_q):
            array = self.get()
            r = randint(self.inclusions_r_min, self.inclusions_r_max)
            watch_dog = 100
            while watch_dog:
                watch_dog -= 1
                if watch_dog == 0:
                    raise Exception("Cannot find place for inclusion")
                y = randint(0, self.rows-1)
                x = randint(0, self.columns-1)
                if array[y][x] == 0:
                    self.gen_circle(x, y, r)
                    break
                else:
                    pass

    def generate_seed(self, grains):
        self.boundary = np.zeros([self.rows, self.columns], dtype=np.bool)

        self.grain_quantity = int(grains)
        array = self.get()
        # print(f'\n\n Seed generation')
        for grainID in range(self.grain_quantity):
            grainID = np.amax(self.data) + 1
            watch_dog = 1000
            while watch_dog:
                watch_dog -= 1
                r = randint(0, self.rows - 1)
                c = randint(0, self.columns - 1)
                if array[r][c] != 0 or array[r][c] == 1:
                    if watch_dog == 0:
                        raise Exception("Cannot find enough free space to insert every seed")
                else:
                    array[r][c] = (grainID if np.amax(self.data) != 0 and np.amax(self.data) != 1 else 3)
                    break
        self.set(array)

    def dilatate_is_procedure(self):
        self.is_procedure = not self.is_procedure

    def dilatate_ALL(self):
         while self.is_procedure == 1:
             self.dilatate()

    def dilatate_base_type(self, r, c):
        array = self.get()
        self.boundary = np.zeros([self.rows, self.columns], dtype=np.bool)
        if array[r][c] != 0 or array[r][c] == 1:
            new_value = [(array[r][c], 0)]
            quantity = 0
        else:
            neighbours = []
            quantity = 0
            for item in self.kernel:
                r_n = r + item[0]
                c_n = c + item[1]
                if (0 <= r_n <= array.shape[0] - 1) and (0 <= c_n <= array.shape[1] - 1):
                    neighbour = array[r_n, c_n]
                else:
                    if self.type == 0:
                        neighbour = 0
                    elif self.type == 1:
                        r_n = self.wrapping(r_n, array.shape[0])
                        c_n = self.wrapping(c_n, array.shape[1])
                        neighbour = array[r_n, c_n]
                    else:
                        raise ValueError("Wrong type given")
                if any([neighbour == 0, neighbour == 1,  (any(neighbour == x for x in self.frozen))]):
                    pass
                else:
                    neighbours.append(neighbour)

            if not neighbours:
                new_value = [(0, 0)]
            else:
                new_value = collections.Counter(neighbours).most_common(8)

        return new_value

    def dilatate_base(self):
        array = self.get()
        array_new = np.zeros([array.shape[0], array.shape[1]], dtype=np.uint8)
        for r in range(array.shape[0]):
            for c in range(array.shape[1]):
                new_value, quantity = self.dilatate_base_type(r, c)[0]
                if self.GBC == 1:
                    if quantity == 0:
                        array_new[r][c] = new_value
                    else:
                        if quantity >= 5:
                            array_new[r][c] = new_value
                        else:
                            self.kernel = self.KERNEL_NEAREST_MOORE
                            new_value, quantity = self.dilatate_base_type(r, c)[0]
                            if quantity >= 3:
                                array_new[r][c] = new_value
                            else:
                                self.kernel = self.KERNEL_FURTHER_MOORE
                                new_value, quantity = self.dilatate_base_type(r, c)[0]
                                if quantity >= 3:
                                    array_new[r][c] = new_value
                                else:
                                    self.kernel = self.KERNEL_MOORE
                                    new_value, quantity = self.dilatate_base_type(r, c)[0]
                                    if randint(0, 100) < self.GBC_threshold:
                                        array_new[r][c] = new_value
                                    else:
                                        array_new[r][c] = 0
                    self.kernel = self.KERNEL_MOORE
                else:
                    array_new[r][c] = new_value

            # window.update_id
        return array_new

    def dilatate(self):
        array = self.get()

        arr_inclusions = np.array([[array[x][y] if (array[x][y] == 1) else 0 for y in range(array.shape[1])]
                              for x in range(array.shape[0])])
        array_only_grains = array - arr_inclusions

        # dilation = ndimage.grey_dilation(array_only_grains, footprint=self.kernel, mode='constant') if self.type == 0 \
        #     else ndimage.grey_dilation(array_only_grains, footprint=self.kernel, mode='wrap')

        dilatated = self.dilatate_base()

        self.update_kernel()
        array_new = np.array([[array[x][y] if (array[x][y] != 0 or array[x][y] == 1) else dilatated[x][y] for y in range(array.shape[1])]
                              for x in range(array.shape[0])])
        array_new = np.array([[array_new[x][y] if array[x][y] != 1 else arr_inclusions[x][y] for y in range(array.shape[1])]
                              for x in range(array.shape[0])])
        if np.array_equal(np.array(array_new), np.array(self.get())):
            self.no_changes_counter += 1
            if self.no_changes_counter >= 10:
                print(f"END - due to no changes (same for {self.no_changes_counter} times. CA is not complete")
                self.is_procedure = 0
            else:
                pass
        else:
            self.no_changes_counter = 0
            if np.all(np.array(array_new)): # np.array_equal(np.array(array_new), np.array(self.get())):
                self.is_procedure = 0
                print("END")
            else:
                self.is_procedure = self.is_procedure
        self.set(array_new)

    def wrapping(self, number, r):
        if number >= r:
            new_no = 0
        elif number < 0:
            new_no = r - 1
        else:
            new_no = number
        return new_no

    def delete_grainID(self, grainID):
        array = self.get()
        array = np.array([[(0 if array[r][c] == grainID and all(array[r][c] != x for x in self.frozen) and array[r][c] != 1 else array[r][c]) for c in range(array.shape[1])] for r in range(array.shape[0])])
        self.set(array)

    def substructures_feature(self):
        array = self.get()
        [[self.frozen.append(array[r][c]) if (array[r][c] != 0 and array[r][c] != 1) else None for c in
        range(array.shape[1])] for r in range(array.shape[0])]
        self.frozen = list(set(self.frozen))

    def dual_phase_feature(self):
        array = self.get()
        [[self.frozen.append(array[r][c]) if (array[r][c] != 0 and array[r][c] != 1) else None for c in range(array.shape[1])] for r in range(array.shape[0])]
        self.frozen = list(set(self.frozen))

        self.firstPhase = [[1 if (array[r][c] != 0 and array[r][c] != 1) else 2 for c in range(array.shape[1])] for r in range(array.shape[0])]


    def get_phase(self):
        return self.firstPhase

    def get_boundaries(self):
        return self.boundary

    def check_boundaries(self):
        array = self.get()
        self.boundary = np.zeros([self.rows, self.columns], dtype=np.bool)
        temp_avg = defaultdict(lambda: 0)
        temp_bl = defaultdict(lambda: 0)
        for r in range(array.shape[0]):
            for c in range(array.shape[1]):
                if array[r][c] == 0 or array[r][c] == 1 or array[r][c] == 2:
                    pass
                else:
                    neighbours = []
                    for item in self.KERNEL_FULL:
                        r_n = r + item[0]
                        c_n = c + item[1]
                        if (0 <= r_n <= array.shape[0] - 1) and (0 <= c_n <= array.shape[1] - 1):
                            neighbour = array[r_n, c_n]
                        else:
                            neighbour = 0

                        neighbours.append(neighbour)
                    if len(collections.Counter(neighbours)) == 1:
                        self.boundary[r][c] = False
                    else:
                        self.boundary[r][c] = True

                    if self.boundary[r][c]:
                        temp_bl[array[r][c]] += 1

                    temp_avg[array[r][c]] += 1
        try:
            self.avg_grain_size = sum(temp_avg.values()) / len(temp_avg)
        except:
            pass

        self.border_length = dict(temp_bl)

class FrontEnd(CellularAutomata):
    def __init__(self):
        super().__init__()
        self.img = np.zeros([self.get().shape[0], self.get().shape[1], 3], dtype=np.uint8)
        # cv2.imshow("Callular Automata Image", self.img)
        b, g, r = cv2.split(self.img)
        self.show = cv2.merge((r, g, b))
        self.show = Image.fromarray(self.show)
        self.refresh()

    def callback(self, event):
        if DELETE_BY_CLICK_VALUE.get() == 1:
            array = self.get()
            print(f'clicked at: {event.x},{event.y}\nGrainID: {array[event.y][event.x]}')
            self.delete_grainID(array[event.y][event.x])

    def map_to_image(self, array=None, change_order=True):
        try:
            if array is None:
                array = self.get()
                img = np.array([[colors[array[r][c] % 301] if self.boundary[r][c] != True else colors[2] for c in range(self.columns)] for r in range(self.rows)], dtype=np.uint8)
            else:
                img = np.array([[colors[array[r][c] % 301] for c in range(self.columns)] for r in range(self.rows)], dtype=np.uint8)
        except:
            img = self.img

        if change_order is False:
            pass
        else:
            b, g, r = cv2.split(img)
            img = cv2.merge((r, g, b))
        # cv2.imshow("Callular Automata Image", self.img)

        self.img = img
        return self.img

    def refresh(self):
        # print(f'0 {datetime.now()}')
        if self.is_procedure is True:
            self.dilatate()
            # self.show = self.show
        else:
            pass
        self.show = self.map_to_image()
        return self.show

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
            self.saveFile()
        elif self.operation == "Export":
            print('Exporting')
            self.exportFile()
        elif self.operation == "Open":
            print('Opening')
            self.FE.set(self.openFile())
        elif self.operation == "Initialize":
            print("Initializing")
            self.FE.rows = ROWS_VALUE.get()
            self.FE.columns = COLUMNS_VALUE.get()
            self.FE.init()
        elif self.operation == "Inclusions":
            print("Inclusions generation")
            self.FE.is_procedure = 0
            self.FE.inclusions_q = QUANTITY_INCLUSIONS_VALUE.get()
            self.FE.inclusions_r_min = MIN_INCLUSIONS_VALUE.get()
            self.FE.inclusions_r_max = MAX_INCLUSIONS_VALUE.get()
            self.FE.generate_inclusions()
        elif self.operation == "Seed":
            print("Seeding")
            # self.FE.reset()
            # self.FE.rows = ROWS_VALUE.get()
            # self.FE.columns = COLUMNS_VALUE.get()

            # print(self.FE.KERNEL[list(KERNELS.values()).index(KERNEL_CURR_VALUE.get())])
            # self.FE.kernel = self.FE.KERNEL[list(KERNELS.values()).index(KERNEL_CURR_VALUE.get())]
            self.FE.is_procedure = 0
            self.FE.generate_seed(window.GRAIN.get())
        elif self.operation == "Once":
            print("Doing Once")
            self.update_vars()
            self.FE.dilatate()
        elif self.operation == "Start/Pause":
            print("Starting/Pausing the Procedure")
            self.update_vars()
            self.FE.dilatate_is_procedure()
        elif self.operation == "Boundaries":
            print("Boundaries creation")
            # self.FE.reset()
            self.FE.check_boundaries()
        elif self.operation == "Dual-phase":
            self.FE.dual_phase_feature()
        elif self.operation == "Substructs":
            self.FE.substructures_feature()
        else:
            raise NameError

    def update_vars(self):
        self.FE.kernel = self.FE.KERNEL[list(KERNELS.values()).index(KERNEL_CURR_VALUE.get())]
        self.FE.is_random = RANDOM_BOX_VALUE.get()
        self.FE.type = WRAP_VALUE.get()
        self.FE.GBC = GBC_VALUE.get()
        self.FE.GBC_threshold = GBC_THRESHOLD_VALUE.get()

    def saveFile(self):
        self.timeNow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        add_name = []
        data = []
        if MERGED_VALUE.get() == 1:
            add_name.append("merged")
            data.append(self.FE.get())
        if GRAINS_VALUE.get() == 1:
            add_name.append("grains")
            data.append(self.FE.only_grains())
        if INCLUSIONS_VALUE.get() == 1:
            add_name.append("inclusions")
            data.append(self.FE.only_inclusions())
        if FIRSTPHASE_VALUE.get() == 1:
            add_name.append("firstPhase")
            data.append(self.FE.only_first_phase())
        if BOUNDARIES_VALUE.get() == 1:
            add_name.append("boundaries")
            data.append(self.FE.only_boundaries())

        if not data:
            MERGED_VALUE.set(1)
            add_name.append("merged")
            data.append(data)

        for a, d in zip(add_name, data):
            if window.PATH_SAVE.get() == '':
                self.fileName = f'CA_{a}_{self.timeNow}'
            else:
                self.fileName = f'{window.PATH_SAVE.get()}_{a}'
            with open(str(self.currentPath + r'\\Data\\' + str(self.fileName) + '.csv'), 'w', newline='') as file_s:
                np.savetxt(file_s, d, delimiter=',', fmt='%d')

    def exportFile(self):
        f.FE.check_boundaries()
        self.timeNow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        add_name = []
        data = []
        image = []
        phase = []
        boundary = []
        is_merged_mode = []
        if MERGED_VALUE.get() == 1:
            is_merged_mode.append(1)
            add_name.append("merged")
            data.append(self.FE.get())
            image.append(self.FE.map_to_image(self.FE.get(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())
        if GRAINS_VALUE.get() == 1:
            is_merged_mode.append(0)
            add_name.append("grains")
            data.append(self.FE.only_grains())
            image.append(self.FE.map_to_image(self.FE.only_grains(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())
        if INCLUSIONS_VALUE.get() == 1:
            is_merged_mode.append(0)
            add_name.append("inclusions")
            data.append(self.FE.only_inclusions())
            image.append(self.FE.map_to_image(self.FE.only_inclusions(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())
        if FIRSTPHASE_VALUE.get() == 1:
            is_merged_mode.append(0)
            add_name.append("firstPhase")
            data.append(self.FE.only_first_phase())
            image.append(self.FE.map_to_image(self.FE.only_first_phase(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())
        if BOUNDARIES_VALUE.get() == 1:
            is_merged_mode.append(0)
            add_name.append("boundaries")
            data.append(self.FE.only_boundaries())
            image.append(self.FE.map_to_image(self.FE.only_boundaries(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())
        if not data:
            MERGED_VALUE.set(1)
            is_merged_mode.append(1)
            add_name.append("merged")
            data.append(self.FE.get())
            image.append(self.FE.map_to_image(self.FE.get(), change_order=False))
            phase.append(self.FE.get_phase())
            boundary.append(self.FE.get_boundaries())


        for a, d, img, pH, b, ism in zip(add_name, data, image, phase, boundary, is_merged_mode):
            if window.PATH_EXPORT.get() == '':
                self.fileName = f'Export_{a}_{self.timeNow}'
            else:
                self.fileName = f'{window.PATH_EXPORT.get()}_{a}'

            # array = ['Row', 'Column', 'grain_ID', 'Phase', 'is_boundary']
            array = []
            with open(str(self.currentPath + r'/Data/CSVs/' + str(self.fileName) + '.csv'), 'w', newline='') as file_s:
                array.append(f'Size [columns x rows]: [{f.FE.columns} x {f.FE.rows}]')
                array.append(f"Boarders' lengths [grainID -> length]: ")
                for k, v in f.FE.border_length.items():
                    array.append(f'{k} -> {v}')
                array.append(f'Average grain size: {f.FE.avg_grain_size}')


                for r in range(d.shape[0]):
                    for c in range(d.shape[1]):
                        if d[r][c] == 0 or d[r][c] == 2 and ism == 0:
                            pass
                        else:
                            new = [r, c, d[r][c], pH[r][c], b[r][c]]
                            array.append(new)


                print(self.currentPath)
                np.savetxt(file_s, array, delimiter=';', fmt='%s')
            cv2.imwrite(self.currentPath + r'/Data/PNGs/' + str(self.fileName) + '.png', img)

    def openFile(self):
        path = filedialog.askopenfilename(filetypes=(("*.csv", "*.csv"), ("All files", "*.*")))
        self.fileName = os.path.split(path)[-1]
        PATH_OPEN_value.set(self.fileName)
        return np.loadtxt(path, delimiter=',', dtype=np.uint8)


class ButtonCreator(Functionalities):
    def __init__(self, w, name):
        super().__init__()
        self.operation = name
        self.button = Button(w, text=self.operation, command=self.command_line_executioner, height=1, width=8)
        self.button.pack(side=RIGHT)




wrapper0 = Frame(window)
wrapper0.pack(side=LEFT, ipady=5)

wrapper1 = Frame(window)
wrapper1.pack(side=TOP, ipady=30)

# -------------------File Operations-----------------
window.lf0 = LabelFrame(wrapper0, text="File Operations", width=10)
window.lf0.pack(ipady=2, anchor=NW)

window.f00 = Frame(window.lf0)
window.f00.pack(pady=2, fill=X)
window.PATH_SAVE = Entry(window.f00, textvariable=None)
window.PATH_SAVE.pack(side=LEFT)
ButtonCreator(window.f00, "Save")

window.f01 = Frame(window.lf0)
window.f01.pack(pady=2, fill=X)
window.PATH_EXPORT = Entry(window.f01, textvariable=None)
window.PATH_EXPORT.pack(side=LEFT)
ButtonCreator(window.f01, "Export")

window.f02 = Frame(window.lf0)
window.f02.pack(pady=2, fill=X)
ButtonCreator(window.f02, "Open")
PATH_OPEN_value = StringVar()
PATH_OPEN_value.set("New")
window.PATH_OPEN = Label(window.f02, textvariable=PATH_OPEN_value, width=45, anchor=W)
window.PATH_OPEN.pack(side=LEFT)

window.f03 = Frame(window.lf0)
window.f03.pack(pady=2, fill=X)
GRAINS_VALUE = IntVar()
window.GRAINS = Checkbutton(window.f03, text="Grains", variable=GRAINS_VALUE)
window.GRAINS.pack(side=LEFT)

INCLUSIONS_VALUE = IntVar()
window.INCLUSIONS = Checkbutton(window.f03, text="Inclusions", variable=INCLUSIONS_VALUE)
window.INCLUSIONS.pack(side=LEFT)

FIRSTPHASE_VALUE = IntVar()
window.FIRSTPHASE = Checkbutton(window.f03, text="firstPhase", variable=FIRSTPHASE_VALUE)
window.FIRSTPHASE.pack(side=LEFT)

BOUNDARIES_VALUE = IntVar()
window.BOUNDARIES = Checkbutton(window.f03, text="Boundaries", variable=BOUNDARIES_VALUE)
window.BOUNDARIES.pack(side=LEFT)

MERGED_VALUE = IntVar()
window.MERGED = Checkbutton(window.f03, text="Merged", variable=MERGED_VALUE)
window.MERGED.pack(side=LEFT)
# -------------END---File Operations---END-----------

window.EMPTY0 = Label(wrapper0)
window.EMPTY0.pack(pady=21)

# -----------------Data-----------------
window.lf1 = LabelFrame(wrapper0, text="Data")
window.lf1.pack(ipady=5)



window.f10 = Frame(window.lf1)
window.f10.pack(pady=5, fill=X)
window.canvas = Canvas(window.f10, width=500, height=500)
window.canvas.pack(side=LEFT)
# -----------END---Data---END-----------





# -----------------Start-up-----------------
window.lf2 = LabelFrame(wrapper1, text="Start-up", height=50)
window.lf2.pack(ipady=2, expand=True, anchor=NE)

window.f20 = Frame(window.lf2)
window.f20.pack(pady=2, fill=X)
window.ROWS_LABEL = Label(window.f20, text="       Rows:  ")
window.ROWS_LABEL.pack(side=LEFT)
ROWS_VALUE = IntVar()
ROWS_VALUE.set(150)
window.ROWS = Entry(window.f20, textvariable=ROWS_VALUE)
window.ROWS.pack(side=LEFT)

window.f21 = Frame(window.lf2)
window.f21.pack(pady=2, fill=X)
window.COLUMNS_LABEL = Label(window.f21, text="Columns:  ")
window.COLUMNS_LABEL.pack(side=LEFT)
COLUMNS_VALUE = IntVar()
COLUMNS_VALUE.set(150)
window.COLUMNS = Entry(window.f21, textvariable=COLUMNS_VALUE)
window.COLUMNS.pack(side=LEFT)

window.f22 = Frame(window.lf2)
window.f22.pack(pady=2, fill=X)
ButtonCreator(window.f22, "Initialize")

window.f23 = Frame(window.lf2)
window.f23.pack(pady=8, fill=X)
ButtonCreator(window.f23, "Boundaries")
# -----------END---Start-up---END-----------


# ----------------Inclusions-----------------
window.lf3 = LabelFrame(wrapper1, text="Inclusions")
window.lf3.pack(ipady=2, anchor=NE, fill=BOTH)

window.f30 = Frame(window.lf3)
window.f30.pack(pady=2, fill=X)
MIN_INCLUSIONS_LBL = Label(window.f30, text="Minimum radius: ")
MIN_INCLUSIONS_LBL.pack(side=LEFT)
MIN_INCLUSIONS_VALUE = IntVar()
MIN_INCLUSIONS_VALUE.set(4)
window.MIN_INCLUSIONS = Entry(window.f30, textvariable=MIN_INCLUSIONS_VALUE, width=10, justify=RIGHT)
window.MIN_INCLUSIONS.pack(side=RIGHT)

window.f31 = Frame(window.lf3)
window.f31.pack(pady=2, fill=X)
MAX_INCLUSIONS_LBL = Label(window.f31, text="Maximum radius: ")
MAX_INCLUSIONS_LBL.pack(side=LEFT)
MAX_INCLUSIONS_VALUE = IntVar()
MAX_INCLUSIONS_VALUE.set(9)
window.MAX_INCLUSIONS = Entry(window.f31, textvariable=MAX_INCLUSIONS_VALUE, width=10, justify=RIGHT)
window.MAX_INCLUSIONS.pack(side=RIGHT)

window.f32 = Frame(window.lf3)
window.f32.pack(pady=2, fill=X)
QUANTITY_INCLUSIONS_LBL = Label(window.f32, text="Quantity:  ")
QUANTITY_INCLUSIONS_LBL.pack(side=LEFT)
QUANTITY_INCLUSIONS_VALUE = IntVar()
QUANTITY_INCLUSIONS_VALUE.set(4)
window.QUANTITY_INCLUSIONS = Entry(window.f32, textvariable=QUANTITY_INCLUSIONS_VALUE, width=10, justify=RIGHT)
window.QUANTITY_INCLUSIONS.pack(side=RIGHT)

window.f33 = Frame(window.lf3)
window.f33.pack(pady=2, fill=X)
ButtonCreator(window.f33, "Inclusions")
# -----------END---Inclusions---END-----------


# -----------------Seeding-----------------
window.lf4 = LabelFrame(wrapper1, text="Seeding")
window.lf4.pack(ipady=2, anchor=E, fill=BOTH)

window.f40 = Frame(window.lf4)
window.f40.pack(pady=2, fill=X)
GRAIN_VALUE = IntVar()
GRAIN_VALUE.set(50)
window.GRAIN = Entry(window.f40, textvariable=GRAIN_VALUE, width=10)
window.GRAIN.pack(side=LEFT)
ButtonCreator(window.f40, "Seed")
# -----------END---Seeding---END-----------


# -----------------Generation-----------------
window.lf5 = LabelFrame(wrapper1, text="Generation")
window.lf5.pack(ipady=2, anchor=E, fill=BOTH)

window.f50 = Frame(window.lf5)
window.f50.pack(pady=2, fill=X)
KERNEL_CURR_VALUE = StringVar()
KERNEL_CURR_VALUE.set(KERNELS[1])
window.KERNEL_CURR = Label(window.f50, textvariable=KERNEL_CURR_VALUE)
window.KERNEL_CURR.pack(side=LEFT)

ButtonCreator(window.f50, "Once")

window.f51 = Frame(window.lf5)
window.f51.pack(pady=2, fill=X)

ButtonCreator(window.f51, "Start/Pause")

# EMPTY33
window.f52 = Frame(window.lf5)
window.f52.pack(pady=2, fill=X)
window.EMPTY53 = Label(window.f52)
window.EMPTY53.pack(side=LEFT)

window.f53 = Frame(window.lf5)
window.f53.pack(pady=2, fill=X)
GBC_VALUE = IntVar()
window.GBC = Checkbutton(window.f53, text="GBC", variable=GBC_VALUE)
window.GBC.pack(side=LEFT)

GBC_THRESHOLD_VALUE = IntVar()
GBC_THRESHOLD_VALUE.set(50)
window.GBC_THRESHOLD = Entry(window.f53, textvariable=GBC_THRESHOLD_VALUE, width=3, justify=RIGHT)
window.GBC_THRESHOLD.pack(side=RIGHT, padx=2)

window.GBC_THRESHOLD_LBL = Label(window.f53, text="|   Probability of change [%]:")
window.GBC_THRESHOLD_LBL.pack(side=RIGHT)


window.f54 = Frame(window.lf5)
window.f54.pack(pady=2, fill=X)
WRAP_VALUE = IntVar()
window.WRAP = Checkbutton(window.f54, text="Wrap?", variable=WRAP_VALUE)
window.WRAP.pack(side=LEFT)

window.f55 = Frame(window.lf5)
window.f55.pack(pady=2, fill=X)
RANDOM_BOX_VALUE = IntVar()
window.RANDOM_BOX = Checkbutton(window.f55, text="Random", variable=RANDOM_BOX_VALUE)
window.RANDOM_BOX.pack(side=LEFT)

window.f56 = Frame(window.lf5)
window.f56.pack(pady=2, fill=X)
window.LIST = Listbox(window.f56, height=6, bd=1)
for k, v in KERNELS.items():
    window.LIST.insert(k, v)
window.LIST.select_set(0)
window.LIST.pack(side=LEFT)
# -----------END---Generation---END--------------

# -----------------Second Phase--------------------
window.lf6 = LabelFrame(wrapper1, text="Second Phase")
window.lf6.pack(ipady=2, anchor=E, fill=BOTH)

window.f60 = Frame(window.lf6)
window.f60.pack(pady=2, fill=X)
DELETE_BY_CLICK_VALUE = IntVar()
window.DELETE_BY_CLICK = Checkbutton(window.f60, text="Delete?", variable=DELETE_BY_CLICK_VALUE)
window.DELETE_BY_CLICK.pack(side=LEFT)


ButtonCreator(window.f60, "Dual-phase")
ButtonCreator(window.f60, "Substructs")

# -----------END---Second Phase---END--------------




f = Functionalities()
merged_old = 0
MERGED_VALUE.set(1)

window.canvas.bind("<Button-1>", f.FE.callback)
if sys.version_info >= (3, 0):
    _thread_target_key = '_target'
    _thread_args_key = '_args'
    _thread_kwargs_key = '_kwargs'
else:
    _thread_target_key = '_Thread__target'
    _thread_args_key = '_Thread__args'
    _thread_kwargs_key = '_Thread__kwargs'
class ThreadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        target = getattr(self, _thread_target_key)
        if not target is None:
            self._return = target(
                *getattr(self, _thread_args_key),
                **getattr(self, _thread_kwargs_key)
            )

    def ret(self, *args, **kwargs):
        return self._return

th1 = ThreadWithReturn(target=f.FE.refresh)
th1.start()
img = f.FE.map_to_image()

while 1:
    try:
        if th1.is_alive():
            pass
        else:
            img = img if th1.ret() is None else th1.ret()
            th1 = ThreadWithReturn(target=f.FE.refresh)
            th1.start()

            i = ImageTk.PhotoImage(Image.fromarray(img), master=window)
            window.canvas.create_image(0, 0, anchor=NW, image=i)

        try:
            KERNEL_CURR_VALUE.set(KERNELS[window.LIST.curselection()[0]])
        except:
            pass

        if f.FE.is_procedure == 1:
            window.GBC.config(state='disabled')
            window.RANDOM_BOX.config(state='disabled')
            window.WRAP.config(state='disabled')
            window.LIST.config(state='disabled')
        else:
            window.GBC.config(state='normal')
            if GBC_VALUE.get() == 1:
                window.LIST.select_clear(first=0, last=6)
                KERNEL_CURR_VALUE.set(KERNELS[0])
                window.GBC_THRESHOLD.config(state='normal')
                window.RANDOM_BOX.config(state='disabled')
                window.WRAP.config(state='disabled')
                window.LIST.config(state='disabled')
            else:
                window.GBC_THRESHOLD.config(state='disabled')
                window.RANDOM_BOX.config(state='normal')
                window.WRAP.config(state='normal')
                window.LIST.config(state='normal')

        if MERGED_VALUE.get() == 0 and merged_old == 1:
            GRAINS_VALUE.set(0)
            INCLUSIONS_VALUE.set(0)
            FIRSTPHASE_VALUE.set(0)
            BOUNDARIES_VALUE.set(0)
            merged_old = 0
        elif MERGED_VALUE.get() == 1 and merged_old == 0:
            GRAINS_VALUE.set(1)
            INCLUSIONS_VALUE.set(1)
            FIRSTPHASE_VALUE.set(1)
            BOUNDARIES_VALUE.set(1)
            merged_old = 1
        else:
            if GRAINS_VALUE.get() == 1 and INCLUSIONS_VALUE.get() == 1 and FIRSTPHASE_VALUE.get() == 1 and BOUNDARIES_VALUE.get():
                MERGED_VALUE.set(1)
                merged_old = 1
            else:
                MERGED_VALUE.set(0)
                merged_old = 0
        # print(list(KERNELS.values()).index(KERNEL_CURR_VALUE.get()))

    except:
        pass

    try:
        window.update_idletasks()
        window.update()
    except:
        break





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

