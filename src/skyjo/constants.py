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
WHITE = (255, 255, 255)
SADDLE_BROWN = (139, 69, 19)
MEAT_BROWN = (229, 183, 59)
GREEN = (0, 255, 0)

# Font
MAIN_FONT = 'comicsansms'

# Card art list
CARD_ART_DIR = 'art'
CARD_ART = {
    0: 'card_0.png', 1: 'card_1.png', 2: 'card_2.png', 3: 'card_3.png',
    4: 'card_4.png', 5: 'card_5.png', 6: 'card_6.png', 7: 'card_7.png',
    8: 'card_8.png', 9: 'card_9.png', 10: 'card_10.png', 11: 'card_11.png',
    12: 'card_12.png', -1: 'card_-1.png', -2: 'card_-2.png',
    'card_back': 'card_back.png',  'placeholder': 'card_placeholder.png'
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

# Player label font
PLAYER_LBL_FONT_SIZE = 30
PLAYER_LBL_COLOUR_DEFAULT = BLACK
PLAYER_LBL_COLOUR_ACTIVE = GREEN

# Player label positioning
PLAYER_LBL_POS_X = int(HAND_PANEL_WIDTH / 2)
PLAYER_LBL_POS_Y = 5

###############################################################################
# Constants for the panel showing the player's currently drawn card
###############################################################################

# Panel dimensions
DRAW_PANEL_WIDTH = 310
DRAW_PANEL_HEIGHT = 95

# Panel coordinates
DRAW_PANEL_Y = HAND_PANEL_HEIGHT

# Panel padding
DRAW_PANEL_PADDING_TOP = 20
DRAW_PANEL_PADDING_LEFT = HAND_PANEL_PADDING_LEFT + 5
DRAW_PANEL_POINTS_PADDING_LEFT = 20
DRAW_PANEL_POINTS_PADDING_TOP = 25

# Card position in Panel
DRAW_PANEL_CARD_POS_X = int((DRAW_PANEL_WIDTH / 2) - (CARD_WIDTH / 3))
DRAW_PANEL_CARD_POS_X = DRAW_PANEL_PADDING_LEFT
DRAW_PANEL_CARD_POS_Y = DRAW_PANEL_Y + DRAW_PANEL_PADDING_TOP

# Points position in panel
DRAW_PANEL_POINTS_POS_X = (
    DRAW_PANEL_CARD_POS_X + CARD_WIDTH + DRAW_PANEL_POINTS_PADDING_LEFT
)
DRAW_PANEL_POINTS_POS_Y = DRAW_PANEL_Y + DRAW_PANEL_POINTS_PADDING_TOP

# Points label font
POINTS_LBL_FONT_SIZE = 25
POINTS_LBL_COLOUR = WHITE

###############################################################################
# Constants for the panel showing the draw and discard piles
###############################################################################

# Panel dimensions
DECK_PANEL_HEIGHT = 95

# Panel padding
DECK_PANEL_PADDING_TOP = 100

# Panel coordinates
DECK_PANEL_Y = DRAW_PANEL_HEIGHT + HAND_PANEL_HEIGHT + DECK_PANEL_PADDING_TOP

###############################################################################
# Constants for round summary panel
###############################################################################

# Panel Colour
SCORE_PANEL_COLOUR = MEAT_BROWN

# Panel Text Font
SCORE_PANEL_TITLE_FONT_SIZE = 30
SCORE_PANEL_TEXT_FONT_SIZE = 25
SCORE_PANEL_TEXT_COLOUR = WHITE

# Panel Text strings
SCORE_PANEL_ROUND_TITLE = 'End of Round Points'
SCORE_PANEL_TOTAL_TITLE = 'Total Scores'

# Panel dimensions
SCORE_PANEL_WIDTH = 320
SCORE_PANEL_HEIGHT = 200

# Panel padding
SCORE_PANEL_PADDING_LEFT = 10
SCORE_PANEL_PADDING_TOP = 50
SCORE_PANEL_TEXT_PADDING_LEFT = 20
SCORE_PANEL_TEXT_PADDING_TOP = 50
SCORE_PANEL_ITEM_PADDING_TOP = 20
SCORE_PANEL_TITLE_PADDING_LEFT = 20
SCORE_PANEL_TITLE_PADDING_TOP = 15

# Panel coordinates
SCORE_PANEL_X  = int((SCREEN_WIDTH / 2) - (SCORE_PANEL_WIDTH / 2))
SCORE_PANEL_Y = DRAW_PANEL_HEIGHT + HAND_PANEL_HEIGHT + SCORE_PANEL_PADDING_TOP

# Text coordinates
SCORE_PANEL_TITLE_X = SCORE_PANEL_X + SCORE_PANEL_TITLE_PADDING_LEFT
SCORE_PANEL_TITLE_Y = SCORE_PANEL_Y + SCORE_PANEL_TITLE_PADDING_TOP
SCORE_PANEL_TXT_X = SCORE_PANEL_X + SCORE_PANEL_TEXT_PADDING_LEFT
SCORE_PANEL_TXT_Y = SCORE_PANEL_Y + SCORE_PANEL_TEXT_PADDING_TOP

# Button
SCORE_PANEL_BUTTON_FONT_SIZE = 25
SCORE_PANEL_BUTTON_TEXT = 'Continue'
SCORE_PANEL_BUTTON_COLOUR = WHITE
SCORE_PANEL_BUTTON_TEXT_COLOUR = BLACK
SCORE_PANEL_BUTTON_WIDTH = 85
SCORE_PANEL_BUTTON_HEIGHT = 30
SCORE_PANEL_BUTTON_PADDING_BOTTOM = 45
SCORE_PANEL_BUTTON_X = int(SCORE_PANEL_X + ((SCORE_PANEL_WIDTH / 2) -
                           (SCORE_PANEL_BUTTON_WIDTH / 2)))
SCORE_PANEL_BUTTON_Y = (SCORE_PANEL_Y + SCORE_PANEL_HEIGHT) - SCORE_PANEL_BUTTON_PADDING_BOTTOM

SCORE_PANEL_BUTTON_TEXT_PADDING_LEFT = 5
SCORE_PANEL_BUTTON_TEXT_PADDING_TOP = 5
SCORE_PANEL_BUTTON_TEXT_X = SCORE_PANEL_BUTTON_X + SCORE_PANEL_BUTTON_TEXT_PADDING_LEFT
SCORE_PANEL_BUTTON_TEXT_Y = SCORE_PANEL_BUTTON_Y + SCORE_PANEL_BUTTON_TEXT_PADDING_TOP
