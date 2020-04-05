
"""
A selection of colour options and colour management functions
"""


########################################################################
# RGB colour options
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED_DARK    = (198,   2,   2)
ORANGE_DARK = (198, 100,   2)
YELLOW_DARK = (198, 198,   2)
GREEN_DARK  = (  2, 198,   2)
BLUE_DARK   = (  2, 118, 198)

RED_LIGHT    = (250, 150, 150)
ORANGE_LIGHT = (250, 200, 150)
YELLOW_LIGHT = (250, 250, 150)
GREEN_LIGHT  = (170, 230, 170)
BLUE_LIGHT   = (150, 210, 250)

BLUE_DARK_BBOXX = (  0,  45, 114)  # Pantone 288 C
BLUE_BBOXX      = (  0, 169, 224)  # Pantone 2995 C
PURPLE_BBOXX    = (125,  85, 199)  # Pantone 2665 C
RED_BBOXX       = (228,  93,  80)  # Pantone 485 C
ORANGE_BBOXX    = (255, 158,  27)  # Pantone 1375 C
YELLOW_BBOXX    = (254, 219,   0)  # Pantone 108 C
GREEN_BBOXX     = (  0, 163, 224)  # Pantone 3395 C


########################################################################
def rgb_to_hex(rgb):
    """
    Convert an RGB tuple into a HEX string.

    Parameters
    ==========
    rgb: <tuple>
        A tuple of 3 integers representing RGB888 values.

    Returns
    =======
    A <string> of the hex conversation of the RGB values, with a '#'
    prefix.
    """
    hex_r = str(hex(rgb[0]).replace("0x", ""))
    hex_g = str(hex(rgb[1]).replace("0x", ""))
    hex_b = str(hex(rgb[2]).replace("0x", ""))
    return "#" + hex_r + hex_g + hex_b

def print_colour(name, rgb):
    """ Print the colour name and hex and rgb representations.
    """
    print("{:>20s}  >>  HEX {:<7s}  >>  RGB {};".format(name, rgb_to_hex(rgb), rgb, ))


########################################################################
if __name__ == "__main__":

    print("")
    print_colour("BLUE_BBOXX", BLUE_BBOXX)
    print("")
