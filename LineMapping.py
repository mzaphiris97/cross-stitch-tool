import numpy as np


class LineMapping:
    start_x = 0
    start_y = 0
    sections = []
    cord_to_section = []

    def __init__(self, vertical_lines, horizontal_lines):
        total_x = int(vertical_lines[len(vertical_lines) - 1] - vertical_lines[0])
        total_y = int(horizontal_lines[len(horizontal_lines) - 1] - horizontal_lines[0])

        self.cord_to_section = [[0 for x in range(total_x)] for y in range(total_y)]

        total_sections = (len(vertical_lines) - 1) * (len(horizontal_lines) - 1)
        self.sections = [0 for x in range(total_sections)]
        self.start_x = vertical_lines[0]
        self.start_y = horizontal_lines[0]
        base_row = self.build_initial_x(vertical_lines)
        self.add_horizontals(horizontal_lines, base_row)

    def build_initial_x(self, vertical_lines):
        i = 1
        x_section = []
        while i < len(vertical_lines):
            start = np.floor(vertical_lines[i - 1])
            end = np.floor(vertical_lines[i])
            x = start
            while x < end:
                x_section.append(i - 1)
                x = x + 1
            i = i + 1
        return x_section

    def add_horizontals(self, horizontal_lines, first_x_row):
        num_x = first_x_row[len(first_x_row) - 1] + 1
        i = 1
        while i < len(horizontal_lines):
            start = np.floor(horizontal_lines[i - 1])
            end = np.floor(horizontal_lines[i])
            y = start
            while y < end:
                x = 0
                for vertical_id in first_x_row:
                    pix_y = int(y - self.start_y)
                    self.cord_to_section[pix_y][int(np.floor(x))] = (int(i - 1) * num_x) + int(np.floor(vertical_id))
                    x = x + 1
                y = y + 1
            i = i + 1

    def toggle(self, x, y):
        if x < self.start_x | y < self.start_y:
            return False
        actual_x = np.floor(x - self.start_x)
        actual_y = np.floor(y - self.start_y)
        section = self.cord_to_section[actual_y][actual_x]

        if self.sections[section] == 0:
            self.sections[section] = 1
        else:
            self.sections[section] = 0
