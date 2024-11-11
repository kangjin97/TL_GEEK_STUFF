import requests

# API URL
url = "https://questlog.gg/throne-and-liberty/api/trpc/actionHouse.getAuctionItem?input=%7B%22language%22%3A%22en%22%2C%22regionId%22%3A%22as-f%22%2C%22itemId%22%3A%22sword_aa_t1_nomal_003%22%2C%22traitId%22%3A1670377858%2C%22timespan%22%3A360%7D"

# Step 1: Fetch the JSON data from the API
try:
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    json_data = response.json()  # Parse JSON data
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# Step 2: Extract the list of auction entries
try:
    auction_items = json_data['result']['data']['history']
except KeyError:
    print("Unexpected JSON structure.")
    exit()

# Step 3: Calculate the average of all min prices
min_prices = [item.get('minPrice', 0) for item in auction_items if item.get('minPrice') is not None]

if min_prices:
    average_min_price = sum(min_prices) / len(min_prices)
    print(f"Average Min Price: {average_min_price:.2f}")
else:
    print("No min prices found in the data.")

