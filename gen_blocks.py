from typing import Literal


import anvil

Direction4 = Literal["north", "east", "south", "west"]


def torch(facing: Direction4, lit: bool = True):
    return anvil.Block(
        "minecraft", "redstone_wall_torch", {"lit": lit, "facing": facing}
    )


def repeater(
    facing: Direction4, delay: int = 1, powered: bool = False, locked: bool = False
):
    return anvil.Block(
        "minecraft",
        "repeater",
        {"delay": delay, "powered": powered, "facing": facing, "locked": locked},
    )

