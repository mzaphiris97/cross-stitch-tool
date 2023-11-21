import cv2
import numpy as np

from AbstractLineDetector import AbstractLineDetector


class VerticalLineDetector(AbstractLineDetector):

    def __init__(self, img):
        super().__init__(img)

    def sobel_transform(self):
        sobel = cv2.Sobel(self.img, 0, 1, 0, 1, 1, 1, cv2.BORDER_DEFAULT)
        return cv2.convertScaleAbs(sobel)

    def line_angle_in_range(self, theta):
        if (theta >= 0.0) & (theta < np.pi / 170):
            return True
        else:
            return False

    def get_threshold(self):
        return self.height / 1.5

    def get_coordinate(self, r_theta):
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.cos(theta)
        x = a * r
        return x

    def compare(self, x0, x1):
        if (x1 - x0) > 1:
            return -1
        else:
            return 1

    def get_color_avg(self, x):
        color_sum = 0
        for y in range(self.height):
            color = self.img[int(y), int(x)]
            color_sum = color_sum + color
        return color_sum / self.height

    def get_max(self):
        return self.width
