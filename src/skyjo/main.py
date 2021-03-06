import pygame
from skyjo.game import Deck, Player, GameState, Phase
from skyjo.gui import SkyjoView

def controller():
    game_state = GameState()
    view = SkyjoView()

    ui_coords = {}
    score_button_coords = None
    game_over_button_coords = {}
    player_select_coords = {}

    running = True
    player_select_view = True
    update_view = False
    round_summary_view = False
    score_view = False
    game_over_view = False
    while running:
        # convenience variables
        current_phase = game_state.current_phase

        if current_phase != Phase.player_select:
            current_player = game_state.get_current_player()
            active_player_index = game_state.active_player_index()
            deck = game_state.get_deck()


        # Handle input events
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_clicked = True
            

        if current_phase == Phase.player_select:
            if mouse_clicked:
                mouse_clicked = False
                no_of_players = 0
                if player_select_coords['2'].collidepoint(mouse_x, mouse_y):
                    no_of_players = 2
                elif player_select_coords['3'].collidepoint(mouse_x, mouse_y):
                    no_of_players = 3
                elif player_select_coords['4'].collidepoint(mouse_x, mouse_y):
                    no_of_players = 4
                if no_of_players > 0:
                    game_state.init_game(no_of_players)
                
        if current_phase == Phase.round_prep:
            update_view = True
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
                    game_state.current_phase = Phase.show_scores

        if current_phase == Phase.show_scores:
            score_view = True
            if mouse_clicked:
                mouse_clicked = False
                if score_button_coords.collidepoint(mouse_x, mouse_y):
                    score_view = False
                    if not game_state.is_game_over():
                        update_view = True
                        game_state.current_phase = Phase.round_prep
                    else:
                        game_state.current_phase = Phase.game_over

        if current_phase == Phase.game_over:
            game_over_view = True
            if mouse_clicked:
                mouse_clicked = False
                restart_button = game_over_button_coords['restart']
                quit_button = game_over_button_coords['quit']
                if quit_button.collidepoint(mouse_x, mouse_y):
                    running = False
                elif restart_button.collidepoint(mouse_x, mouse_y):
                    game_state.init_game(game_state.player_count)
                    game_over_view = False
            
        if game_state.round_over:
            game_state.current_phase = Phase.round_over

        if player_select_view:
            player_select_coords = view.show_player_select_view(game_state)
            player_select_view = False
        if update_view:
            ui_coords = view.update_display(game_state)
            update_view = False
        if round_summary_view:
            score_button_coords = view.show_scores(game_state, type='round')
            round_summary_view = False
        if score_view:
            score_button_coords = view.show_scores(game_state, type='total')
            score_view = False
        if game_over_view:
            game_over_button_coords = view.show_game_over(game_state)
            game_over_view = False


if __name__ == "__main__":
    controller()
