"""Download every hub listed in the Corvus loader, named after its game.

Fetches the loader, reads its `Repo` and `Games` table, then saves each hub as
"<game name>.lua" in ./hubs (also saves the loader itself as Corvus_loader.lua).
Usage: python download_hubs.py [outdir]
"""
import os
import re
import sys
import urllib.request

LOADER = "https://raw.githubusercontent.com/Cineksvj/Loader/refs/heads/main/Corvus"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read()


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "hubs"
    os.makedirs(out, exist_ok=True)
    loader = get(LOADER)
    with open(os.path.join(out, "Corvus_loader.lua"), "wb") as f:
        f.write(loader)
    text = loader.decode("utf-8", "replace")
    repo = re.search(r'local Repo\s*=\s*"([^"]+)"', text).group(1)
    games = re.findall(
        r'\[(\d+)\]\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*,\s*file\s*=\s*"([^"]+)"', text)
    print(f"repo: {repo}  games: {len(games)}")
    for place_id, name, file in games:
        safe = re.sub(r'[<>:"/\\|?*]', "_", name)
        dest = os.path.join(out, safe + ".lua")
        try:
            data = get(repo + file)
            with open(dest, "wb") as f:
                f.write(data)
            print(f"ok    {name} ({place_id}) -> {dest} [{len(data)} bytes]")
        except Exception as e:
            print(f"FAIL  {name} ({place_id}): {e}")


if __name__ == "__main__":
    main()
