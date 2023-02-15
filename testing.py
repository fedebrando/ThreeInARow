'''
P2. 3 in a row, testing
@author Federico Brandini, Gianmarco Fogu
'''
# comment the main function if you want to test

import unittest
from threeInARow import ThreeInARow
from random import choice

class Param3inARowTest(unittest.TestCase):
    def t_play_at(self):
        game = ThreeInARow("medium.cfg")
        
        game.play_at(1, 3)
        self.assertTrue(game.value_at(1, 3) == "W")
        game.play_at(1, 3)
        self.assertTrue(game.value_at(1, 3) == "B")
        game.play_at(1, 3)
        self.assertTrue(game.value_at(1, 3) == "-")
        
    def t_finished_grey_cells(self):
        game = ThreeInARow("medium.cfg")
        
        for y in range(game.rows()):
            for x in range(game.cols()):
                if (x != 1 and y != 3):
                    game.play_at(x, y)
                    if choice([True, False]):
                        game.play_at(x, y) # per avere anche celle nere
        self.assertTrue(not game.finished())
        
    def t_finished_3cells_equal(self):
        game = ThreeInARow("medium.cfg")
        
        for y in range(game.rows()):
            for x in range(game.cols()):
                game.play_at(x, y)
                if choice([True, False]) and not ((x, y) in [(1, 3), (2, 3), (3, 3)]):
                    game.play_at(x, y) # per avere anche celle nere
        
        self.assertTrue(not game.finished())
        
    def t_finished_unbalanced_cells(self):
        game = ThreeInARow("medium.cfg")
        
        for y in range(game.rows()):
            for x in range(game.cols()):
                game.play_at(x, y)
                if choice([True, False]) and not ((x, y) in [(1, 0), (1, 1), (1, 3), (1, 5), (1, 7)]):
                    game.play_at(x, y) # per avere anche celle nere
        
        self.assertTrue(not game.finished())
        
def main():
    test = Param3inARowTest()
    test.t_play_at()
    test.t_finished_grey_cells()
    test.t_finished_3cells_equal()
    test.t_finished_unbalanced_cells()
        
main()