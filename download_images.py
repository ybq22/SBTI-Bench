import os
import requests

BASE_URL = "https://sbti.unun.dev/image/"
OUT_DIR = os.path.join(os.path.dirname(__file__), "image")
os.makedirs(OUT_DIR, exist_ok=True)

images = [
    "IMSB.png", "BOSS.png", "MUM.png", "FAKE.png", "Dior-s.jpg",
    "DEAD.png", "ZZZZ.png", "GOGO.png", "FUCK.png", "CTRL.png",
    "HHHH.png", "SEXY.png", "OJBK.png", "JOKE-R.jpg", "POOR.png",
    "OH-NO.png", "MONK.png", "SHIT.png", "THAN-K.png", "MALO.png",
    "ATM-er.png", "THIN-K.png", "SOLO.png", "LOVE-R.png", "WOC.png",
    "DRUNK.png", "IMFW.png",
]

for fname in images:
    url = BASE_URL + fname
    dest = os.path.join(OUT_DIR, fname)
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        print(f"OK  {fname} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"ERR {fname}: {e}")
