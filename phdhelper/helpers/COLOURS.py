red = "#BF245A"
green = "#4BB977"
blue = "#107EA9"
dark = "#020E13"
purple = "#82349C"
red_intense = "#E12346"
mandarin = "#E67737"
light_blue = "#C3F4FE"
white = "#FFFFFF"
green_deep = "#4A9669"
green_aquamarine = "#6CE09A"
red_ultra = "#EB6F86"
blue_green = "#2790B9"


def hex_to_rgb(hex):
    r = hex[1:3]
    g = hex[3:5]
    b = hex[5:7]
    rgb = [r, g, b]
    return [float(int(f"0x{i}", 16)) / 255 for i in rgb]
