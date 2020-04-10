# Skyjo main game algorithm


## Phases

1. round_prep
2. draw
3. discard
4. game_over

## Model
```
skyjo_model = {
  hand,
  active,
  discard,
  draw
}
```

## Controller logic

```
## For each iteration
  # get current_player
  # get current_phase
  # get click_coordinates

## current_phase == round_prep
  # if click_coordinates within bounds of current_player hidden cards
    # reveal hidden card
    # if current_player has two visible cards on their board
      # move GameState.current_player to next player
    # if all players have two cards visible
      # move GameState.mode to card draw mode

## current_phase == draw
  # if click_coordinates within bounds of the draw pile or discard pile
    # if draw pile chosen
      # draw card from draw draw pile
      # add drawn card to player's active card area
      # move GameState.mode to replace_or_discard
    # if discard pile chosen
      # remove card from discard pile
      # add card to players' active card area
      # move GameState.mode to replace_or_discard


## current_phase = discard
  # if click_coordinates within bounds of the current_player visible cards
    # replace clicked card with active card
    # move clicked card to the top of the discard pile
    # clear active card
    # move GameState.current_player to next player
    # call GameState.end_turn
  # if clicked_coordinates within bounds of the current_player hidden cards
    # move active card to the top of the discard file
    # clear active card
    # set the clicked card to visible
    # move GameState.current_player to next player
    # call GameState.end_turn

## if game_over is True
  # move GameState.mode to game over mode


## Update display

```
