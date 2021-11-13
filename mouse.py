import numpy as np


class Mouse:
    def __init__(self, affine_transform, img, action, type) -> None:
        self.isClick = False
        self.isLastClick = False
        self.start = np.array([0, 0])
        self.end = np.array([0, 0])
        self.pos = np.array([0, 0])
        self.angle = 0
        self.defaultAngle = 0
        self.affine_transform = affine_transform
        self.image = img
        self.action = action
        self.canvasCenter = np.array([900, 500])
        self.type = type
        self.scale = [1, 1]
        self.afterSize = np.array(self.image.originalImg.shape[:2])
        self.lastSize = np.flip(np.array(self.image.originalImg.shape[:2]))

    def onClick(self, e):
        self.start = np.array([e.x, e.y])
        diff = self.start - self.canvasCenter
        if self.action.get():
            self.defaultAngle = np.arctan2(diff[0], diff[1]) - np.pi / 2 - self.angle
        self.isClick = True

    def outClick(self, e):
        self.end = np.array([e.x, e.y])
        diff = self.end - self.canvasCenter
        if self.action.get():
            self.angle = np.arctan2(diff[0], diff[1]) - np.pi / 2 - self.defaultAngle
            self.image.npimg = self.affine_transform(
                self.image.originalImg,
                self.scale[0],
                self.scale[1],
                -self.angle,
                type=self.type.get(),
            )
            self.image.originalImg = self.image.npimg
            self.scale = [1, 1]
            self.angle = 0
        else:
            self.lastSize = self.afterSize
        self.isClick = False

    def mouse(self, e):
        if self.isClick:
            self.pos = np.array([e.x, e.y])
            if self.action.get():
                diff = self.pos - self.canvasCenter
                self.angle = (
                    np.arctan2(diff[0], diff[1]) - np.pi / 2 - self.defaultAngle
                )
            else:
                diff = self.pos - self.start
                diff[1] = 0
                self.afterSize = self.lastSize + diff
                self.scale = self.afterSize / np.flip(self.image.originalImg.shape[:2])
