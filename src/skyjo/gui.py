import pygame
import os
from skyjo import constants as const


class SkyjoView():
    ''' Singleton class that displays the model in the GUI '''
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            pygame.init()
            working_dir = os.path.dirname(__file__)
            cls.__instance._art_dir = os.path.join(working_dir,
                                                   const.CARD_ART_DIR)
            cls.__instance._screen = (
                pygame.display.set_mode((const.SCREEN_WIDTH,
                                         const.SCREEN_HEIGHT))
            )
            pygame.display.set_caption('Skyjo')
            cls.__instance._clock = pygame.time.Clock()
        return cls.__instance

    @classmethod
    def update_display(cls, game_state):
        ui_coords = {
            'hand': [],
            'active': []
        }

        # Set convenience variables
        art_dir = cls.__instance._art_dir
        card_back = const.CARD_ART['card_back']
        placehoder = const.CARD_ART['placeholder']
        players = game_state.get_players()
        no_of_players = len(players)
        current_player_no = game_state.current_player_index()
        deck = game_state.get_deck()
        screen = cls.__instance._screen
        clock = cls.__instance._clock

        screen.fill(const.SADDLE_BROWN)

        # display player hand panels
        hand_panel_spacer = 0
        for player_no, player in enumerate(players):
            card_x = const.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            card_y = const.HAND_PANEL_PADDING_TOP

            hand_rects = []

            card_itr = 0
            for row in range(3):
                for col in range(4):
                    card_filename = card_back
                    current_card = player.get_card(card_itr)
                    if player.card_visible(card_itr):
                        card_filename = const.CARD_ART[current_card]
                    card_itr += 1

                    card_img = pygame.image.load(os.path.join(art_dir,
                                                              card_filename))
                    card_img = pygame.transform.scale(card_img,
                                                      (const.CARD_WIDTH,
                                                       const.CARD_HEIGHT))
                    card_rect = card_img.get_rect()
                    card_rect.x = card_x + (const.CARD_PADDING * col)
                    card_rect.y = card_y + (const.CARD_PADDING * row)

                    hand_rects.append(card_rect)

                    screen.blit(card_img, card_rect)
                    card_x += card_rect.width
                    card_h = card_rect.height
                card_y += card_h
                card_x = const.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
            ui_coords['hand'].append(hand_rects)

            # Draw active card panel
            card_no = player.get_active_card()
            card_filename = placehoder
            if card_no is not None:
                card_filename = const.CARD_ART[card_no]
            card_img = pygame.image.load(os.path.join(art_dir, card_filename))
            card_img = pygame.transform.scale(card_img,
                                              (const.CARD_WIDTH + 2,
                                               const.CARD_HEIGHT + 2))
            card_rect = card_img.get_rect()
            card_rect.x = const.DRAW_PANEL_CARD_POS_X + hand_panel_spacer
            card_rect.y = const.DRAW_PANEL_CARD_POS_Y
            screen.blit(card_img, card_rect)
            ui_coords['active'].append(card_rect)

            # Draw player score in active card panel
            points = player.get_round_points()
            points_label_colour = const.POINTS_LBL_COLOUR
            font = pygame.font.SysFont(const.MAIN_FONT,
                                       const.POINTS_LBL_FONT_SIZE)
            txt_points = font.render(f'Round points: {points}',
                                     True, points_label_colour)
            txt_rect = txt_points.get_rect()
            txt_rect.x = const.DRAW_PANEL_POINTS_POS_X + hand_panel_spacer
            txt_rect.y = const.DRAW_PANEL_POINTS_POS_Y
            screen.blit(txt_points, txt_rect)

            # Draw player name label
            player_label_colour = const.PLAYER_LBL_COLOUR_DEFAULT
            if player_no == current_player_no:
                player_label_colour = const.PLAYER_LBL_COLOUR_ACTIVE

            font = pygame.font.SysFont(const.MAIN_FONT,
                                       const.PLAYER_LBL_FONT_SIZE)
            txt_player_no = font.render(f'Player {player_no + 1}',
                                        True, player_label_colour)
            txt_rect = txt_player_no.get_rect()
            txt_rect.x = int(const.PLAYER_LBL_POS_X -
                             (txt_player_no.get_width() / 2) +
                             hand_panel_spacer)
            txt_rect.y = const.PLAYER_LBL_POS_Y
            screen.blit(txt_player_no, txt_rect)

            hand_panel_spacer += const.HAND_PANEL_WIDTH

        # Draw the deck (discard and draw piles)
        card_no = deck.get_discarded_card()
        card_filename = placehoder
        if card_no is not None:
            card_filename = const.CARD_ART[card_no]
        card_img = pygame.image.load(os.path.join(art_dir, card_filename))
        card_img = pygame.transform.scale(card_img, (const.CARD_WIDTH + 2,
                                                     const.CARD_HEIGHT + 2))
        card_rect = card_img.get_rect()
        card_rect.x = int(((no_of_players * const.DRAW_PANEL_WIDTH) / 2) -
                          (const.CARD_WIDTH * 1.5))
        card_rect.y = const.DECK_PANEL_Y
        screen.blit(card_img, card_rect)
        ui_coords['discard'] = card_rect

        card_filename = card_back
        card_img = pygame.image.load(os.path.join(art_dir, card_filename))
        card_img = pygame.transform.scale(card_img, (const.CARD_WIDTH + 2,
                                                     const.CARD_HEIGHT + 2))
        card_rect = card_img.get_rect()
        card_rect.x = int(((no_of_players * const.DRAW_PANEL_WIDTH) / 2) +
                          (const.CARD_WIDTH * 1.5))
        card_rect.y = const.DECK_PANEL_Y
        screen.blit(card_img, card_rect)
        ui_coords['draw'] = card_rect

        # End of function
        pygame.display.flip()
        clock.tick(const.TICK_RATE)
        return ui_coords
