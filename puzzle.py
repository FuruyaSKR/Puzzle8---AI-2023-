import time

import pygame
from GeneratePuzzle import GeneratePuzzle


class Puzzle:
    def __init__(self, route):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.dist = 200

        pygame.init()
        pygame.font.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Puzzle8 - BCC IA/2023 ")
        self.screen.fill(self.black)
        self.generate_puzzle = GeneratePuzzle(self.screen)
        self.route = route

    def initialization(self):
        self.finish = False
        self.you_win = False
        count = 0
        solve = False

        while not self.finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish = True

            # TODO COLOCAR BOTÃO AQUI

            if count < len(self.route):
                if count == 0 or solve:
                    self.generate_puzzle.draw_puzzle(self.route[count])
                    count += 1

            # else:
            #     self.finish = True
            #     break

            pygame.display.update()
            self.clock.tick(60)
            time.sleep(2)

        pygame.quit()
        quit()
