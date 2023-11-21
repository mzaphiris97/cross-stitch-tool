import cv2
import os

import numpy as np

from HorizontalLineDetector import HorizontalLineDetector
from LineMappingTwo import LineMappingTwo
from VerticalLineDetector import VerticalLineDetector

global line_mapping
global img
global output_path
global rect_img
global progress


def draw_vertical(x, img, g):
    cv2.line(img, (int(x), 0), (int(x), img.shape.height), (255, int(g), 255), 2)


def draw_horizontal(y, img, g):
    cv2.line(img, (0, int(y)), (img.shape.width, int(y)), (255, int(g), 255), 2)


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        toggled = line_mapping.toggle(x, y)
        draw_mapping_img(toggled)

        final_image = cv2.addWeighted(img, 1, rect_img, 0.75, 0)

        cv2.imshow('image', final_image)
        print("END CLICK")


def draw_mapping_img(toggled):
    if toggled[4]:
        new_img = cv2.rectangle(rect_img, (int(toggled[0]), int(toggled[2])), (int(toggled[1]), int(toggled[3])),
                                (193, 183, 44, 1), -1)
    else:
        new_img = cv2.rectangle(rect_img, (int(toggled[0]), int(toggled[2])), (int(toggled[1]), int(toggled[3])),
                                (0, 0, 0, 0), -1)

    cv2.imwrite(output_path, new_img)


if __name__ == '__main__':
    img_path = "venv/samples/0009.jpg"
    output_path = img_path.split('.')[0] + "-rect.png"

    init = cv2.imread(img_path)
    height, width, channels = init.shape

    img = cv2.cvtColor(init, cv2.COLOR_BGR2BGRA)

    if os.path.isfile(output_path):
        rect_img = cv2.imread(output_path, cv2.IMREAD_UNCHANGED)
    else:
        rect_img = np.zeros((height, width, 4), dtype=np.uint8)
        cv2.imwrite(output_path, rect_img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    vertical_line_detector = VerticalLineDetector(gray)
    vertical_lines = vertical_line_detector.get_lines()

    horizontal_line_detector = HorizontalLineDetector(gray)
    horizontal_lines = horizontal_line_detector.get_lines()

    line_mapping = LineMappingTwo(vertical_lines, horizontal_lines)

    cv2.namedWindow('image', cv2.WINDOW_GUI_EXPANDED)

    final_img = cv2.addWeighted(img, 1, rect_img, 0.75, 0)
    cv2.imshow('image', final_img)
    cv2.setMouseCallback('image', click_event)

    cv2.waitKey(0)
