"""Download every hub file listed in the Corvus loader's Games table.

Each file is saved as "<game name>.lua" in ./hubs (one file per game), ready to
feed to deob.py. Usage: python download_hubs.py [outdir]
"""
import os
import re
import sys
import urllib.request

REPO = "https://raw.githubusercontent.com/Cineksvj/Corvus/refs/heads/main/"

GAMES = {
    11543903102439: ("+1 Stone Skipping", "%2B1%20Stone%20Skipping"),
    113290951185459: ("Anime Dice", "Anime%20Dice"),
    96510569525082: ("Ball VS Ball", "Ball%20VS%20Ball"),
    132767094768856: ("Blue Lock Farm", "Blue%20Lock%20Farm"),
    114326934417838: ("Break and Steal an Egg", "Break%20and%20Steal%20an%20Egg"),
    537413528: ("Build A Boat For Treasure", "Build%20A%20Boat%20For%20Treasure"),
    78490532994307: ("Build An Ant Empire", "Build%20An%20Ant%20Empire"),
    105011592530400: ("Build and Kill Zombies", "Build%20and%20Kill%20Zombies"),
    132239307080610: ("Deep Fishing", "Deep%20Fishing"),
    120656419209274: ("Drill for Eggs", "Drill%20for%20Eggs"),
    107535308163741: ("Huss Valley", "Huss%20Valley"),
    118805555015549: ("+1 Loot To Forge", "%2B1%20Loot%20To%20Forge"),
    88047783411976: ("Open Sea For Animals", "Open%20Sea%20For%20Animals"),
    74629631798007: ("Pets Universe", "Pets%20Universe"),
    124216119978534: ("Ride A Pet", "Ride%20A%20Pet"),
    87740422849523: ("Steal A Car", "Steal%20A%20Car"),
    99679692310083: ("Steal Animal Egg", "Steal%20Animal%20Egg"),
    82081400078378: ("Steal ASMR", "Steal%20ASMR"),
    120475074479690: ("Steal From The Rich", "Steal%20From%20The%20Rich"),
    122245938604556: ("Tongue Escape", "Tongue%20Escape"),
    185655149: ("Welcome to Bloxburg", "Welcome%20to%20Bloxburg"),
    72858262610964: ("Tap Simulator Reborn", "Tap%20Simulator%20Reborn"),
}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "hubs"
    os.makedirs(out, exist_ok=True)
    for place_id, (name, file) in GAMES.items():
        safe = re.sub(r'[<>:"/\\|?*]', "_", name)
        dest = os.path.join(out, safe + ".lua")
        try:
            req = urllib.request.Request(REPO + file, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            with open(dest, "wb") as f:
                f.write(data)
            print(f"ok    {name} ({place_id}) -> {dest} [{len(data)} bytes]")
        except Exception as e:
            print(f"FAIL  {name} ({place_id}): {e}")


if __name__ == "__main__":
    main()
