import requests

USERNAME = "USERNAME"
TOKEN = "TOKEN"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_all(url):
    results = []
    while url:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print("Failed to fetch:", res.status_code)
            break
        results.extend(res.json())
        url = res.links.get("next", {}).get("url")
    return results

def get_usernames(data):
    return [user["login"] for user in data]

# Get who you follow (sorted by most recent)
following_url = f"https://api.github.com/users/{USERNAME}/following?per_page=100"
following_data = get_all(following_url)
following_users = get_usernames(following_data)

# Get your followers
followers_url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
followers_data = get_all(followers_url)
follower_users = get_usernames(followers_data)

# Compare
non_followers = [user for user in following_users if user not in follower_users]

# Print results
print("\nUsers you follow who don't follow you back (most recent first):\n")
current_user = 0
for user in non_followers:
    current_user += 1
    print(f"{current_user}: https://github.com/{user}")
