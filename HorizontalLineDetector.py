import cv2
import numpy as np

from AbstractLineDetector import AbstractLineDetector

class HorizontalLineDetector(AbstractLineDetector):
    def __init__(self, img):
        super().__init__(img)

    def get_threshold(self):
        return self.width / 1.5

    def sobel_transform(self):
        sobel = cv2.Sobel(self.img, 0, 0, 2, 1, 1, 1, cv2.BORDER_DEFAULT)
        return cv2.convertScaleAbs(sobel)

    def line_angle_in_range(self, theta):
        if (theta > np.pi/2.05) & (theta < np.pi/1.95):
            return True
        else:
            return False

    def get_coordinate(self, r_theta):
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.sin(theta)
        y = a * r
        return y

    def compare(self, y0, y1):
        if (y1 - y0) > 1:
            return -1
        else:
            return 1

    def get_color_avg(self, y):
        color_sum = 0
        for x in range(self.width):
            color = self.img[int(y), int(x)]
            color_sum = color_sum + color
        return color_sum / self.width

    def get_max(self):
        return self.height