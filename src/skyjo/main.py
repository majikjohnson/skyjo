import tkinter as tk
import itertools
from random import randrange


class SkyjoDeck(object):

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._draw_pile = []
            cls.__instance._draw_pile.extend(itertools.repeat(-2, 5))
            cls.__instance._draw_pile.extend(itertools.repeat(0, 15))
            cls.__instance._draw_pile.extend(itertools.repeat(-1, 10))
            for num in range(1, 13):
                cls.__instance._draw_pile.extend(itertools.repeat(num, 10))
        return cls.__instance

    @classmethod
    def draw_card(cls):
        return cls.__instance._draw_pile.pop(randrange(len(cls.__instance._draw_pile)))

class Player:
    def __init__(self, deck):
        self._board = []
        for _ in range(3):
            for _ in range(4):
                self._board.append((deck.draw_card(), True))
        print(self._board)

    def get_card(self, index):
        if self._board[index][1] is True:
            return self._board[index][0]
        return ' '

def print_board(player, window):
    card_index = 0
    for row_no in range(3):
        for col_no in range(4):
            frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
            frame.grid(row=row_no, column=col_no, padx=5, pady=5)
            label = tk.Label(master=frame, text=f'{player.get_card(card_index)}')
            label.pack()
            card_index = card_index + 1

def gui():

    root = tk.Tk()

    deck = SkyjoDeck()
    player1 = Player(deck)

    print_board(player1, root)

    root.mainloop()

if __name__ == "__main__":
    gui() 