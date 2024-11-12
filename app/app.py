import requests
import pandas as pd

# Function to fetch auction house data from the API using dynamic region ID
def fetch_auction_house_data(region_id):
    url = f"https://questlog.gg/throne-and-liberty/api/trpc/actionHouse.getAuctionHouse?input=%7B%22language%22%3A%22en%22%2C%22regionId%22%3A%22{region_id}%22%7D"
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data['result']['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    
# Feature 1: Generate Auction House Summary
def generate_auction_house_summary(region_id):
    items = fetch_auction_house_data(region_id)
    if not items:
        print("No data fetched from API.")
        return

    # Prepare data for Excel with 'Trait ID' included
    data_list = []
    for item in items:
        item_id = item.get('id')
        name = item.get('name')
        grade = item.get('grade')
        main_category = item.get('mainCategory')
        sub_category = item.get('subCategory')
        sub_sub_category = item.get('subSubCategory', '')  # Get subSubCategory, leave blank if not present
        min_price = item.get('minPrice', 0)
        in_stock = item.get('inStock', 0)
        trait_ids_map = item.get('traitIds', {})

        # Collect trait items info
        trait_items = item.get('traitItems', [])
        for trait in trait_items:
            trait_id = trait.get('traitId')
            trait_text = trait_ids_map.get(str(trait_id), "Unknown Trait")
            trait_min_price = trait.get('minPrice', 0)
            trait_in_stock = trait.get('inStock', 0)
            
            # Append data including 'Trait ID'
            data_list.append({
                "ID": item_id,
                "Name": name,
                "Grade": grade,
                "Main Category": main_category,
                "Sub Category": sub_category,
                "Sub Sub Category": sub_sub_category,  # Include subSubCategory here
                "Min Price": min_price,
                "In Stock": in_stock,
                "Trait ID": trait_id,
                "Trait": trait_text,
                "Trait Min Price": trait_min_price,
                "Trait In Stock": trait_in_stock
            })

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(data_list)
    output_file = f"auction_house_summary_{region_id}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data successfully written to {output_file}")

# Feature 2: Generate Trait Extract Summary based on Sub Sub Category
def generate_trait_extract_summary(region_id, sub_sub_category):
    items = fetch_auction_house_data(region_id)
    if not items:
        print("No data fetched from API.")
        return

    # Filter items by Main Category "traitextract" and Sub Sub Category
    filtered_items = [item for item in items if item.get('mainCategory') == 'traitextract' and item.get('subSubCategory') == sub_sub_category]
    if not filtered_items:
        print(f"No items found for Sub Sub Category: {sub_sub_category}")
        return

    # Prepare trait IDs and min prices in a dictionary
    trait_ids_map = {}
    for item in filtered_items:
        item_id = item.get('id')
        name = item.get('name')
        grade = item.get('grade')
        min_price = item.get('minPrice', 0)
        trait_ids = item.get('traitIds', {})
        
        # Collect trait items info
        trait_items = item.get('traitItems', [])
        for trait in trait_items:
            trait_id = trait.get('traitId')
            trait_text = trait_ids.get(str(trait_id), "Unknown Trait")
            trait_min_price = trait.get('minPrice', 0)
            trait_in_stock = trait.get('inStock', 0)
            
            if trait_id not in trait_ids_map:
                trait_ids_map[trait_id] = {
                    "trait_name": trait_text,
                    "records": {}
                }

            # Add record for this trait ID with the item's min price
            trait_ids_map[trait_id]["records"][name] = trait_min_price

    # Sort items by grade (higher grades first)
    sorted_items = sorted(filtered_items, key=lambda x: x.get('grade', 0), reverse=True)

    # Prepare data for the Excel sheet
    data_list = []
    trait_ids = list(trait_ids_map.keys())  # List of all trait IDs
    headers = ["Trait ID", "Trait Name"] + [item.get('name') for item in sorted_items]  # First two columns for Trait ID and Name

    for trait_id in trait_ids:
        trait_info = trait_ids_map[trait_id]
        row = [trait_id, trait_info["trait_name"]]  # Trait ID and Name

        # For each record, append the min price for this trait_id
        for item in sorted_items:
            name = item.get('name')
            min_price = trait_info["records"].get(name, "")
            row.append(min_price)

        data_list.append(row)

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(data_list, columns=headers)
    output_file = f"trait_extract_summary_{region_id}_{sub_sub_category}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Trait Extract data written to {output_file}")

# Function to prompt the user to select a region
def select_region():
    regions = {
        "1": ("North America West", "naw-f"),
        "2": ("North America East", "nae-f"),
        "3": ("Europe", "eu-f"),
        "4": ("South America", "sa-f"),
        "5": ("Asia Pacific", "as-f")
    }

    print("\nSelect a region:")
    for key, (name, _) in regions.items():
        print(f"{key}. {name}")

    while True:
        choice = input("Enter your choice (1-5): ")
        if choice in regions:
            region_name, region_id = regions[choice]
            print(f"Selected Region: {region_name} ({region_id})")
            return region_id
        else:
            print("Invalid choice. Please try again.")

# Function to prompt the user to input the subSubCategory for filtering
def select_sub_sub_category():
    sub_sub_categories = [
        "sword",  # Replace with actual sub-sub categories available
        "sword2h",
        "dagger",
        "bow",
        "crossbow",
        "staff",
        "wand",
        "head",
        "chest",
        "hands",
        "legs",
        "feet",
        "cloak",
        "necklace",
        "belt",
        "bracelet",
        "ring"
    ]
    
    print("\nSelect a Sub Sub Category:")
    for idx, category in enumerate(sub_sub_categories, 1):
        print(f"{idx}. {category}")

    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in map(str, range(1, len(sub_sub_categories) + 1)):
            sub_sub_category = sub_sub_categories[int(choice) - 1]
            print(f"Selected Sub Sub Category: {sub_sub_category}")
            return sub_sub_category
        else:
            print("Invalid choice. Please try again.")

# Main function to handle user input
def main():
    while True:
        print("\n=== Document Generation Menu ===")
        print("1. Generate Auction House Summary")
        print("2. Generate Trait Extract Summary")
        print("3. Exit")
        choice = input("Select an option (1, 2, or 3): ")

        if choice == "1":
            region_id = select_region()
            generate_auction_house_summary(region_id)
        elif choice == "2":
            region_id = select_region()
            sub_sub_category = select_sub_sub_category()
            generate_trait_extract_summary(region_id, sub_sub_category)
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    main()
