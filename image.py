from PIL import Image
import numpy as np

from aabb import AABB


def clip_xy(ref_xy, img_shape):
    ref_x = np.where(
        (0 <= ref_xy[..., 0]) & (ref_xy[..., 0] < img_shape[0]), ref_xy[..., 0], -1
    )
    ref_y = np.where(
        (0 <= ref_xy[..., 1]) & (ref_xy[..., 1] < img_shape[1]), ref_xy[..., 1], -1
    )

    return np.dstack([ref_x, ref_y])


def getAffineMatrix(scaleX, scaleY, stride, angle):
    return np.matrix(
        "{},{},{};{},{},{};0,0,1".format(
            scaleY * np.cos(angle),
            np.sin(angle),
            -stride[0] * np.cos(angle) - stride[1] * np.sin(angle),
            -np.sin(angle),
            scaleX * np.cos(angle),
            stride[0] * np.sin(angle) - stride[1] * np.cos(angle),
        )
    )


class ImageWrapper:
    def __init__(self, imagePass) -> None:
        self.originalImg = np.array(Image.open(imagePass))
        self.npimg = self.originalImg
        self.back = np.zeros((1800, 1000))

    def save(self, filePass):
        if len(filePass):
            Image.fromarray(self.originalImg).save(filePass)

    def affine_transform(
        self, img, scaleX=1, scaleY=1, angle=0, type=0, updateOriginal=False
    ):
        img = np.pad(img, [(1, 1), (1, 1), (0, 0)], "constant")
        stride = np.array([scaleY * img.shape[0] / 2, scaleX * img.shape[1] / 2])
        affin = getAffineMatrix(scaleX, scaleY, stride, angle)

        aa = AABB(getAffineMatrix(scaleX, scaleY, stride, np.pi / 4), img)
        maxLength = int(
            max(scaleX, scaleY) * np.sqrt(img.shape[0] ** 2 + img.shape[1] ** 2)
        )
        maxLength = np.array([maxLength, maxLength], np.uint32)
        # maxLength = np.array([scaleY * img.shape[0], scaleX * img.shape[1]], np.uint32)
        affin[0, 2] += maxLength[0] / 2
        affin[1, 2] += maxLength[1] / 2

        resizedSize = maxLength
        inv_affin = np.linalg.inv(affin)
        x, y = np.mgrid[: resizedSize[0], : resizedSize[1]]
        resize = np.dstack((x, y, np.ones((resizedSize[0], resizedSize[1]))))
        ref_xy = np.einsum("ijk,lk->ijl", resize, inv_affin)[..., :2]

        if type == 0:
            ref_nearmost_xy = clip_xy(ref_xy.astype(np.uint32), img.shape)
            img_nearmost = img[ref_nearmost_xy[..., 0], ref_nearmost_xy[..., 1]]
            img = img_nearmost
        elif type == 1:
            diff = ref_xy - np.floor(ref_xy)
            xy = [clip_xy(ref_xy.astype(np.uint32), img.shape)]
            xy.append(clip_xy(xy[0] + [1, 0], img.shape))
            xy.append(clip_xy(xy[0] + [0, 1], img.shape))
            xy.append(clip_xy(xy[0] + [1, 1], img.shape))
            dx = diff[..., 0][:, :, np.newaxis]
            dy = diff[..., 1][:, :, np.newaxis]
            img = (
                np.multiply((1 - dx) * (1 - dy), img[xy[0][..., 0], xy[0][..., 1]])
                + np.multiply(dx * (1 - dy), img[xy[1][..., 0], xy[1][..., 1]])
                + np.multiply((1 - dx) * dy, img[xy[2][..., 0], xy[2][..., 1]])
                + np.multiply(dx * dy, img[xy[3][..., 0], xy[3][..., 1]])
            ).astype(np.uint8)
        self.npimg = img
        if updateOriginal:
            self.originalImg = img
        return img
