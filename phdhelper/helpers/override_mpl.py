import enum
import matplotlib.pyplot as plt
from matplotlib import cycler
from matplotlib.colors import LinearSegmentedColormap
from .COLOURS import *
import matplotlib
from typing import Literal

defaults = plt.rcParams.copy()


def override(
    name: Literal["", "pub", "book_gs"] = "",
    font: Literal["eb garamond", "inter"] = "inter",
    serif: bool = True,
):
    name = name.split("|")
    if "" in name:
        colours = cycler("color", [red, green, blue, dark, purple])
        plt.rc("axes", grid=True, prop_cycle=colours, xmargin=0)
        plt.rc("lines", linewidth=1)
        plt.rc("xtick", direction="in", top=True, bottom=True)
        plt.rc("xtick.minor", visible=True)
        plt.rc("ytick", direction="in", left=True, right=True)
        plt.rc("ytick.minor", visible=True)
        matplotlib.rc("font", family=font)

        plt.rc("legend", fancybox=False, edgecolor="0.2", facecolor="0.2")

        cmap = LinearSegmentedColormap.from_list(
            "custom_rgb",
            [tuple(hex_to_rgb(i)) for i in [green, blue, red_intense]],
        )
        plt.register_cmap("custom_rgb", cmap)
        plt.rc("image", cmap="custom_rgb")
    if "pub" in name:
        override()
        matplotlib.rc("text", usetex=True)
        matplotlib.rc(
            "text.latex",
            preamble=r"""\usepackage[T1]{fontenc}
\usepackage{bm}"""
            + (
                r"""
\usepackage{ebgaramond}"""
                if serif
                else r"""
\usepackage{arev}"""
            ),
        )
        matplotlib.rcParams.update({"font.size": 11})
    if "book_gs" in name:
        colours = cycler(color=["k"] * 4 + ["#777777"] * 4) + cycler(
            linestyle=["-", "--", ":", "-."] * 2
        )
        plt.rc("axes", grid=False, prop_cycle=colours)
        plt.rc("lines", linewidth=2)
        plt.rc("xtick", direction="in", labelbottom=False, labeltop=False)
        plt.rc("ytick", direction="in", labelleft=False, labelright=False)

        cmap = LinearSegmentedColormap.from_list(
            "custom_rgb",
            [tuple(hex_to_rgb(i)) for i in ["#FFFFFF", "#000000"]],
        )
        plt.register_cmap("book_gs", cmap)
        plt.rc("image", cmap="book_gs")


def cmaps(name="custom_diverging"):
    if name == "custom_diverging":
        cmap = LinearSegmentedColormap.from_list(
            "custom_diverging",
            [tuple(hex_to_rgb(i)) for i in [red, mandarin, white, light_blue, blue]],
        )
    plt.register_cmap(name, cmap)
