from typing import Dict, Tuple, Union

from pathlib import Path
import json

import anvil  # type: ignore


region = anvil.EmptyRegion(0, 0)

stone = anvil.Block("minecraft", "stone")
redstone_wire = anvil.Block("minecraft", "redstone_wire")
air = anvil.Block("minecraft", "air")


for y in range(4):
    for z in range(32):
        for x in range(32):
            region.set_block(stone, x, y, z)

Point = Tuple[int, int, int]


class Blueprint(Dict[Point, anvil.Block]):
    @property
    def dimensions(self) -> Point:
        max_x = max(point[0] for point in self)
        max_y = max(point[1] for point in self)
        max_z = max(point[2] for point in self)
        return (max_x + 1, max_y + 1, max_z + 1)

    def place(self, region: anvil.Region, offset: Point = (0, 0, 0)) -> None:
        for point, block in self.items():
            region.set_block(
                block, point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]
            )

    @classmethod
    def load(cls, path: Union[Path, str]) -> "Blueprint":
        self = cls()

        with open(path) as f:
            blueprint = json.load(f)

        for point_str, block in blueprint.items():
            point = [int(p) for i, p in enumerate(point_str.split(","))]
            self[(point[0], point[1], point[2])] = anvil.Block(
                "minecraft", block["block"], block["attrs"]
            )

        return self


byte_cell = Blueprint.load("blueprints/byte_cell.json")
full_adder = Blueprint.load("blueprints/full_adder.json")

# Stack 2 byte memory cells on top of each other

byte_cell.place(region, (5, 10, 1))
byte_cell.place(region, (5, 15, 1))

# Stack 8 full adders to form a one byte adder

for i in range(8):
    full_adder.place(
        region, (byte_cell.dimensions[0] + 6, 14, i * full_adder.dimensions[2])
    )

# Remove the extra carry torches from the adder


region.set_block(
    air, byte_cell.dimensions[0] + 6 + 6, 15, 1 + 7 * full_adder.dimensions[2]
)
region.set_block(
    air, byte_cell.dimensions[0] + 6 + 7, 16, 1 + 7 * full_adder.dimensions[2]
)

# Connect to together

connector = Blueprint()

connector[(1, 0, 0)] = stone
connector[(1, 1, 0)] = redstone_wire
connector[(2, 1, 0)] = stone
connector[(2, 2, 0)] = redstone_wire
connector[(3, 2, 0)] = stone
connector[(3, 3, 0)] = redstone_wire

connector[(1, 5, 0)] = stone
connector[(1, 6, 0)] = redstone_wire
connector[(2, 5, 0)] = stone
connector[(2, 6, 0)] = redstone_wire
connector[(3, 5, 0)] = stone
connector[(3, 6, 0)] = redstone_wire

connector[(0, 2, 2)] = stone
connector[(0, 3, 2)] = redstone_wire
connector[(1, 2, 2)] = stone
connector[(1, 3, 2)] = redstone_wire
connector[(2, 2, 2)] = stone
connector[(2, 3, 2)] = redstone_wire
connector[(3, 2, 2)] = stone
connector[(3, 3, 2)] = redstone_wire

connector[(1, 7, 1)] = stone
connector[(1, 8, 1)] = redstone_wire
connector[(1, 7, 2)] = stone
connector[(1, 8, 2)] = redstone_wire
connector[(2, 6, 2)] = stone
connector[(2, 7, 2)] = redstone_wire
connector[(3, 5, 2)] = stone
connector[(3, 6, 2)] = redstone_wire

for i in range(4):
    connector.place(region, (byte_cell.dimensions[0] + 4, 12, 1 + i * 4))


region.save("test.mca")
