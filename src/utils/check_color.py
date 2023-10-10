from colour import Color


def check_color(color):
    try:
        color = color.replace(" ", "")
        Color(color)
        return True
    except ValueError:  # The color code was not found
        return False