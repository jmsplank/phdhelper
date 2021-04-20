red = "#BF245A"
green = "#4BB977"
blue = "#107EA9"
dark = "#020E13"
purple = "#82349C"
red_intense = "#E12346"


def hex_to_rgb(hex):
    r = hex[1:3]
    g = hex[3:5]
    b = hex[5:7]
    rgb = [r, g, b]
    return [float(int(f"0x{i}", 16)) / 255 for i in rgb]
