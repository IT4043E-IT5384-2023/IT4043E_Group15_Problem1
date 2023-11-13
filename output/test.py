import json

with open("output\\profiles.json", 'r+') as f:
    profiles = json.load(f)
    x = {
        "user3": {}
    }
    profiles.update(x)
    f.seek(0)
    json.dump(profiles, f, ensure_ascii=False, indent=4)
