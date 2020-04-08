import pygame
import itertools
from random import randrange
import os
from skyjo import constants

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
    def draw_pile_size(cls):
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
        return self._hand[index][0]

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

    def card_visible(self, index):
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
    def current_player_index(cls):
        ''' Returns an int representing the index of the currently active player '''
        return cls.__instance._current_player

def gui():
    current_path = os.path.dirname(__file__) # Where your .py file is located
    art_path = os.path.join(current_path, 'art') # The image folder path

    deck = SkyjoDeck()
    dealer = Dealer(deck)
    players = []
    for i in range(4):
        players.append(Player())
    dealer.deal_hand(players)
    game_state = GameState(players, deck)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    running = True

    while running:
        mouse_clicked = False
        current_player_index = game_state.current_player_index()
        current_player = game_state.get_current_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_clicked = True

        screen.fill(constants.SADDLE_BROWN)

        hand_panel_spacer = 0
        ui_elements = []

        for player in game_state.get_players():
            card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            card_y = constants.HAND_PANEL_PADDING_TOP
            card_coords = []

            card_itr = 0

            for row in range(3):
                for col in range(4):
                    constants.CARD_ART_filename = 'card_back.png'
                    current_card = player.get_card(card_itr)
                    if player.card_visible(card_itr):
                        constants.CARD_ART_filename = constants.CARD_ART[current_card]
                    card_itr += 1

                    card_img = pygame.image.load(os.path.join(art_path, constants.CARD_ART_filename))
                    card_img = pygame.transform.scale(card_img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))
                    rect_card = card_img.get_rect()
                    rect_card.x = card_x + (constants.CARD_PADDING * col)
                    rect_card.y = card_y + (constants.CARD_PADDING * row)

                    card_coords.append(rect_card)

                    screen.blit(card_img, rect_card)
                    card_x += rect_card.width
                    card_h = rect_card.height
                card_y += card_h
                card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            ui_elements.append(card_coords)
            hand_panel_spacer += constants.HAND_PANEL_WIDTH               
        
        if mouse_clicked:
            for i, card in enumerate(ui_elements[current_player_index]):
                if card.collidepoint(mouse_x, mouse_y):
                    if not current_player.card_visible(i):
                        current_player.reveal_card(i)
                        game_state.end_turn()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    gui() 