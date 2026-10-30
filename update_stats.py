import json, re, sys, urllib.request

URL = "https://www.tiktok.com/@aym13144"
req = urllib.request.Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

def get(key):
    m = re.search(r'"%s":(\d+)' % key, html)
    return int(m.group(1)) if m else None

followers = get("followerCount")
likes = get("heartCount") or get("heart")
if followers is None:
    sys.exit("TikTok n'a pas renvoye les chiffres : stats.json reste inchange")

data = json.load(open("stats.json", encoding="utf-8"))
data["abo"] = data["actuel"] = followers
if likes:
    data["likes"] = likes
json.dump(data, open("stats.json", "w", encoding="utf-8"), ensure_ascii=False)
print("OK", followers, likes)
