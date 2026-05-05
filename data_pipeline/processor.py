import json
import os

def load_data(file_path):
    """Loads raw JSON data from the specified file path."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def clean_product(product):
    """Cleans and validates individual product data."""
    # Helper to safely convert to integer
    def to_int(val, default=0):
        try:
            return int(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    # Helper to safely convert to float
    def to_float(val, default=0.0):
        try:
            return float(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    # Helper to safely clean string
    def clean_str(val, default=""):
        return str(val).strip() if val is not None else default

    cleaned = {
        "name": clean_str(product.get("name")),
        "url": product.get("url"),
        "image_url": product.get("image_url"),
        "price": to_int(product.get("price")),
        "rating": to_float(product.get("rating")),
        "sold": to_int(product.get("sold")),
        "comment": clean_str(product.get("description"))
    }
    
    return cleaned

def transform_data(raw_data):
    """Transforms a list of raw products into cleaned products."""
    print(f"Starting transformation of {len(raw_data)} products...")
    processed_data = [clean_product(item) for item in raw_data]
    print("Transformation complete.")
    return processed_data

def save_data(data, output_path):
    """Saves the processed data to a JSON file."""
    try:
        # Ensure target directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved {len(data)} items to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data_raw.json")
    output_file = os.path.join(base_dir, "data_processed.json")
    
    # Alternative output path if 'data' folder is required as per requirement 4
    # data_dir_output = os.path.join(os.path.dirname(base_dir), "data", "data_processed.json")

    print("--- DATA PROCESSING PIPELINE ---")
    
    # Execute Pipeline
    raw_products = load_data(input_file)
    if raw_products:
        processed_products = transform_data(raw_products)
        save_data(processed_products, output_file)
    else:
        print("No data to process.")
