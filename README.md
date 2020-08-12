# Minecraft Redstone CPU generator

Set of tools to generate Redstone CPUs in modular and scalable manner.
The tools and an actual CPU are developed together.

The main idea is to create a set of blueprints that can be combined together into larger components.

## Setup

A minecraft server (like [Spigot](https://www.spigotmc.org/)) should be placed in the `server/` directory. Usually you will also add [WorldEdit](https://dev.bukkit.org/projects/worldedit/files) plugin for the server.

I would suggest also getting redstone-related texture improvements for your Minecraft client from [VanillaTweaks](https://vanillatweaks.net/picker/resource-packs/).

## Workflow

`read.py` can be used to read new blueprints from the Minecraft world.

### Generating new version

```
black worldgen.py && mypy worldgen.py
python worldgen.py
```

### Starting the server with the new version

```bash
cp ../test.mca server/world/region/r.0.0.mca
java -Xms2G -Xmx2G -jar spigot-1.16.1.jar nogui
```