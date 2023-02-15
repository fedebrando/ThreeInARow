'''
P2. 3 in a row, logical control
@author Federico Brandini, Gianmarco Fogu
'''
from boardgame import BoardGame
from boardgamegui import gui_play
from random import randint, choice
import copy
G, W, B = 0, 1, 2
NE_B_NE_W = -1 # né nera né bianca

class ThreeInARow(BoardGame):
    def __init__(self, filePath: str):
        self._board = []
        self._coordCelleFisse = []
        
        # inizializzazione del gioco
        with open(filePath, "r") as cfg:
            try:
                yc = 0
                for line in cfg:
                    xc = 0
                    line = line.split(',')
                    riga = []
                    for val in line:
                        val = int(val)
                        riga.append(val)
                        if val != G:
                            self._coordCelleFisse.append((xc, yc))
                        xc += 1
                    self._board.append(riga)
                    yc += 1
            except OSError as e:
                print(e)
            except ValueError as e:
                print(e)
            except:
                print("Errore non specificato.")
        
        self._ordine = len(self._board)
    
    def _almeno_unaG_riga(self, y: int) -> bool:
        for x in range(self._ordine):
            if self._board[y][x] == G:
                return True
        return False
    
    def _meta_stesso_colore_riga(self, y: int) -> int:
        if not self._almeno_unaG_riga(y):
            return NE_B_NE_W
        board = self._board
        celleB = 0
        celleW = 0
        for x in range(self._ordine):
            if board[y][x] == B:
                celleB += 1
            elif board[y][x] == W:
                celleW += 1
                
        if celleB == self._ordine // 2:
            return B
        elif celleW == self._ordine // 2:
            return W
        return NE_B_NE_W
    
    def _almeno_unaG_colonna(self, x) -> bool:
        for y in range(self._ordine):
            if self._board[y][x] == G:
                return True
        return False
    
    def _meta_stesso_colore_colonna(self, x: int) -> int:
        if not self._almeno_unaG_colonna(x):
            return NE_B_NE_W
        
        board = self._board
        celleB = 0
        celleW = 0
        for y in range(self._ordine):
            if board[y][x] == B:
                celleB += 1
            elif board[y][x] == W:
                celleW += 1
                
        if celleB == self._ordine // 2:
            return B
        elif celleW == self._ordine // 2:
            return W
        return NE_B_NE_W
    
    def _set_meta_celle_riga(self, y: int, color: int):
        '''
        imposta le celle grigie della riga 'y' del colore opposto a quello ricevuto (W -> B, B -> W)
        '''
        colorAltraMeta = (B if color == W else W)
        for x in range(self._ordine):
            if self._board[y][x] == G:
                self._board[y][x] = colorAltraMeta
    
    def _set_meta_celle_colonna(self, x: int, color: int):
        colorAltraMeta = (B if color == W else W)
        for y in range(self._ordine):
            if self._board[y][x] == G:
                self._board[y][x] = colorAltraMeta
    
    def _auto_meta(self) -> bool:
        '''
        Colora di un colore le celle grigie di una riga o di una colonna se almeno metà sono già del colore opposto.
        Restituisce True nel caso ci siano state modifiche alla matrice principale del gioco, false altrimenti.
        '''
        for y in range(self._ordine):
            colorPiuDiMeta = self._meta_stesso_colore_riga(y)
            if colorPiuDiMeta != NE_B_NE_W :
                self._set_meta_celle_riga(y, colorPiuDiMeta)
                return True
        for x in range(self._ordine):
            colorPiuDiMeta = self._meta_stesso_colore_colonna(x)
            if colorPiuDiMeta != NE_B_NE_W:
                self._set_meta_celle_colonna(x, colorPiuDiMeta)
                return True
        return False
            
    def _2celle_uguali_riga(self, y: int) -> (int, int):
        '''
        Nel caso in cui alla riga 'y' sia presente una sequenza di due colori uguali, restituisce l'indice della cella
        la quale dovra avere per forza colore diverso, specificando anche quale colore.
        Se non vi è nessuna sequenza di questo tipo, restituisce None.
        '''
        board = self._board
        for x in range(self._ordine - 2):
            if board[y][x] != G and board[y][x] == board[y][x+1] and board[y][x+2] == G:
                coloreOpposto = (B if board[y][x] == W else W)
                return (x+2, coloreOpposto)
            if board[y][-x-1] != G and board[y][-x-1] == board[y][-x-2] and board[y][-x-3] == G:
                coloreOpposto = (B if board[y][-x-1] == W else W)
                return (-x-3, coloreOpposto)
        return None
        
    def _2celle_uguali_colonna(self, x: int) -> (int, int):
        # analogo al precedente, ma per le colonne
        board = self._board
        for y in range(self._ordine - 2):
            if board[y][x] != G and board[y][x] == board[y+1][x] and board[y+2][x] == G:
                coloreOpposto = (B if board[y][x] == W else W)
                return (y+2, coloreOpposto)
            if board[-y-1][x] != G and board[-y-1][x] == board[-y-2][x] and board[-y-3][x] == G:
                coloreOpposto = (B if board[-y-1][x] == W else W)
                return (-y-3, coloreOpposto)
        return None
            
    def _auto_2inline(self) -> bool: # il valore logico restituito indica se la funzione ha modificato la matrice o meno
        '''
        Colora una cella di una riga o di una colonna nel caso in cui sia preceduta o seguita da due celle di egual colore che non sia grigio.
        Restituisce True nel caso ci siano state modifiche alla matrice principale del gioco, false altrimenti.
        '''
        board = self._board
        for y in range(self._ordine):
            cellColor = self._2celle_uguali_riga(y)
            if not (cellColor is None):
                board[y][cellColor[0]] = cellColor[1]
                return True
        for x in range(self._ordine):
            cellColor = self._2celle_uguali_colonna(x)
            if not (cellColor is None):
                board[cellColor[0]][x] = cellColor[1]
                return True
        return False
            
    def automatism(self) -> bool:
        if not self._auto_2inline():
            return self._auto_meta()
        return True
               
    def _thereare_oltre_meta_stesso_colore(self) -> bool:
        board = self._board
        ordine = self._ordine

        for y in range(ordine):
            celleB = 0
            celleW = 0
            for x in range(ordine):
                if board[y][x] == B:
                    celleB += 1
                    if celleB > ordine // 2:
                        return True
                elif board[y][x] == W:
                    celleW += 1
                    if celleW > ordine // 2:
                        return True
        for x in range(ordine):
            celleB = 0
            celleW = 0
            for y in range(ordine):
                if board[y][x] == B:
                    celleB += 1
                    if celleB > ordine // 2:
                        return True
                elif board[y][x] == W:
                    celleW += 1
                    if celleW > ordine // 2:
                        return True
        return False
    
    def _thereare_3celle_stesso_colore(self) -> bool:
        board = self._board
        for y in range(self._ordine):
            for x in range(self._ordine - 2):
                if board[y][x] != G and board[y][x] == board[y][x+1] and board[y][x+1] == board[y][x+2]:
                    return True
        for x in range(self._ordine):
            for y in range(self._ordine - 2):
                if board[y][x] != G and board[y][x] == board[y+1][x] and board[y+1][x] == board[y+2][x]:
                    return True
        return False
    
    def suggerimento(self):
        if self.unsolvable():
            return

        for y in range(self._ordine):
            for x in range(self._ordine):
                if self._board[y][x] == G:
                    boardCtrlZ = copy.deepcopy(self._board) # salvataggio stato attuale
                    self._board[y][x] = W
                    self.automatism()
                    if self.unsolvable():
                        self._board = boardCtrlZ
                        self._board[y][x] = B
                        return
                    else:
                        self._board = boardCtrlZ
                        boardCtrlZ = copy.deepcopy(self._board)
                        self._board[y][x] = B
                        self.automatism()
                        if self.unsolvable():
                            self._board = boardCtrlZ
                            self._board[y][x] = W
                            return
                        else:
                            self._board = boardCtrlZ
                            
    def solution(self, y: int, x: int) -> bool:
        while self.automatism():
            continue
        if self.unsolvable():
            return False
        
        while y < self._ordine and self._board[y][x] != G:
            if x + 1 == self._ordine:
                y += 1
            x = (x + 1) % self._ordine
            
        if y < self._ordine:
            saved = copy.deepcopy(self._board)
            for color in (B, W):
                self._board[y][x] = color
                if self.solution(y if x + 1 != self._ordine else y + 1, (x + 1) % self._ordine):
                    return True
                self._board = saved  # backtracking
        return self.finished()
        
    
    def unsolvable(self) -> bool:
        return self._thereare_oltre_meta_stesso_colore() or self._thereare_3celle_stesso_colore()
        
    def play_at(self, x: int, y: int):
        if not ((x, y) in self._coordCelleFisse):
            self._board[y][x] = (self._board[y][x] + 1) % 3
        
    def flag_at(self, x: int, y: int):
        return
    
    def value_at(self, x: int, y: int) -> str:
        val = self._board[y][x]

        if val == G:
            return "-"
        if val == W:
            strVal = "W"
        else:
            strVal = "B"
        
        return strVal + "f" if (x, y) in self._coordCelleFisse else strVal # 'f' indica che la cella è fissa
        
    def cols(self) -> int:
        return self.rows()
    
    def rows(self) -> int:
        return self._ordine
        
    def finished(self) -> bool:
        ordine = self._ordine
        brd = self._board
        for riga in brd:
            if G in riga or riga.count(W) != riga.count(B):
                return False
            
        for r in range(ordine - 2):
            for c in range(ordine - 2):
                if brd[r][c] == brd[r][c + 1] and brd[r][c + 1] == brd[r][c + 2] or brd[r][c] == brd[r + 1][c] and brd[r + 1][c] == brd[r + 2][c]:
                    return False
                
        return True
    
    def message(self) -> str:
        return "Complimenti, hai vinto!"
    
def main():
    game = ThreeInARow("hard.cfg") # select your difficulty level among easy, medium, hard and hardest
    gui_play(game)
    
main()
    