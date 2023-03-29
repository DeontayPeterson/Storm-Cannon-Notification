from maps import regions
import json

def generate_etags():
    etags = {}
    for region in regions:
        etags[region] = ""
    with open('etags.json', 'w') as f:
        json.dump(etags, f, indent=4)

    print("Generated etags..")



generate_etags()