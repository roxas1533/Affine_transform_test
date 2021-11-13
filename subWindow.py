import tkinter as tk

import numpy as np
from numpy.lib.function_base import angle


class ScaleWindow(tk.Frame):
    def __init__(self, master, img):
        super().__init__(master)
        self.pack()
        self.img = img
        master.grab_set()
        master.resizable(width=False, height=False)
        master.title("拡大縮小")
        self.isParcent = tk.BooleanVar()
        self.pxparcent = tk.StringVar()
        self.textX = tk.IntVar()
        self.textY = tk.IntVar()
        self.pxInputX = None
        self.pxInputY = None
        self.changedSize = np.array([1, 1])
        self.originalShape = np.flip(np.array(self.img.originalImg.shape[:2]))
        self.setGUI(master)
        self.setDefault()
        master.geometry("200x150")

        self.setParcent()

    def setDefault(self):
        self.textX.set(self.img.originalImg.shape[1])
        self.textY.set(self.img.originalImg.shape[0])

    def valueCheck(self, str):
        try:
            int(str)
        except:
            return False
        return True

    def change(self, *args):
        try:
            self.textX.get()
        except:
            self.textX.set(self.pxInputX.get()[:-1])
        try:
            self.textY.get()
        except:
            self.textY.set(self.pxInputY.get()[:-1])
        if len(self.pxInputY.get()) and len(self.pxInputX.get()):
            if self.isParcent.get():
                self.changedSize = [
                    int(self.pxInputX.get()) / 100,
                    int(self.pxInputY.get()) / 100,
                ]
            else:
                self.changedSize = [
                    int(self.pxInputX.get()),
                    int(self.pxInputY.get()),
                ] / self.originalShape

    def setParcent(self):
        self.pxInputX.delete(0, tk.END)
        self.pxInputY.delete(0, tk.END)
        if self.isParcent.get():
            self.textX.set(int(self.changedSize[0] * 100))
            self.textY.set(int(self.changedSize[1] * 100))
            self.pxparcent.set("%")
        else:

            temp = np.ceil(np.array(self.changedSize) * self.originalShape)
            self.textX.set(int(temp[0]))
            self.textY.set(int(temp[1]))
            self.pxparcent.set("px")

    def setGUI(self, master):
        vc = master.register(self.valueCheck)
        self.textX.trace("w", self.change)
        self.textY.trace("w", self.change)
        lbl = tk.Label(master, text="X:")
        lbl.place(x=30, y=10)
        lbl = tk.Label(master, text="Y:")
        lbl.place(x=30, y=35)

        lbl = tk.Label(master, textvariable=self.pxparcent)
        lbl.place(x=120, y=10)
        self.pxInputX = tk.Entry(
            master, width=10, textvariable=self.textX, validate="key", vcmd=(vc, "%S")
        )
        self.pxInputX.place(x=50, y=10)

        lbl = tk.Label(master, textvariable=self.pxparcent)
        lbl.place(x=120, y=35)
        self.pxInputY = tk.Entry(
            master, width=10, textvariable=self.textY, validate="key", vcmd=(vc, "%S")
        )
        self.pxInputY.place(x=50, y=35)

        maintenance = tk.Checkbutton(master, text="横縦比を維持する(未実装)")
        maintenance.place(x=50, y=55)
        parcentButton = tk.Checkbutton(
            master, text="パーセントで指定する", command=self.setParcent, variable=self.isParcent
        )
        parcentButton.place(x=50, y=75)
        okbutton = tk.Button(
            master,
            text="OK",
            command=lambda: master.destroy()
            or self.img.affine_transform(
                self.img.originalImg,
                self.changedSize[0],
                self.changedSize[1],
                type=1,
                updateOriginal=True,
            ),
        )
        okbutton.place(relx=0.15, rely=0.80, relwidth=0.3)
        cancelButton = tk.Button(master, text="キャンセル", command=lambda: master.destroy())
        cancelButton.place(relx=0.5, rely=0.80)


class rotateWindow(tk.Frame):
    def __init__(self, master, img):
        super().__init__(master)
        self.pack()
        self.img = img
        master.grab_set()
        master.resizable(width=False, height=False)
        master.title("回転")
        self.textX = tk.IntVar()
        self.pxInput = None
        self.changedSize = np.array([1, 1])
        self.originalShape = np.flip(np.array(self.img.originalImg.shape[:2]))
        self.setGUI(master)
        self.setDefault()
        master.geometry("200x120")

    def setDefault(self):
        self.textX.set(0)

    def valueCheck(self, str):
        try:
            int(str)
        except:
            return False
        return True

    def change(self, *args):
        try:
            self.textX.get()
        except:
            self.textX.set(self.pxInput.get()[:-1])

    def setGUI(self, master):
        vc = master.register(self.valueCheck)
        self.textX.trace("w", self.change)
        lbl = tk.Label(master, text="度")
        lbl.place(x=120, y=40)
        self.pxInput = tk.Entry(
            master, width=10, textvariable=self.textX, validate="key", vcmd=(vc, "%S")
        )
        self.pxInput.place(x=50, y=40)

        okbutton = tk.Button(
            master,
            text="OK",
            command=lambda: master.destroy()
            or self.img.affine_transform(
                self.img.originalImg,
                angle=np.deg2rad(int(self.textX.get())),
                type=1,
                updateOriginal=True,
            ),
        )
        okbutton.place(relx=0.15, rely=0.70, relwidth=0.3)
        cancelButton = tk.Button(master, text="キャンセル", command=lambda: master.destroy())
        cancelButton.place(relx=0.5, rely=0.70)
