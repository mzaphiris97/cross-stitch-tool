import functools
from abc import (
    ABC,
    abstractmethod,
)

import cv2
import numpy as np


class AbstractLineDetector(ABC):
    img = [[]]
    height = 0
    width = 0

    @abstractmethod
    def sobel_transform(self):
        ...

    @abstractmethod
    def line_angle_in_range(self, r_theta):
        ...

    @abstractmethod
    def get_coordinate(self, r_theta):
        ...

    @abstractmethod
    def compare(self, cord1, cord2):
        ...

    @abstractmethod
    def get_color_avg(self, cord):
        ...

    @abstractmethod
    def get_max(self):
        ...

    @abstractmethod
    def get_threshold(self):
        ...

    def __init__(self, img):
        self.img = img
        self.height, self.width = img.shape

    def get_lines(self):
        gradient = self.sobel_transform()
        edges = cv2.Canny(gradient, 50, 150, apertureSize=3)

        variance = np.round(self.height / 250)

        initial_lines = cv2.HoughLines(edges, variance, np.pi / 2, int(self.get_threshold()))

        final_lines = []

        for line in initial_lines:
            arr = np.array(line[0], dtype=np.float64)
            r, theta = arr

            if self.line_angle_in_range(theta):
                final_lines.append(self.get_coordinate(line))

        final_lines = sorted(final_lines, key=functools.cmp_to_key(self.compare))

        diffs = []

        for i in range(len(final_lines)):
            if i == 0:
                continue
            cord1 = final_lines[i]
            cord0 = final_lines[i - 1]
            diff = abs(cord1 - cord0)
            diffs.append(diff)

        std_dev = np.std(diffs)
        avg = np.average(diffs)

        output = []

        if len(final_lines) == 0:
            exit()

        cur_cord = self.find_most_likely_line(final_lines[0], int(std_dev+2))

        idx = 1
        while (cur_cord < final_lines[len(final_lines) - 1]) & (idx < len(final_lines)):
            output.append(cur_cord)
            pot_cord = []
            new_idx = []
            idx_new = idx + 1
            while idx_new < len(final_lines):
                if final_lines[idx_new] > (cur_cord + avg * 1.25):
                    break
                diff = final_lines[idx_new] - cur_cord
                if (diff < (avg + std_dev)) & (diff >= (avg - std_dev)):
                    pot_cord.append(final_lines[idx_new])
                    new_idx.append(idx_new)
                idx_new = idx_new + 1
            if len(pot_cord) == 0:
                if cur_cord + avg >= self.get_max():
                    cur_cord = cur_cord + avg
                    continue
                cur_cord = self.find_most_likely_line(cur_cord + avg, int(std_dev+2))
                if final_lines[idx] >= cur_cord:
                    idx = idx
                else:
                    idx = idx + 1
                continue
            else:
                min_color_avg = 1000
                pot_idx = 0
                new_cord = cur_cord
                for next_cord in pot_cord:
                    color_avg = self.get_color_avg(next_cord)
                    if color_avg < min_color_avg:
                        min_color_avg = color_avg
                        pot_idx = new_idx[pot_cord.index(next_cord)]
                        new_cord = next_cord
                idx = pot_idx
                cur_cord = self.find_most_likely_line(new_cord, int(std_dev+2))

        output.append(cur_cord)
        return output

    def find_most_likely_line(self, cord, padding):
        lowest_color_avg = 1000
        likely_cord = cord
        start_cord = cord - padding

        while (start_cord <= cord + padding) & (start_cord < self.get_max()):
            color_avg = self.get_color_avg(start_cord)
            if color_avg < lowest_color_avg:
                likely_cord = start_cord
                lowest_color_avg = color_avg
            start_cord = start_cord + 1

        return likely_cord

