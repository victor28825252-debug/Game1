"""Fetch only Godot's official Web export template from its large TPZ archive."""
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = "https://godot-releases.nbg1.your-objectstorage.com/4.7.2-stable/Godot_v4.7.2-stable_export_templates.tpz"
DEST = Path.home() / "AppData/Roaming/Godot/export_templates/4.7.2.stable"


class RemoteZip(io.RawIOBase):
    def __init__(self, url):
        self.url = url
        self.pos = 0
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD")) as response:
            self.size = int(response.headers["Content-Length"])
        self.cache_start = -1
        self.cache = b""

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.size + offset
        return self.pos

    def read(self, n=-1):
        if n < 0: n = self.size - self.pos
        if n == 0 or self.pos >= self.size: return b""
        end = min(self.size, self.pos + n)
        if self.cache_start <= self.pos and end <= self.cache_start + len(self.cache):
            result = self.cache[self.pos - self.cache_start:end - self.cache_start]
        else:
            # Small reads are grouped into a cache; template payloads use one range.
            fetch_end = min(self.size, max(end, self.pos + 131072))
            request = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{fetch_end - 1}"})
            with urllib.request.urlopen(request) as response:
                if response.status != 206: raise RuntimeError("Server ignored HTTP Range")
                result_bytes = response.read()
            self.cache_start, self.cache = self.pos, result_bytes
            result = result_bytes[:n]
        self.pos += len(result)
        return result


with zipfile.ZipFile(RemoteZip(URL)) as archive:
    web = [name for name in archive.namelist() if name.endswith(".zip") and "web" in name.lower()]
    print("Available:", web, flush=True)
    target = next((name for name in web if name.endswith("web_nothreads_release.zip")), None)
    if target is None:
        target = next((name for name in web if name.endswith("web_dlink_nothreads_release.zip")), None)
    if target is None: raise RuntimeError("No matching Web export template")
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "version.txt").write_text("4.7.2.stable", encoding="utf-8")
    output = DEST / Path(target).name
    with archive.open(target) as src, output.open("wb") as dst:
        while True:
            block = src.read(1024 * 1024)
            if not block: break
            dst.write(block)
    print("Installed:", output, output.stat().st_size, flush=True)
