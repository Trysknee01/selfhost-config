#!/usr/bin/env python3
import json, re, os, hashlib, requests
from pathlib import Path

UPSTREAM_URL = "http://www.xn--sss604efuw.art/jm/jiemi.php?url=http%3A%2F%2Fwww.%E9%A5%AD%E5%A4%AA%E7%A1%AC.art%2Ftv"
REPO = Path(__file__).resolve().parent
LIB = REPO / "lib"
JAR = REPO / "jar"
TVFAN = REPO / "tvfan"

URL_MAP = {
    "https://nos.netease.com/ysf/0075389dca9afadd4614e9713765ff17.txt": "lib/0075389dca9afadd4614e9713765ff17.txt",
    "https://nos.netease.com/ysf/5af5fbe12a88b7c45aa1c21e6551826c.txt": "lib/5af5fbe12a88b7c45aa1c21e6551826c.txt",
    "https://nos.netease.com/ysf/6496356286589c68f52c2f99c0c674c7.txt": "lib/6496356286589c68f52c2f99c0c674c7.txt",
    "https://nos.netease.com/ysf/89370c8ddf36b5e1beb4d71adb921bda.txt": "lib/89370c8ddf36b5e1beb4d71adb921bda.txt",
    "https://nos.netease.com/ysf/d7a21cf34ede56f5c686ecfba5fc7e3f.txt": "lib/d7a21cf34ede56f5c686ecfba5fc7e3f.txt",
    "https://nos.netease.com/ysf/8f55d520f8d70056695740ef151744a7.txt": "lib/8f55d520f8d70056695740ef151744a7.txt",
    "https://nos.netease.com/ysf/c66a4b5356141c49fd45ec51568017b4.txt": "lib/c66a4b5356141c49fd45ec51568017b4.txt",
    "https://nos.netease.com/ysf/3d75a78a0fc7ede372c03598d6d10367.m3u": "lib/3d75a78a0fc7ede372c03598d6d10367.m3u",
    "https://file.icve.com.cn/file_doc/946/41/ECB0A5FBED1D8C4D4E049E95DB9F756F.m3u": "lib/ECB0A5FBED1D8C4D4E049E95DB9F756F.m3u",
    "https://file.icve.com.cn/file_doc/254/346/3FB56B2C49DF92B3252352FBE5CD00F1.m3u": "lib/3FB56B2C49DF92B3252352FBE5CD00F1.m3u",
    "https://file.icve.com.cn/file_doc/220/1003/370FAE41BD301F89BA1FCD6FDB8D5BD6.m3u": "lib/370FAE41BD301F89BA1FCD6FDB8D5BD6.m3u",
    "https://file.icve.com.cn/file_doc/178/700/2C9AF1F98DBC1523826C0CD4DA8D8947.m3u": "lib/2C9AF1F98DBC1523826C0CD4DA8D8947.m3u",
    "https://gh.927223.xyz/https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u": "lib/iptv.m3u",
}

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

def fetch_upstream():
    r = s.get(UPSTREAM_URL, timeout=30)
    r.encoding = "utf-8"
    lines = [l for l in r.text.split("\n") if not l.strip().startswith("//")]
    return json.loads("\n".join(lines))

def dl(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = s.get(url, timeout=60, allow_redirects=True)
    r.raise_for_status()
    dest.write_bytes(r.content)

def replace_urls(o):
    if isinstance(o, str): return URL_MAP.get(o, o)
    if isinstance(o, list): return [replace_urls(i) for i in o]
    if isinstance(o, dict): return {k: replace_urls(v) for k, v in o.items()}
    return o

def clean(config):
    config["wallpaper"] = ""
    config.pop("logo", None)
    branding = ["饭太硬", "fty", "fanty", "饭团"]
    for site in config.get("sites", []):
        n = site.get("name", "")
        for b in branding: n = n.replace(b, "")
        site["name"] = re.sub(r'\s+', ' ', n).strip() or site["name"]
    for live in config.get("lives", []):
        n = live.get("name", "")
        for b in branding: n = n.replace(b, "")
        live["name"] = re.sub(r'\s+', ' ', n).strip() or live["name"]
    return config

print("Fetching...")
config = fetch_upstream()
print(f"Sites: {len(config.get('sites',[]))}")

print("Syncing resources...")
for url, local in URL_MAP.items():
    dest = REPO / local
    if not dest.exists():
        print(f"  {local.split('/')[-1]}")
        dl(url, dest)

spider = config.get("spider", "")
if spider:
    url = spider.split(";")[0]
    md = spider.split(";md5;")[-1] if ";md5;" in spider else ""
    dest = JAR / "fan.txt"
    if dest.exists() and md and hashlib.md5(dest.read_bytes()).hexdigest() == md:
        pass
    else:
        print("  spider")
        dl(url, dest)

config = replace_urls(config)
config = clean(config)

if config.get("spider"):
    f = JAR / "fan.txt"
    if f.exists():
        config["spider"] = f"./jar/fan.txt;md5;{hashlib.md5(f.read_bytes()).hexdigest()}"

for site in config.get("sites", []):
    ext = site.get("ext", {})
    if isinstance(ext, dict) and "Cloud-drive" in ext and "Cloud-drive.txt" in ext["Cloud-drive"]:
        ext["Cloud-drive"] = "./tvfan/Cloud-drive.txt"

(REPO / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK")
