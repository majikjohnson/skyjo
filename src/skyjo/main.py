import pygame
import os
from skyjo import constants
from skyjo.game import (
    Deck, 
    Player, 
    GameState
)

def gui():
    current_path = os.path.dirname(__file__) # Where your .py file is located
    art_path = os.path.join(current_path, 'art') # The image folder path

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