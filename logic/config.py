from infra import create_enum

SUITS_LIST, SUITS = create_enum(
    (('S', 's'),  # Spade
     ('D', 'd'),  # Diamond
     ('H', 'h'),  # Heart
     ('C', 'c'),  # Club
     )
)

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

# POSITIONS_LIST, POSITIONS = create_enum(
#     (('SB', 0),  # Small blind
#      ('BB', 1),  # Big blind
#      ('CO', 2),  # Cut-off
#      ('BTN', 3),  # Button
#      )
# )
POSITIONS_LIST, POSITIONS = create_enum(
    (('UTG', 'UTG'),  # Under the gun
     ('BTN', 'BTN'),  # Button
     ('SB', 'SB'),  # Small blind
     ('BB', 'BB'),  # Big blind
     )
)

# OCOC1 - will it work for less than 4 players?
POS_SB_VS_DEALER = 2
POS_BB_VS_DEALER = 2
POS_UTG_VS_DEALER = 3
