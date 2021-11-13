from os import times
import os
import time
from tkinter.constants import N, NO
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import StringVar, filedialog

from numpy.core.fromnumeric import resize, var
from numpy.lib.function_base import angle

from aabb import AABB
from image import ImageWrapper
from mouse import Mouse
from subWindow import ScaleWindow, rotateWindow


WIDTH = 0
HEIGHT = 0
# img = np.array(
#     [
#         [[0, 0, 0], [0, 0, 0], [255, 0, 0], [255, 0, 255]],
#         [[0, 0, 0], [0, 0, 0], [0, 255, 255], [0, 0, 255]],
#         [[255, 0, 0], [255, 0, 255], [0, 0, 0], [0, 0, 0]],
#         [[0, 255, 255], [0, 0, 255], [0, 0, 0], [0, 0, 0]],
#     ],
#     np.uint8,
# )
# def rotate(img, angle, type=0):
#     return affine_transform(img, angle=angle, type=type)


# def scale(img, scale, type=0):
#     return affine_transform(img, scaleX=scale[0], scaleY=scale[1], type=type)


image = None
canvas = None
mouse = None
tkimg = None
filetypes = [("画像", "*.jpg;*.png")]


def openFile():
    global image, canvas, imgarea, mouse, tkimg
    file = filedialog.askopenfilename(
        filetypes=filetypes,
        initialdir=os.path.abspath(os.path.dirname(__file__)),
    )
    if len(file):
        image = ImageWrapper(file)
        image.affine_transform(image.originalImg, 1, 1, 0, 1)

        mouse = Mouse(image.affine_transform, image, action, type)

        img = Image.fromarray(image.npimg)
        tkimg = ImageTk.PhotoImage(image=img)
        imgarea = canvas.create_image(
            int(WIDTH / 2) - image.npimg.shape[1] / 2,
            int(HEIGHT / 2) - image.npimg.shape[0] / 2,
            anchor="nw",
            image=tkimg,
        )
        canvas.bind("<1>", mouse.onClick, action.get())
        canvas.bind("<ButtonRelease>", mouse.outClick)
        canvas.bind("<Motion>", mouse.mouse)
        canvas.pack()
        if image:
            men.entryconfigure("編集モード", state="active")
            men.entryconfigure("編集", state="active")
            men.entryconfigure("補間法", state="active")
            menu_file.entryconfigure("保存", state="active")


root = tk.Tk()
root.geometry("300x100+0+0")
men = tk.Menu(root, tearoff=0)
root.config(menu=men)

menu_file = tk.Menu(men, tearoff=0)
men.add_cascade(label="ファイル", menu=menu_file)


menu_file.add_command(label="開く", command=openFile)
menu_file.add_cascade(
    label="保存",
    command=lambda: image.save(
        filedialog.asksaveasfilename(filetypes=filetypes, defaultextension="png")
    ),
    state="disable",
)
menu_mode = tk.Menu(men, tearoff=0)
men.add_cascade(label="編集モード", menu=menu_mode, state="disable")
action = tk.IntVar()
action.set(0)
menu_mode.add_radiobutton(label="拡大縮小", value=0, variable=action)
menu_mode.add_radiobutton(label="回転", value=1, variable=action)

menu_edit = tk.Menu(men, tearoff=0)
men.add_cascade(label="編集", menu=menu_edit, state="disable")
menu_edit.add_command(
    label="拡大縮小", command=lambda: ScaleWindow(master=tk.Toplevel(), img=image)
)
menu_edit.add_command(
    label="回転", command=lambda: rotateWindow(master=tk.Toplevel(), img=image)
)
menu_edit.add_command(label="アフィン行列指定")


menu_interpolation = tk.Menu(men, tearoff=0)
men.add_cascade(label="補間法", menu=menu_interpolation, state="disable")
type = tk.IntVar()
type.set(1)
menu_interpolation.add_radiobutton(label="ニアレストネイバー", value=0, variable=type)
menu_interpolation.add_radiobutton(label="バイリニア", value=1, variable=type)


def resize(e):
    global imgarea, HEIGHT, WIDTH
    WIDTH = e.width
    HEIGHT = e.height
    if image:
        imgarea = canvas.create_image(
            e.width / 2 - image.npimg.shape[1] / 2,
            e.height / 2 - image.npimg.shape[0] / 2,
            anchor="nw",
            image=tkimg,
        )
        mouse.canvasCenter[0] = e.width / 2
        mouse.canvasCenter[1] = e.height / 2


canvas = tk.Canvas(root, width=1800, height=1000, bg="white")
root.bind("<Configure>", resize)


def animation():
    global tkimg, imgarea
    if image:
        if mouse.isClick:
            image.affine_transform(
                image.originalImg, mouse.scale[0], mouse.scale[1], -mouse.angle
            )
            imgarea = canvas.create_image(
                WIDTH / 2 - image.npimg.shape[1] / 2,
                HEIGHT / 2 - image.npimg.shape[0] / 2,
                anchor="nw",
                image=tkimg,
            )

        img = Image.fromarray(image.npimg)
        tkimg = ImageTk.PhotoImage(image=img)
        canvas.itemconfig(imgarea, image=tkimg)
        mouse.isLastClick = mouse.isClick
    # print(app)
    root.after(16, animation)


root.after(0, animation)

root.mainloop()
