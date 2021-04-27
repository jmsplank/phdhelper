import matplotlib.pyplot as plt
from matplotlib import cycler
from matplotlib.colors import LinearSegmentedColormap
from .COLOURS import *

defaults = plt.rcParams.copy()


def override(name=""):
    name = name.split("|")
    if "" in name:
        colours = cycler("color", [red, green, blue, dark, purple])
        plt.rc("axes", grid=True, prop_cycle=colours)
        plt.rc("lines", linewidth=1)
        plt.rc("xtick", direction="out")
        plt.rc("ytick", direction="out")

        cmap = LinearSegmentedColormap.from_list(
            "custom_rgb",
            [tuple(hex_to_rgb(i)) for i in [green, blue, red_intense]],
        )
        plt.register_cmap("custom_rgb", cmap)
        plt.rc("image", cmap="custom_rgb")

def cmaps(name="custom_diverging"):
    if name == 'custom_diverging':
        cmap = LinearSegmentedColormap.from_list(
            "custom_diverging",
            [tuple(hex_to_rgb(i)) for i in [red, mandarin, white, light_blue, blue]]
        )
    plt.register_cmap(name, cmap)
