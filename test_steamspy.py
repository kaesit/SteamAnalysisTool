import requests

def test_steamspy():
    res = requests.get("https://steamspy.com/api.php?request=tag&tag=RPG")
    data = res.json()
    print(f"Got {len(data)} games for RPG")
    # print first game
    first_key = list(data.keys())[0]
    print(data[first_key])

if __name__ == "__main__":
    test_steamspy()
