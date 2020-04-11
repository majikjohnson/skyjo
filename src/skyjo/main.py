import pygame
from skyjo.game import Deck, Player, GameState, Phase
from skyjo.gui import SkyjoView


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
    score_button_coords = None

    running = True
    update_view = True
    round_summary_view = False
    while running:
        # convenience variables
        current_player = game_state.get_current_player()
        active_player_index = game_state.active_player_index()
        current_phase = game_state.current_phase
        deck = game_state.get_deck()

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
                hand_card_rects = ui_coords['hand'][active_player_index]
                for i, card_rect in enumerate(hand_card_rects):
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        if not current_player.card_visible(i):
                            current_player.reveal_card(i)
                            if current_player.visible_card_count() == 2:
                                game_state.rotate_player()
                                if game_state.active_player_index() == 0:
                                    start_player = game_state.highest_points_player_index()
                                    game_state.set_current_player(start_player)
                                    game_state.current_phase = Phase.draw

        if current_phase == Phase.draw:
            if mouse_clicked:
                mouse_clicked = False
                draw_card_rect = ui_coords['draw']
                discard_card_rect = ui_coords['discard']
                if draw_card_rect.collidepoint(mouse_x, mouse_y):
                    current_player.draw_card(deck)
                    game_state.current_phase = Phase.discard
                    update_view = True
                elif discard_card_rect.collidepoint(mouse_x, mouse_y):
                    current_player.draw_discarded_card(deck)
                    game_state.current_phase = Phase.discard
                    update_view = True

        if current_phase == Phase.discard:
            if mouse_clicked:
                mouse_clicked = False
                card_source = current_player.get_active_card_source()
                if card_source == 'draw_pile':
                    hand_card_rects = ui_coords['hand'][active_player_index]
                    for i, card_rect in enumerate(hand_card_rects):
                        if card_rect.collidepoint(mouse_x, mouse_y):
                            if current_player.card_visible(i):
                                current_player.switch_card(i, deck)
                                game_state.current_phase = Phase.draw
                                game_state.end_turn()
                                update_view = True
                            else:
                                current_player.discard_active_card(deck)
                                current_player.reveal_card(i)
                                game_state.current_phase = Phase.draw
                                game_state.end_turn()
                                update_view = True
                elif card_source == 'discard_pile':
                    hand_card_rects = ui_coords['hand'][active_player_index]
                    for i, card_rect in zip(range(12), hand_card_rects):
                        if current_player.card_visible(i):
                            if card_rect.collidepoint(mouse_x, mouse_y):
                                current_player.switch_card(i, deck)
                                game_state.current_phase = Phase.draw
                                game_state.end_turn()
                                update_view = True

        if current_phase == Phase.round_over:
            round_summary_view = True
            if mouse_clicked:
                mouse_clicked = False
                if score_button_coords.collidepoint(mouse_x, mouse_y):
                    game_state.end_round()
                    round_summary_view = False
                    update_view = True
                    game_state.current_phase = Phase.round_prep

        if game_state.round_over:
            game_state.current_phase = Phase.round_over

        if update_view:
            ui_coords = view.update_display(game_state)
            update_view = False
        if round_summary_view:
            score_button_coords = view.show_round_summary(game_state)
            round_summary_view = False


if __name__ == "__main__":
    controller()
