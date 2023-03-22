import enum
from typing import Literal

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cycler
from matplotlib.colors import LinearSegmentedColormap

from .COLOURS import (
    blue,
    blue_green,
    dark,
    green,
    green_aquamarine,
    hex_to_rgb,
    light_blue,
    mandarin,
    purple,
    red,
    red_intense,
    red_ultra,
    white,
)

defaults = plt.rcParams.copy()


def override(
    name: str = "",
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

        plt.rc(
            "legend",
            fancybox=False,
            edgecolor="0.95",
            facecolor="0.95",
            framealpha="0.9",
        )

        cmap = LinearSegmentedColormap.from_list(
            "custom_rgb",
            [tuple(hex_to_rgb(i)) for i in [green, blue, red_intense]],
        )
        plt.register_cmap("custom_rgb", cmap)
        plt.rc("image", cmap="custom_rgb")
    if "krgb" in name:
        colours = cycler("color", [dark, red, green, blue, purple])
        plt.rc("axes", prop_cycle=colours)
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
    elif name == "custom_linear":
        cmap = LinearSegmentedColormap.from_list(
            "custom_linear",
            [
                tuple(hex_to_rgb(i))
                for i in [
                    blue,
                    blue_green,
                    green,
                    green_aquamarine,
                    red_ultra,
                    mandarin,
                ]
            ],
        )
    plt.register_cmap(name, cmap)
