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
    current_player_no = game_state.current_player_index()

    hand_panel_spacer = 0
    ui_elements = []

    for player_no, player in enumerate(game_state.get_players()):
        card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
        card_y = constants.HAND_PANEL_PADDING_TOP
        card_coords = []

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

                card_coords.append(rect_card)

                screen.blit(card_img, rect_card)
                card_x += rect_card.width
                card_h = rect_card.height
            card_y += card_h
            card_x = constants.HAND_PANEL_PADDING_LEFT + hand_panel_spacer
        ui_elements.append(card_coords)

        # Draw placeholder for drawn card
        card_img = pygame.image.load(os.path.join(art_path, constants.CARD_ART['placeholder']))
        card_img = pygame.transform.scale(card_img, (constants.CARD_WIDTH + 2, constants.CARD_HEIGHT + 2))
        rect_card = card_img.get_rect()
        rect_card.x = constants.DRAW_PANEL_CARD_POS_X + hand_panel_spacer
        rect_card.y = constants.DRAW_PANEL_CARD_POS_Y
        screen.blit(card_img, rect_card)

        # Draw player name label
        player_label_colour = constants.BLACK
        if player_no == current_player_no:
            player_label_colour = constants.GREEN

        font = pygame.font.SysFont(constants.MAIN_FONT, constants.PLAYER_LBL_FONT_SIZE)
        txt_player_no = font.render(f'Player {player_no + 1}', True, player_label_colour)
        txt_rect = txt_player_no.get_rect()
        txt_rect.x = constants.PLAYER_LBL_POS_X - (txt_player_no.get_width() / 2) + hand_panel_spacer
        txt_rect.y = constants.PLAYER_LBL_POS_Y
        screen.blit(txt_player_no, txt_rect)

        hand_panel_spacer += constants.HAND_PANEL_WIDTH

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
