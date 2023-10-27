import random
from digit_sqr import DigitSqr
import numpy as np


class GeneratePuzzle:
    def __init__(self, screen):
        self.screen = screen
        self.digits = []
        self.generate_puzzle()

    def generate_puzzle(self):
        self.digits = []
        while len(self.digits) != 9:
            num = random.randint(0, 8)
            if num not in self.digits:
                self.digits.append(num)
        print(self.digits)
        # if not self.is_solvable(self.digits) % 2 == 0:
        #     print("re-generating")
        #     self.generate_puzzle()

        self.digits = np.array(self.digits).reshape((3, 3))
        return self.digits

    def draw_puzzle(self, digits):
        counter_x = 1
        counter_y = 1
        puzzle = []
        for digit in digits:
            puzzle.append(
                DigitSqr(self.screen, digit, 100 * counter_x, 100 * counter_y)
            )
            counter_x += 1
            if counter_x % 4 == 0:
                counter_x = 1
                counter_y += 1

        return puzzle
