'''
P2. 3 in a row, user interface
@author Federico Brandini, Gianmarco Fogu
'''

import g2d
from boardgame import BoardGame
from time import time

W, H = 40, 40
LONG_PRESS = 0.5
COLOR_B = (0, 0, 0)
COLOR_W = (255, 255, 255)
COLOR_G = (156, 156, 156)
COLOR_BORDER = (210, 210, 210)

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self.update_buttons()

    def tick(self):
        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._downtime > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
            self.update_buttons()
            
        if g2d.key_pressed("a"):
            self._game.automatism()
            self.update_buttons()
        elif g2d.key_pressed("u"):
            if self._game.unsolvable():
                g2d.alert("La configurazione attuale è irrisolvibile.")
            else:
                g2d.alert("La configurazione attuale può essere risolta.")
        elif g2d.key_pressed("h"):
            self._game.suggerimento()
            self.update_buttons()
        elif g2d.key_pressed("s"):
            if g2d.confirm("Vuoi davvero guardare la soluzione?"):
                self._game.solution(0, 0)
                self.update_buttons()

    def update_buttons(self):
        g2d.clear_canvas()
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(rows):
            for x in range(cols):
                value = self._game.value_at(x, y)
                if value == "-":
                    color = COLOR_G
                elif "W" in value:
                    color = COLOR_W
                elif "B" in value:
                    color = COLOR_B
                g2d.set_color(color)
                g2d.fill_rect((x * W, y * H, W, H))
                if "f" in value: # segnalazione della cella fissa
                    center = x * W + W//2, y * H + H//2
                    g2d.set_color(COLOR_BORDER)
                    g2d.draw_text_centered("F", center, H//2)
        g2d.set_color(COLOR_BORDER)
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
            
        g2d.update_canvas()
        
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
