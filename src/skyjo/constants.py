'''Contains constants used to draw elements of the UI'''
###############################################################################
# Main game constants
###############################################################################

TICK_RATE = 60

# Main screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colour Tuples
BLACK = (0, 0, 0)
SADDLE_BROWN = (139, 69, 19)
GREEN = (0, 255, 0)

# Font
MAIN_FONT = 'comicsansms'

# Card art list
CARD_ART_DIR = 'art'
CARD_ART = {
    0: 'card_0.png',
    1: 'card_1.png',
    2: 'card_2.png',
    3: 'card_3.png',
    4: 'card_4.png',
    5: 'card_5.png',
    6: 'card_6.png',
    7: 'card_7.png',
    8: 'card_8.png',
    9: 'card_9.png',
    10: 'card_10.png',
    11: 'card_11.png',
    12: 'card_12.png',
    -1: 'card_-1.png',
    -2: 'card_-2.png',
    'card_back': 'card_back.png',
    'placeholder': 'card_placeholder.png'
}

###############################################################################
# Constants for the players hand panel (panel that displays the player's cards)
###############################################################################

# Panel dimensions
HAND_PANEL_WIDTH = 310
HAND_PANEL_HEIGHT = 320

# Panel padding
HAND_PANEL_PADDING_LEFT = 50
HAND_PANEL_PADDING_TOP = 50

# Padding between cards
CARD_PADDING = 10

# Sets size of the cards
CARD_WIDTH = 50
CARD_HEIGHT = 75

# Player label font size
PLAYER_LBL_FONT_SIZE = 30

# Player lable positioning
PLAYER_LBL_POS_X = int(HAND_PANEL_WIDTH / 2)
PLAYER_LBL_POS_Y = 5

###############################################################################
# Constants for the panel showing the player's currently drawn card
###############################################################################

# Panel dimensions
DRAW_PANEL_WIDTH = 310
DRAW_PANEL_HEIGHT = 95

# Panel coordinates
DRAW_PANEL_X = 0
DRAW_PANEL_Y = HAND_PANEL_HEIGHT

# Panel padding
DRAW_PANEL_PADDING_TOP = 20

# Card position in Panel
DRAW_PANEL_CARD_POS_X = int((DRAW_PANEL_WIDTH / 2) - (CARD_WIDTH / 3))
DRAW_PANEL_CARD_POS_Y = DRAW_PANEL_Y + DRAW_PANEL_PADDING_TOP

###############################################################################
# Constants for the panel showing the draw and discard piles
###############################################################################

# Panel dimensions
DECK_PANEL_HEIGHT = 95

# Panel padding
DECK_PANEL_PADDING_TOP = 100

# Panel coordinates
DECK_PANEL_Y = DRAW_PANEL_HEIGHT + HAND_PANEL_HEIGHT + DECK_PANEL_PADDING_TOP
