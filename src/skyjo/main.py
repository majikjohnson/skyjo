import pygame
from skyjo import constants
from skyjo.game import Deck, Player, GameState, Phase
from skyjo.gui import SkyjoView
from enum import Enum

def init_game(number_of_players):
    ''' Returns a GameState object configured with initial settings '''
    deck = Deck()
    players = [Player() for _ in range(number_of_players)]
    deck.deal_hand(players)
    return GameState(players, deck)

def controller():
    number_of_players = 4
    game_state = init_game(number_of_players)
    view = SkyjoView()

    ui_coords = {}

    running = True
    update_view = True
    while running:
        # convenience variables
        current_player = game_state.get_current_player()
        current_player_index = game_state.current_player_index()
        current_phase = game_state.current_phase

        # Handle input events
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_clicked = True
                update_view = True

        if current_phase == Phase.round_prep:
            if mouse_clicked:
                mouse_clicked = False
                hand_card_rects = ui_coords['hand'][current_player_index]
                for i, card in enumerate(hand_card_rects):
                    if card.collidepoint(mouse_x, mouse_y):
                        if not current_player.card_visible(i):
                            current_player.reveal_card(i)
                            if current_player.visible_card_count() == 2:
                                game_state.rotate_player()
                                if game_state.current_player_index() == 0:
                                    game_state.current_phase = Phase.draw

        if update_view:
            ui_coords = view.update_display(game_state)
            update_view = False

if __name__ == "__main__":
    controller()
