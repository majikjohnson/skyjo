'''Contains constants used to draw elements of the UI'''
###############################################################################
# Main game constants
###############################################################################

# Main screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colour Tuples
BLACK = (0, 0, 0)
SADDLE_BROWN = (139, 69, 19)

# Card art list
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
    'card_back': 'card_back.png'
}

################################################################################
# Constants for the player's hand panel (panel that displays the player's cards)
################################################################################

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