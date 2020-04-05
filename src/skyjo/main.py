import tkinter as tk
import itertools
from random import randrange


class SkyjoDeck(object):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._discard_pile = []
            cls.__instance._draw_pile = []
            cls.__instance._draw_pile.extend(itertools.repeat(-2, 5))
            cls.__instance._draw_pile.extend(itertools.repeat(0, 15))
            cls.__instance._draw_pile.extend(itertools.repeat(-1, 10))
            for num in range(1, 13):
                cls.__instance._draw_pile.extend(itertools.repeat(num, 10))
        return cls.__instance

    @classmethod
    def draw_card(cls):
        ''' Allows the player to draw a card from the draw pile '''
        return cls.__instance._draw_pile.pop(randrange(len(cls.__instance._draw_pile)))

    @classmethod
    def discard_card(cls, card):
        ''' Adds the given card to the top of the discard pile'''
        cls.__instance._discard_pile.append(card)

    @classmethod
    def draw_discarded_card(cls):
        ''' Allows the player to draw the card on the top of the draw pile '''
        return cls.__instance._discard_pile.pop()

    @classmethod
    def get_discarded_card(cls):
        ''' Returns the card on the top of the draw pile (for display purposes)'''
        if cls.__instance._discard_pile:
            return cls.__instance._discard_pile[-1]
        return None

    @classmethod
    def cards_in_draw_pile(cls):
        ''' Return an int representing the number of cards left in the draw pile '''
        return len(cls.__instance._draw_pile)

class Player:
    def __init__(self):
        self._hand = []
        self._drawn_card = None

    def set_hand(self, cards):
        ''' Takes a list of cards and adds them to hand '''
        for card in cards:
            self._hand.append([card, False])

    def get_card(self, index):
        ''' Returns the card at the given index '''
        if self._hand[index][1] is True:
            return self._hand[index][0]
        return ' '

    def reveal_card(self, index):
        ''' Sets the card at the given index to visible '''
        self._hand[index][1] = True
        return self._hand[index][0]

    def switch_card(self, index, deck):
        ''' Switches the card at the given index with the last drawn card.  Old card is added to the deck discard pile '''
        old_card = self._hand[index][0]
        self._hand[index][0] = self._drawn_card
        deck.discard_card(old_card)
        return self._hand[index][0]

    def is_card_visible(self, index):
        ''' Returns boolean indicating if the card at the given index is visibile or not '''
        return self._hand[index][1]

    def draw_card(self, deck):
        ''' Draw a card from the deck draw pile '''
        self._drawn_card = deck.draw_card()

    def all_cards_visible(self):
        ''' Returns a boolean indicating if all of the player's cards are visibile or not '''
        for card in self._hand:
            if card[1] == False:
                return False
        return True

class Dealer:
    def __init__(self, deck):
        self.deck = deck

    def deal_hand(self, players):
        for player in players:
            cards = []
            for _ in range(12):
                cards.append(self.deck.draw_card())
            player.set_hand(cards)

class GameState(object):
    __instance = None

    def __new__(cls, players, deck):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._players = players
            cls.__instance._current_player = 0
            cls.__instance._game_over = False
            cls.__instance._remaining_turns = deck.draw_pile_size()
    
    @classmethod
    def end_turn(cls):
        ''' Runs end turn procedure and returns a boolean indicating if the game is over or not '''
        cls.__instance._remaining_turns -= 1
        if cls.__instance._remaining_turns > 0:
            if cls.__instance._players[cls.__instance._current_player].all_cards_visible():
                cls.__instance._remaining_turns = len(cls.__instance._players) - 1
            if cls.__instance._current_player == len(cls.__instance._players) - 1:
                cls.__instance._current_player = 0
            else:
                cls.__instance._current_player += 1
            return False
        return True


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
    dealer = Dealer(deck)
    player1 = Player()
    player2 = Player()
    dealer.deal_hand([player1])
    dealer.deal_hand([player2])
    player1.reveal_card(1)
    player1.reveal_card(2)
    player2.reveal_card(5)
    player2.reveal_card(6)

    print(player1._hand)
    print(player2._hand)


    frame_p1 = tk.Frame(master=root, borderwidth=10)
    frame_p2 = tk.Frame(master=root, borderwidth=10)

    print_board(player1, frame_p1)
    print_board(player2, frame_p2)

    frame_p1.grid(row=0, column=0)
    frame_p2.grid(row=0, column=1)

    root.mainloop()

if __name__ == "__main__":
    gui() 