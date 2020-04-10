import pygame
import os
from skyjo import constants as const
from skyjo.game import Deck, Player, GameState

class SkyjoView():
    ''' Singleton class that displays the model in the GUI '''
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            pygame.init()
            working_dir = os.path.dirname(__file__)
            cls.__instance._art_dir = os.path.join(working_dir, const.CARD_ART_DIR)
            cls.__instance._screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
            cls.__instance._clock = pygame.time.Clock()
        return cls.__instance

    @classmethod
    def update_display(cls, game_state):
        ui_coords = {
            'hand': []
        }

        # Set convenience variables
        art_dir = cls.__instance._art_dir
        players = game_state.get_players()
        no_of_players = len(players)
        current_player_no = game_state.current_player_index()
        deck = game_state.get_deck()
        screen = cls.__instance._screen
        clock = cls.__instance._clock

        # diaplay player hand panels
        hand_panel_spacer = 0
        for player_no, player in enumerate(players):
            card_x = const.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            card_y = const.HAND_PANEL_PADDING_TOP

            hand_rects = []

            card_itr = 0
            for row in range(3):
                for col in range(4):
                    card_filename = const.CARD_ART['card_back']
                    current_card = player.get_card(card_itr)
                    if player.card_visible(card_itr):
                        card_filename = const.CARD_ART[current_card]
                    card_itr += 1

                    card_img = pygame.image.load(os.path.join(art_dir, card_filename))
                    card_img = pygame.transform.scale(card_img, (const.CARD_WIDTH, const.CARD_HEIGHT))
                    card_rect = card_img.get_rect()
                    card_rect.x = card_x + (const.CARD_PADDING * col)
                    card_rect.y = card_y + (const.CARD_PADDING * row)

                    hand_rects.append(card_rect)

                    screen.blit(card_img, card_rect)
                    card_x += card_rect.width
                    card_h = card_rect.height
                card_y += card_h
                card_x = const.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            hand_panel_spacer += const.HAND_PANEL_WIDTH
            ui_coords['hand'].append(hand_rects)




        # End of function
        pygame.display.flip()
        clock.tick(const.TICK_RATE)
        return ui_coords
