#!/usr/bin/python3

from PIL import Image
from numpy import *
import numpy as np
import sys
import os

Pattern = {
    1: [[1]],
    2: [[0, 2], [3, 1]],
    3: [[0, 7, 2], [8, 4, 5], [3, 6, 1]],
    4: [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
}


def getfilelist(path, type):
    file = ""
    filelist = [file for file in os.listdir(path)
                if os.path.splitext(file)[1] == type]
    return filelist


def render(path, name, dim):
    paint = Pattern[dim]
    if paint == None:
        return

    filename = os.path.join(path, name)
    if os.path.exists(os.path.join(path, 'after/')) == False:
        os.mkdir(os.path.join(path, 'after/'))
    savefilename = os.path.join(path, 'after', '%d%s' % (dim, name))
    start_color = (0, 0, 0, 0)  # white
    new_color = (255, 255, 255, 255)  # black

    im = Image.open(filename).convert("RGBA")  # .convert("L")
    data = array(im)
    data[(data == start_color).all(axis=-1)] = new_color
    im = Image.fromarray(data, mode='RGBA').convert("L")
    data = array(im)
    width, height = im.size
    data.reshape(height, width)

    n = dim * height
    m = dim * width

    top_color = 255
    arr = [None] * n

    for i in range(len(arr)):
        arr[i] = [0] * m

    if dim == 1:
        div = top_color / 2
    else:
        div = top_color / dim / dim

    for i in range(0, height):
        for j in range(0, width):
            tmp = int(data[i][j] / div)
            for ii in range(0, dim):
                for jj in range(0, dim):
                    if paint[ii][jj] < tmp:
                        arr[dim * i + ii][dim * j + jj] = top_color
                    else:
                        arr[dim * i + ii][dim * j + jj] = 0

    new_matrix = mat(arr)
    new_im = Image.fromarray(new_matrix.astype(np.ubyte))
    new_im = new_im.convert("RGBA")
    new_im.save(savefilename)


if __name__ == '__main__':
    length = len(sys.argv)
    path = os.path.join('./')
    dim = 2
    if length == 2:
        path = sys.argv[1]
    elif length >= 3:
        path = sys.argv[1]
        dim = int(sys.argv[2])
    filelist = getfilelist(path, '.png')
    for name in filelist:
        render(path, name, dim)
