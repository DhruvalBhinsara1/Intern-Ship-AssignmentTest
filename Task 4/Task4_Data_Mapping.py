
# Import required libraries
import pandas as pd  # For data manipulation
import re            # For regular expressions
import os            # For file and directory operations


# Map a keyword and URL to a Category and Sub-Category based on business rules
def map_category_subcategory(keyword, url):
    """
    Map keyword and URL to Category and Sub-Category based on guidelines.
    Uses keyword analysis, URL patterns, and business logic.
    """
    keyword_lower = keyword.lower() if keyword else ""
    url_lower = url.lower() if url else ""

    # Check for specific product categories (most specific)
    # Fresh produce
    if any(fresh in keyword_lower for fresh in ['vegetable', 'fruit', 'greens', 'potato', 'onion', 'tomato', 'broccoli', 'carrot', 'cucumber', 'spinach', 'ash gourd']):
        return 'E-commerce', 'Fresh Produce'
    elif any(fresh in keyword_lower for fresh in ['fish', 'meat', 'poultry', 'seafood', 'salmon', 'chicken', 'mutton', 'rohu']):
        return 'E-commerce', 'Fresh Meat & Seafood'
    elif any(fresh in keyword_lower for fresh in ['flower', 'bouquet', 'plants', 'jasmine', 'rose', 'lily']):
        return 'E-commerce', 'Fresh Flowers & Plants'

    # Dairy products
    if any(dairy in keyword_lower for dairy in ['milk', 'dairy', 'cheese', 'butter', 'yogurt', 'curd']):
        return 'E-commerce', 'Dairy Products'

    # Bakery items
    if any(bakery in keyword_lower for bakery in ['bread', 'bakery', 'cake', 'pastry', 'cookie', 'ice cream', 'dessert']):
        return 'E-commerce', 'Bakery Items'

    # Snacks
    if any(snack in keyword_lower for snack in ['snack', 'chips', 'chocolate', 'cookies', 'namkeen']):
        return 'E-commerce', 'Snacks & Sweets'

    # Grains and staples
    if any(grain in keyword_lower for grain in ['rice', 'wheat', 'grain', 'flour', 'atta', 'maida']):
        return 'E-commerce', 'Grains & Cereals'

    # Cooking essentials
    if any(essential in keyword_lower for essential in ['oil', 'ghee', 'butter', 'sugar', 'salt', 'spice', 'masala']):
        return 'E-commerce', 'Cooking Essentials'

    # Beverages
    if any(beverage in keyword_lower for beverage in ['tea', 'coffee', 'juice', 'soda', 'drink', 'water']):
        return 'E-commerce', 'Beverages'

    # Household items
    if any(household in keyword_lower for household in ['cleaning', 'detergent', 'soap', 'stationery', 'pen', 'paper']):
        return 'E-commerce', 'Household Items'

    # Location-based searches (e.g., "near me")
    location_keywords = ['near me', 'nearby', 'close to', 'around me', 'in my area']
    if any(loc in keyword_lower for loc in location_keywords):
        if any(word in keyword_lower for word in ['restaurant', 'food', 'swiggy']):
            return 'Food & Dining', 'Local Restaurants'
        elif any(word in keyword_lower for word in ['grocery', 'vegetable', 'fruit', 'bigbasket', 'supermarket', 'store', 'stationery', 'chicken']):
            return 'E-commerce', 'Local Grocery Stores'
        else:
            return 'Local Services', 'Nearby Services'

    # Swiggy specific mappings (food delivery)
    if 'swiggy' in url_lower:
        if 'instamart' in url_lower or 'instamart' in keyword_lower:
            return 'E-commerce', 'Instant Grocery'
        elif 'partner' in url_lower or 'partner' in keyword_lower:
            return 'Business Services', 'Food Delivery Partnership'
        elif any(word in keyword_lower for word in ['customer care', 'support', 'help', 'contact']):
            return 'Customer Service', 'Food Delivery Support'
        elif any(word in keyword_lower for word in ['restaurant', 'food', 'delivery', 'order']):
            return 'Food & Dining', 'Food Delivery'
        else:
            return 'Food & Dining', 'Restaurant Discovery'

    # Food/restaurant related keywords
    food_keywords = ['restaurant', 'food', 'pizza', 'burger', 'biryani', 'chinese', 'italian', 'cafe', 'dining']
    if any(food in keyword_lower for food in food_keywords):
        return 'Food & Dining', 'Restaurants'

    # Specific food types
    if any(food in keyword_lower for food in ['vegetarian', 'veg', 'vegan']):
        return 'Food & Dining', 'Vegetarian Restaurants'
    elif any(food in keyword_lower for food in ['non veg', 'chicken', 'meat']):
        return 'Food & Dining', 'Non-Vegetarian Restaurants'
    elif 'bar' in keyword_lower or 'pub' in keyword_lower:
        return 'Food & Dining', 'Bars & Pubs'

    # BigBasket specific mappings (grocery/e-commerce)
    if 'bigbasket' in url_lower or 'big basket' in keyword_lower:
        if any(word in keyword_lower for word in ['partner', 'seller', 'vendor', 'business']):
            return 'Business Services', 'E-commerce Partnership'
        elif any(word in keyword_lower for word in ['care', 'support', 'help', 'contact']):
            return 'Customer Service', 'E-commerce Support'
        else:
            return 'E-commerce', 'Grocery Delivery'

    # Delivery services
    if 'delivery' in keyword_lower or 'order' in keyword_lower:
        if any(word in keyword_lower for word in ['food', 'restaurant', 'swiggy']):
            return 'Food & Dining', 'Food Delivery'
        elif any(word in keyword_lower for word in ['grocery', 'bigbasket']):
            return 'E-commerce', 'Grocery Delivery'
        else:
            return 'Delivery Services', 'General Delivery'

    # Grocery/shopping related general
    if any(grocery in keyword_lower for grocery in ['grocery', 'supermarket', 'store', 'shopping']):
        return 'E-commerce', 'Grocery Shopping'

    # URL-based categorization for specific domains
    if 'swiggy.com' in url_lower:
        return 'Food & Dining', 'Online Food Ordering'
    elif 'bigbasket.com' in url_lower:
        return 'E-commerce', 'Online Grocery'

    # Generic fallbacks for online shopping
    if any(word in keyword_lower for word in ['online', 'shopping', 'buy', 'purchase']):
        return 'E-commerce', 'Online Shopping'

    # Default categories based on keyword intent
    if len(keyword_lower.split()) <= 2:  # Brand or short queries
        return 'Brand Search', 'Direct Navigation'
    else:
        return 'General Search', 'Information Search'


