import json, re, sys, urllib.request

USER = "aym13144"
req = urllib.request.Request("https://www.tiktok.com/@" + USER, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
if not m:
    sys.exit("Donnees TikTok introuvables : stats.json reste inchange")

scope = json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {})
info = scope.get("webapp.user-detail", {}).get("userInfo", {})
user, stats = info.get("user", {}), info.get("stats", {})
print("Compte lu :", user.get("uniqueId"))
print("Stats brutes :", stats)

if str(user.get("uniqueId", "")).lower() != USER:
    sys.exit("Ce n'est pas le bon compte : stats.json reste inchange")

followers = stats.get("followerCount")
likes = stats.get("heartCount") or stats.get("heart")
if followers is None:
    sys.exit("Abonnes introuvables : stats.json reste inchange")

data = json.load(open("stats.json", encoding="utf-8"))
data["abo"] = data["actuel"] = int(followers)
if likes:
    data["likes"] = int(likes)
json.dump(data, open("stats.json", "w", encoding="utf-8"), ensure_ascii=False)
print("OK", followers, likes)
