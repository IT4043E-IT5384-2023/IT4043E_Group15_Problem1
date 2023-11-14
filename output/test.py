
import json
path = "output\\profiles.json"
profiles = {"user1": {}}
with open(path, 'r+') as f:
    data = json.load(f)
    data.update(profiles)
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
print(f"[Profile] Scrape users from {0} to {0+1} succesfully!")