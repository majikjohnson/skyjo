from random import randrange
import itertools
from enum import Enum


class Deck(object):
    ''' Sigleton class used for managing the card deck '''
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
            card = cls.__instance.draw_card()
            cls.__instance.discard_card(card)
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
    def draw_pile_size(cls):
        ''' Return an int representing the number of cards left in the draw pile '''
        return len(cls.__instance._draw_pile)

    @classmethod
    def deal_hand(cls, players):
        ''' takes a list of players and creates a hand for each one '''
        for player in players:
            cards = []
            for _ in range(12):
                cards.append(cls.__instance.draw_card())
            player.set_hand(cards)


class Player:
    ''' Represents the states and operations for a player '''
    def __init__(self):
        self._hand = []
        self._active_card = None

    def set_hand(self, cards):
        ''' Takes a list of cards and adds them to hand '''
        for card in cards:
            self._hand.append([card, False])

    def get_card(self, index):
        ''' Returns the card at the given index '''
        return self._hand[index][0]

    def reveal_card(self, index):
        ''' Sets the card at the given index to visible '''
        self._hand[index][1] = True
        return self._hand[index][0]

    def switch_card(self, index, deck):
        ''' Switches the card at the given index with the last drawn card.  Old card is added to the deck discard pile '''
        old_card = self._hand[index][0]
        self._hand[index][0] = self._active_card[0]
        self._active_card = None
        deck.discard_card(old_card)

    def card_visible(self, index):
        ''' Returns boolean indicating if the card at the given index is visibile or not '''
        return self._hand[index][1]

    def draw_card(self, deck):
        ''' Draw a card from the deck draw pile '''
        self._active_card = (deck.draw_card(), True)

    def draw_discarded_card(self, deck):
        ''' Draw a card from the deck discard pile '''
        self._active_card = (deck.draw_discarded_card(), False)

    def get_active_card(self):
        ''' Returns the most recently drawn card.  If no card is active then returns None '''
        if self._active_card is None:
            return None
        return self._active_card[0]

    def get_active_card_source(self):
        ''' Returns either the string 'draw' or 'discard' to indicate where the active card was drawn from '''
        if self._active_card is None:
            return None
        if self._active_card[1]:
            return 'draw_pile'
        return 'discard_pile'

    def discard_active_card(self, deck):
        ''' Sends most recently drawn card to the discard pile '''
        if self._active_card is not None:
            deck.discard_card(self._active_card[0])
            self._active_card = None

    def all_cards_visible(self):
        ''' Returns a boolean indicating if all of the player's cards are visible or not '''
        for card in self._hand:
            if card[1] is False:
                return False
        return True

    def visible_card_count(self):
        visible_cards = 0
        for card in self._hand:
            if card[1] == True:
                visible_cards += 1
        return visible_cards

    def get_round_points(self):
        points = 0
        for card in self._hand:
            if card[1]:
                points += card[0]
        return points


Phase = Enum('Phase', 'round_prep draw discard game_over')


class GameState(object):
    ''' Singleton class that keeps track of the state of the game '''
    __instance = None

    round_prep, draw, discard, game_over = (0, 1, 2, 3)

    def __new__(cls, players, deck):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._players = players
            cls.__instance._deck = deck
            cls.__instance._current_player = 0
            cls.__instance.current_phase = Phase.round_prep
            cls.__instance._game_over = False
            cls.__instance._remaining_turns = deck.draw_pile_size()
        return cls.__instance

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

    @classmethod
    def get_current_player(cls):
        ''' Returns the player who's turn it currently is '''
        return cls.__instance._players[cls.__instance._current_player]

    @classmethod
    def get_players(cls):
        ''' Returns a list containing all players '''
        return cls.__instance._players

    @classmethod
    def rotate_player(cls):
        ''' Sets the current plater to the next player '''
        if cls.__instance._current_player == len(cls.__instance._players) - 1:
            cls.__instance._current_player = 0
        else:
            cls.__instance._current_player += 1

    @classmethod
    def active_player_index(cls):
        ''' Returns an int representing the index of the currently active player '''
        return cls.__instance._current_player

    @classmethod
    def set_current_player(cls, index):
        ''' Sets the current player to the given index '''
        cls.__instance._current_player = index

    @classmethod
    def get_deck(cls):
        ''' Returns the deck '''
        return cls.__instance._deck

    @classmethod
    def highest_points_player_index(cls):
        ''' Returns the index of the player with the highest points in the current round '''
        player_index = 0
        highest_points = -5
        for i, player in enumerate(cls.__instance._players):
            if player.get_round_points() > highest_points:
                highest_points = player.get_round_points()
                player_index = i
        return player_index
