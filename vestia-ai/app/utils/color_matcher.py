import colorsys


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsv(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hsv(r, g, b)


def get_hue(hex_color):
    rgb = hex_to_rgb(hex_color)
    hsv = rgb_to_hsv(rgb)
    return hsv[0] * 360  # degrees


def is_neutral(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return abs(r - g) < 15 and abs(g - b) < 15


def color_distance(c1, c2):
    h1 = get_hue(c1)
    h2 = get_hue(c2)
    return min(abs(h1 - h2), 360 - abs(h1 - h2))


def score_color_pair(c1, c2):
    """
    Returns score between 0–1
    """

    if is_neutral(c1) or is_neutral(c2):
        return 0.9  # neutrals match almost everything

    dist = color_distance(c1, c2)

    if dist < 30:
        return 0.8  # similar colors
    elif 150 < dist < 210:
        return 1.0  # complementary colors
    elif dist < 90:
        return 0.6  # okay combo
    else:
        return 0.4  # poor match


def score_palette(palette1, palette2):
    """
    Compare two color palettes
    """

    if not palette1 or not palette2:
        return 0.5

    scores = []

    for c1 in palette1:
        for c2 in palette2:
            scores.append(score_color_pair(c1, c2))

    return sum(scores) / len(scores)