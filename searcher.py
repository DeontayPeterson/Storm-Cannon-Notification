import requests
import json
import time
#from maps import regions 



ep_shard1 = 'https://war-service-live.foxholeservices.com/api'
ep_shard2 = 'https://war-service-live-2.foxholeservices.com/api'
ep_shard3 = 'https://war-service-live-3.foxholeservices.com/api'


regions = ["TheFingersHex", "TempestIslandHex", "GreatMarchHex", "MarbanHollow", "ViperPitHex", "BasinSionnachHex", "DeadLandsHex", "HeartlandsHex", "EndlessShoreHex", "WestgateHex", "OarbreakerHex", "AcrithiaHex", "MooringCountyHex", "WeatheredExpanseHex", "MorgensCrossingHex", "LochMorHex", "StonecradleHex", "AllodsBightHex", "KalokaiHex", "RedRiverHex", "OriginHex", "HowlCountyHex", "SpeakingWoodsHex", "ShackledChasmHex", "TerminusHex", "LinnMercyHex", "ClansheadValleyHex", "NevishLineHex", "GodcroftsHex", "CallumsCapeHex", "FishermansRowHex", "ReachingTrailHex", "UmbralWildwoodHex", "CallahansPassageHex", "AshFieldsHex", "DrownedValeHex", "FarranacCoastHex"]



def grab_from_json(file_path):

    with open(file_path, 'r') as f:
        temp = json.load(f)

    return temp


def make_call():
    to_return = []
    location_return = []
    for region in regions:
        url = f"https://war-service-live.foxholeservices.com/api/worldconquest/maps/{region}/dynamic/public"
        etags = grab_from_json('etags.json')

        if not etags[region]:
            print(url)
            response = requests.get(url=url)
        elif etags[region]:
            print(url)

            headers = {"If-None-Match": etags[region]}
            response = requests.get(url=url, headers=headers)


        if response.status_code == 200:

            map_info = response.json()
            old_map_info = grab_from_json(f'map_data/{region}.json')


            old_map_items = old_map_info['mapItems']
            new_map_items = map_info['mapItems']

            for item in new_map_items:
                if item not in old_map_items:
                    print(f"New Event: {item}")
                    if item['iconType'] == 59:
                        print(item)
                        to_return.append(item)
                        location_return.append(region)
                    if item['iconType'] == 60:
                        print(item)
                        to_return.append(item)
                        location_return.append(region)



            #Need to check "map_info against map_data/{region}" before re-writing
            with open(f'map_data/{region}.json', 'w')as f:
                json.dump(map_info, f, indent=4)

            new_etag = response.headers['ETag']

            ###############################
            print(f"ETag updated in: '{region}' ETag was: '{etags[region]}' ETag is now: '{new_etag}'")
            ###############################

            current_tags = grab_from_json('etags.json')
            current_tags[region] = new_etag

            with open('etags.json', 'w')as f:
                json.dump(current_tags, f, indent=4)

        elif response.status_code == 304:
            pass

        elif response.status_code == 500:
            pass
    print("********NEXT IN 5 *********")

    return (to_return, location_return)
    

def start_searching():
    while True:
        make_call()

        time.sleep(5)



if __name__ == "__main__":
    start_searching()