# Process an Excel file: add Category and Sub-Category columns using mapping logic
def process_excel_file(file_path):
    """
    Process Excel file to add Category and Sub-Category columns.
    Reads the file, applies mapping, and saves the result.
    """
    print(f"Processing: {file_path}")

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Add columns if not already present
    if 'Category' not in df.columns:
        df['Category'] = ''
    if 'Sub-Category' not in df.columns:
        df['Sub-Category'] = ''

    # Process each row and assign category/sub-category
    for idx, row in df.iterrows():
        keyword = str(row.get('Keyword', ''))
        url = str(row.get('URL', ''))

        category, subcategory = map_category_subcategory(keyword, url)

        df.at[idx, 'Category'] = category
        df.at[idx, 'Sub-Category'] = subcategory

        # Print progress every 5000 rows
        if (idx + 1) % 5000 == 0:
            print(f"  Processed {idx + 1}/{len(df)} rows")

    # Save the updated DataFrame to mapped data set folder
    mapped_folder = r"e:\Intern-Ship-AssignmentTest\Task 4\mapped data set"
    os.makedirs(mapped_folder, exist_ok=True)
    filename = os.path.basename(file_path).replace('.xlsx', '_mapped.xlsx')
    output_path = os.path.join(mapped_folder, filename)
    df.to_excel(output_path, index=False)

    print(f"✓ Saved mapped file: {output_path}")
    print(f"  Total rows processed: {len(df)}")
    print(f"  Categories found: {df['Category'].nunique()}")
    print(f"  Sub-categories found: {df['Sub-Category'].nunique()}")
    print()

    return df


# Main execution function
def main():
    print("Task 4: Research Data Mapping")
    print("=" * 50)

    # Folder containing input Excel files
    data_folder = r"e:\Intern-Ship-AssignmentTest\Task 4\data-set"

    # List of files to process
    files_to_process = [
        "Positions.bigbasket.com.xlsx",
        "Positions.swiggy.com.xlsx"
    ]

    # Process each file
    for filename in files_to_process:
        file_path = os.path.join(data_folder, filename)
        if os.path.exists(file_path):
            process_excel_file(file_path)
        else:
            print(f"File not found: {file_path}")

    print("Data mapping completed for both sheets!")


# Script entry point
if __name__ == "__main__":
    main()