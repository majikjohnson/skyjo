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
    def show_game_over(cls, game_state):
        screen = cls.__instance._screen
        players = game_state.get_players()
        button_coords = {
            'restart': None,
            'quit': None
        }

        title = const.GAME_OVER_PANEL_TITLE_TEXT

        pygame.draw.rect(
            screen, const.GAME_OVER_PANEL_COLOUR,
            (const.GAME_OVER_PANEL_X, const.GAME_OVER_PANEL_Y,
             const.GAME_OVER_PANEL_WIDTH, const.GAME_OVER_PANEL_HEIGHT)
        )

        # Print title for score panel
        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.GAME_OVER_PANEL_TITLE_FONT_SIZE)
        font.set_bold(True)
        font.set_underline(True)
        txt_title = font.render(title, True, const.GAME_OVER_PANEL_TITLE_COLOUR)
        txt_rect = txt_title.get_rect()
        txt_rect.x = const.GAME_OVER_PANEL_TITLE_X
        txt_rect.y = const.GAME_OVER_PANEL_TITLE_Y
        screen.blit(txt_title, txt_rect)

        # Print scores for each player
        scores = []
        for i, player in enumerate(players):
            scores.append((f'Player {i + 1}', player.get_score()))
        scores.sort(key=lambda tup: tup[1])

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                       const.GAME_OVER_1ST_FONT_SIZE)
        txt_score = font.render(f'1st  -- {scores[0][0]}: {scores[0][1]}',
                                True, const.GAME_OVER_1ST_COLOUR)
        txt_rect = txt_score.get_rect()
        txt_rect.x = const.GAME_OVER_PANEL_TEXT_X
        txt_rect.y = (
            const.GAME_OVER_PANEL_TEXT_Y +
            (0 * const.GAME_OVER_PANEL_ITEM_PADDING_TOP)
        )
        screen.blit(txt_score, txt_rect)

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                const.GAME_OVER_2ND_FONT_SIZE)
        txt_score = font.render(f'2nd -- {scores[1][0]}: {scores[1][1]}',
                                True, const.GAME_OVER_2ND_COLOUR)
        txt_rect = txt_score.get_rect()
        txt_rect.x = const.GAME_OVER_PANEL_TEXT_X
        txt_rect.y = (
            const.GAME_OVER_PANEL_TEXT_Y +
            (1 * const.GAME_OVER_PANEL_ITEM_PADDING_TOP)
        )
        screen.blit(txt_score, txt_rect)

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                const.GAME_OVER_3RD_FONT_SIZE)
        txt_score = font.render(f'3rd -- {scores[2][0]}: {scores[2][1]}',
                                True, const.GAME_OVER_3RD_COLOUR)
        txt_rect = txt_score.get_rect()
        txt_rect.x = const.GAME_OVER_PANEL_TEXT_X
        txt_rect.y = (
            const.GAME_OVER_PANEL_TEXT_Y +
            (2 * const.GAME_OVER_PANEL_ITEM_PADDING_TOP)
        )
        screen.blit(txt_score, txt_rect)

        # Print restart button
        pygame.draw.rect(
            screen, const.GAME_OVER_RESTART_BUTTON_COLOUR,
            (const.GAME_OVER_RESTART_BUTTON_X, const.GAME_OVER_RESTART_BUTTON_Y,
             const.GAME_OVER_RESTART_BUTTON_WIDTH, const.GAME_OVER_RESTART_BUTTON_HEIGHT)
        )

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.GAME_OVER_RESTART_BUTTON_FONT_SIZE)
        txt_button = font.render(const.GAME_OVER_RESTART_BUTTON_TEXT,
                                 True, const.GAME_OVER_RESTART_BUTTON_TEXT_COLOUR)
        txt_rect = txt_button.get_rect()
        txt_rect.x = const.GAME_OVER_RESTART_BUTTON_TEXT_X
        txt_rect.y = const.GAME_OVER_RESTART_BUTTON_TEXT_Y
        screen.blit(txt_button, txt_rect)
        button_coords['restart'] = txt_rect

        # Print Quit button
        pygame.draw.rect(
            screen, const.GAME_OVER_QUIT_BUTTON_COLOUR,
            (const.GAME_OVER_QUIT_BUTTON_X, const.GAME_OVER_QUIT_BUTTON_Y,
             const.GAME_OVER_QUIT_BUTTON_WIDTH, const.GAME_OVER_QUIT_BUTTON_HEIGHT)
        )

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.GAME_OVER_QUIT_BUTTON_FONT_SIZE)
        txt_button = font.render(const.GAME_OVER_QUIT_BUTTON_TEXT,
                                 True, const.GAME_OVER_QUIT_BUTTON_TEXT_COLOUR)
        txt_rect = txt_button.get_rect()
        txt_rect.x = const.GAME_OVER_QUIT_BUTTON_TEXT_X
        txt_rect.y = const.GAME_OVER_QUIT_BUTTON_TEXT_Y
        screen.blit(txt_button, txt_rect)
        button_coords['quit'] = txt_rect

        pygame.display.flip()
        return button_coords






    @classmethod
    def show_scores(cls, game_state, type='round'):
        screen = cls.__instance._screen
        players = game_state.get_players()

        title = const.SCORE_PANEL_ROUND_TITLE

        if type == 'total':
            title = const.SCORE_PANEL_TOTAL_TITLE


        pygame.draw.rect(
            screen, const.SCORE_PANEL_COLOUR,
            (const.SCORE_PANEL_X, const.SCORE_PANEL_Y,
             const.SCORE_PANEL_WIDTH, const.SCORE_PANEL_HEIGHT)
        )

        scores = []
        for i, player in enumerate(players):
            if type == 'total':
                score = player.get_score()
                
            else:
                score = player.get_round_points()
            scores.append((f'Player {i + 1}', score))
        scores.sort(key=lambda tup: tup[1])

        # Print title for score panel
        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.SCORE_PANEL_TITLE_FONT_SIZE)
        font.set_bold(True)
        font.set_underline(True)
        txt_title = font.render(title, True, const.SCORE_PANEL_TEXT_COLOUR)
        txt_rect = txt_title.get_rect()
        txt_rect.x = const.SCORE_PANEL_TITLE_X
        txt_rect.y = const.SCORE_PANEL_TITLE_Y
        screen.blit(txt_title, txt_rect)

        # Print scores for each player
        for i, score in enumerate(scores):
            font = pygame.font.Font(const.RETRO_COMPUTER,
                                       const.SCORE_PANEL_TEXT_FONT_SIZE)
            txt_score = font.render(f'{i + 1}. {score[0]}: {score[1]}',
                                    True, const.SCORE_PANEL_TEXT_COLOUR)
            txt_rect = txt_score.get_rect()
            txt_rect.x = const.SCORE_PANEL_TXT_X
            txt_rect.y = (
                const.SCORE_PANEL_TXT_Y +
                (i * const.SCORE_PANEL_ITEM_PADDING_TOP)
            )
            screen.blit(txt_score, txt_rect)

        # Print continue button
        pygame.draw.rect(
            screen, const.SCORE_PANEL_BUTTON_COLOUR,
            (const.SCORE_PANEL_BUTTON_X, const.SCORE_PANEL_BUTTON_Y,
             const.SCORE_PANEL_BUTTON_WIDTH, const.SCORE_PANEL_BUTTON_HEIGHT)
        )

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.SCORE_PANEL_BUTTON_FONT_SIZE)
        txt_button = font.render(const.SCORE_PANEL_BUTTON_TEXT,
                                 True, const.SCORE_PANEL_BUTTON_TEXT_COLOUR)
        txt_rect = txt_button.get_rect()
        txt_rect.x = const.SCORE_PANEL_BUTTON_TEXT_X
        txt_rect.y = const.SCORE_PANEL_BUTTON_TEXT_Y
        screen.blit(txt_button, txt_rect)

        pygame.display.flip()
        return txt_rect

    @classmethod
    def update_display(cls, game_state):
        ui_coords = {
            'hand': [],
            'active': []
        }

        # Set convenience variables
        players = game_state.get_players()
        no_of_players = len(players)
        active_player_no = game_state.active_player_index()
        deck = game_state.get_deck()
        screen = cls.__instance._screen
        clock = cls.__instance._clock

        screen.fill(const.SADDLE_BROWN)

        # display player hand panels
        panel_spacer = 0
        for player_no, player in enumerate(players):
            # Displaye player names
            cls.__instance._blit_player_name_label(screen,
                                                   player_no,
                                                   active_player_no,
                                                   panel_spacer)

            # Display player's hand
            player_rects = cls.__instance._blit_player_hand_panel(screen,
                                                                  player,
                                                                  panel_spacer)
            ui_coords['hand'].append(player_rects)

            # Display player's active card panel
            panel_rect = cls.__instance._blit_active_card_panel(screen,
                                                                player,
                                                                panel_spacer)
            ui_coords['active'].append(panel_rect)

            # Update the horizontal panel spacer
            panel_spacer += const.HAND_PANEL_WIDTH

        # Display the discard pile
        ui_coords['discard'] = cls.__instance._blit_discard_pile(screen,
                                                                 deck,
                                                                 no_of_players)
        # Display the draw pile
        ui_coords['draw'] = cls.__instance._blit_draw_pile(screen,
                                                           no_of_players)

        # End of function
        pygame.display.flip()
        clock.tick(const.TICK_RATE)
        return ui_coords

    @classmethod
    def _blit_player_name_label(cls, screen, player_no, active_player_no,
                                spacer):
        # Draw player name label
        player_label_colour = const.PLAYER_LBL_COLOUR_DEFAULT
        if player_no == active_player_no:
            player_label_colour = const.PLAYER_LBL_COLOUR_ACTIVE

        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.PLAYER_LBL_FONT_SIZE)
        txt_player_no = font.render(f'Player {player_no + 1}',
                                    True, player_label_colour)
        txt_rect = txt_player_no.get_rect()
        txt_rect.x = int(const.PLAYER_LBL_POS_X -
                         (txt_player_no.get_width() / 2) +
                         spacer)
        txt_rect.y = const.PLAYER_LBL_POS_Y
        screen.blit(txt_player_no, txt_rect)

    @classmethod
    def _blit_player_hand_panel(cls, screen, player, spacer):
        art_dir = cls.__instance._art_dir
        card_x = const.HAND_PANEL_PADDING_LEFT + spacer
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
            card_x = const.HAND_PANEL_PADDING_LEFT + spacer
        return hand_rects

    @classmethod
    def _blit_active_card_panel(cls, screen, player, spacer):
        # Draw active card panel
        card_no = player.get_active_card()
        card_filename = const.CARD_ART['placeholder']
        art_dir = cls.__instance._art_dir
        if card_no is not None:
            card_filename = const.CARD_ART[card_no]
        card_img = pygame.image.load(os.path.join(art_dir, card_filename))
        card_img = pygame.transform.scale(card_img,
                                          (const.CARD_WIDTH + 2,
                                           const.CARD_HEIGHT + 2))
        card_rect = card_img.get_rect()
        card_rect.x = const.DRAW_PANEL_CARD_POS_X + spacer
        card_rect.y = const.DRAW_PANEL_CARD_POS_Y
        screen.blit(card_img, card_rect)

        # Draw player score in active card panel
        points = player.get_round_points()
        points_label_colour = const.POINTS_LBL_COLOUR
        font = pygame.font.Font(const.RETRO_COMPUTER,
                                   const.POINTS_LBL_FONT_SIZE)
        txt_points = font.render(f'Round points: {points}',
                                 True, points_label_colour)
        txt_rect = txt_points.get_rect()
        txt_rect.x = const.DRAW_PANEL_POINTS_POS_X + spacer
        txt_rect.y = const.DRAW_PANEL_POINTS_POS_Y
        screen.blit(txt_points, txt_rect)

        return card_rect

    @classmethod
    def _blit_discard_pile(cls, screen, deck, no_of_players):
        # Draw the deck (discard and draw piles)
        card_filename = const.CARD_ART['placeholder']
        art_dir = cls.__instance._art_dir
        card_no = deck.get_discarded_card()
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
        return card_rect

    @classmethod
    def _blit_draw_pile(cls, screen, no_of_players):
        card_filename = const.CARD_ART['card_back']
        art_dir = cls.__instance._art_dir

        card_img = pygame.image.load(os.path.join(art_dir, card_filename))
        card_img = pygame.transform.scale(card_img, (const.CARD_WIDTH + 2,
                                                     const.CARD_HEIGHT + 2))
        card_rect = card_img.get_rect()
        card_rect.x = int(((no_of_players * const.DRAW_PANEL_WIDTH) / 2) +
                          (const.CARD_WIDTH * 1.5))
        card_rect.y = const.DECK_PANEL_Y
        screen.blit(card_img, card_rect)
        return card_rect
