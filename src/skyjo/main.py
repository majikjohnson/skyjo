import pygame
import os
from skyjo import constants
from skyjo.game import (
    Deck, 
    Player, 
    GameState
)

def draw(screen, game_state):
    ''' Draws the palying board on the screen '''
    current_path = os.path.dirname(__file__) # Where your .py file is located
    art_path = os.path.join(current_path, 'art') # The image folder path
    screen.fill(constants.SADDLE_BROWN)
    no_of_players = len(game_state.get_players())
    current_player_no = game_state.current_player_index()
    deck = game_state.get_deck()

    hand_panel_spacer = 0
    player_hand_cards = []
    player_draw_cards = []

    for player_no, player in enumerate(game_state.get_players()):
        card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
        card_y = constants.HAND_PANEL_PADDING_TOP
        player_hand_rects = []

        card_itr = 0

        for row in range(3):
            for col in range(4):
                card_filename = constants.CARD_ART['card_back']
                current_card = player.get_card(card_itr)
                if player.card_visible(card_itr):
                    card_filename = constants.CARD_ART[current_card]
                card_itr += 1

                card_img = pygame.image.load(os.path.join(art_path, card_filename))
                card_img = pygame.transform.scale(card_img, (constants.CARD_WIDTH, constants.CARD_HEIGHT))
                rect_card = card_img.get_rect()
                rect_card.x = card_x + (constants.CARD_PADDING * col)
                rect_card.y = card_y + (constants.CARD_PADDING * row)

                player_hand_rects.append(rect_card)

                screen.blit(card_img, rect_card)
                card_x += rect_card.width
                card_h = rect_card.height
            card_y += card_h
            card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
        player_hand_cards.append(player_hand_rects)

        # Draw placeholder for drawn card
        card_img = pygame.image.load(os.path.join(art_path, constants.CARD_ART['placeholder']))
        card_img = pygame.transform.scale(card_img, (constants.CARD_WIDTH + 2, constants.CARD_HEIGHT + 2))
        rect_card = card_img.get_rect()
        rect_card.x = constants.DRAW_PANEL_CARD_POS_X + hand_panel_spacer
        rect_card.y = constants.DRAW_PANEL_CARD_POS_Y
        screen.blit(card_img, rect_card)
        player_draw_cards.append(rect_card)

        # Draw player name label
        player_label_colour = constants.BLACK
        if player_no == current_player_no:
            player_label_colour = constants.GREEN

        font = pygame.font.SysFont(constants.MAIN_FONT, constants.PLAYER_LBL_FONT_SIZE)
        txt_player_no = font.render(f'Player {player_no + 1}', True, player_label_colour)
        txt_rect = txt_player_no.get_rect()
        txt_rect.x = int(constants.PLAYER_LBL_POS_X - (txt_player_no.get_width() / 2) + hand_panel_spacer)
        txt_rect.y = constants.PLAYER_LBL_POS_Y
        screen.blit(txt_player_no, txt_rect)

        hand_panel_spacer += constants.HAND_PANEL_WIDTH

    # Draw the deck (discard and draw piles)
    discarded_card_no = deck.get_discarded_card()
    discarded_card_filename = constants.CARD_ART['placeholder']
    if discarded_card_no is not None:
        discarded_card_filename = constants.CARD_ART[discarded_card_no]
    discarded_card_img = pygame.image.load(os.path.join(art_path, discarded_card_filename))
    discarded_card_img = pygame.transform.scale(discarded_card_img, (constants.CARD_WIDTH + 2, constants.CARD_HEIGHT + 2))
    discarded_card_rect = discarded_card_img.get_rect()
    discarded_card_rect.x = int(((no_of_players * constants.DRAW_PANEL_WIDTH) / 2) - (constants.CARD_WIDTH * 1.5))
    discarded_card_rect.y = constants.DECK_PANEL_Y
    screen.blit(discarded_card_img, discarded_card_rect)

    draw_pile_card_filename = constants.CARD_ART['card_back']
    draw_pile_card_img = pygame.image.load(os.path.join(art_path, draw_pile_card_filename))
    draw_pile_card_img = pygame.transform.scale(draw_pile_card_img, (constants.CARD_WIDTH + 2, constants.CARD_HEIGHT + 2))
    draw_pile_card_rect = draw_pile_card_img.get_rect()
    draw_pile_card_rect.x = int(((no_of_players * constants.DRAW_PANEL_WIDTH) / 2) + (constants.CARD_WIDTH * 1.5))
    draw_pile_card_rect.y = constants.DECK_PANEL_Y
    screen.blit(draw_pile_card_img, draw_pile_card_rect)

    ui_elements = {
        'player_hand_cards': player_hand_cards,
        'player_draw_cards': player_draw_cards,
        'discard_pile': discarded_card_rect,
        'draw_pile': draw_pile_card_rect
    }

    return ui_elements            

def gui():
    ''' Main game entry point.  Sets up game. '''
    deck = Deck()
    players = []
    for i in range(4):
        players.append(Player())
    deck.deal_hand(players)
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

        ui_elements = draw(screen, game_state)

        player_hand_cards = ui_elements['player_hand_cards']
               
        if mouse_clicked:
            for i, card in enumerate(player_hand_cards[current_player_index]):
                if card.collidepoint(mouse_x, mouse_y):
                    if not current_player.card_visible(i):
                        current_player.reveal_card(i)
                        game_state.end_turn()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    gui()
