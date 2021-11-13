import numpy as np


class AABB:
    def __init__(self, affine, img) -> None:
        edge = np.array(
            [
                [0, 0],
                [img.shape[0], 0],
                [0, img.shape[1]],
                [img.shape[0], img.shape[1]],
            ]
        )
        afterEdge = np.array([])
        for e in edge:
            t = np.append(e, 1).reshape(-1, 1)
            afterEdge = np.append(afterEdge, np.array(affine.dot(t)).flatten())
        afterEdge = afterEdge.reshape(4, 3)
        EdgeX = afterEdge[..., 0]
        EdgeY = afterEdge[..., 1]

        self.max = [np.max(EdgeX), np.max(EdgeY)]
        self.min = [np.min(EdgeX), np.min(EdgeY)]
        self.size = np.abs(
            np.array([self.max[0] - self.min[0], self.max[1] - self.min[1]], np.uint32)
        )
