import anvil
from nbt import nbt
import json

path = "server/world/region/r.-1.-1.mca"


region = anvil.Region.from_file(path)


MARKER = "diamond_block"
BLACKLIST = {"air", "bedrock", "dirt", "grass_block"}

contents = {}
endpoints = []

for rx in range(-1, -8, -1):
    for rz in range(-1, -8, -1):

        chunk = anvil.Chunk.from_region(region, rx, rz)

        for y in range(256):
            for cx in range(16):
                for cz in range(16):
                    block = chunk.get_block(cx, y, cz)

                    x = rx * 16 + cx
                    z = rz * 16 + cz

                    if block.id == MARKER:
                        endpoints.append((x, y, z))

                    if block.id not in BLACKLIST:
                        contents[(x, y, z)] = block

assert len(endpoints) == 2

# Select only the blocks between endpoints

intervals = [sorted((endpoints[0][i], endpoints[1][i])) for i in range(3)]

selected = {
    point: block
    for point, block in contents.items()
    if all(intervals[i][0] <= point[i] <= intervals[i][1] for i in range(3))
    and block.id != MARKER
}


# Normalize to start from the origo
# Do not user intervals as the might contain empty space around the selected blocks

mins = [min(p[i] for p in selected) for i in range(3)]
selected = {
    tuple(point[i] - mins[i] for i in range(3)): block
    for point, block in selected.items()
}


# Export to json

print(
    json.dumps(
        {
            ",".join([str(p) for p in point]): {
                "block": block.id,
                "attrs": {k: v.value for k, v in block.properties.items()},
            }
            for point, block in selected.items()
        }
    )
)
