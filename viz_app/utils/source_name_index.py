from django.conf import settings
import os

index_to_name = {}
name_to_index = {}

def load_catalog():
    file_path = os.path.join(settings.BASE_DIR,"viz_app","utils", "AS1ssmcatalog.cat")
    global index_to_name, name_to_index
    index_to_name.clear()
    name_to_index.clear()

    # Ensure file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#") or line.strip() == "":
                    continue  # Skip comments and empty lines
                
                parts = line.split()
                if len(parts) < 4:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue
                
                src_index = int(parts[3])  # Extract src_index
                src_name = parts[2]        # Extract src_name
                
                index_to_name[src_index] = src_name
                name_to_index[src_name] = src_index
    except Exception as e:
        print(f"Error reading catalog: {e}")

    

# Function to get src_name by src_index
def get_src_name(index):
    return index_to_name.get(index, "Not Found")

# Function to get src_index by src_name
def get_src_index(name):
    return name_to_index.get(name, "Not Found")

def get_src_name_full():
    return name_to_index

def get_src_index_full():
    return index_to_name

# Load the catalog when the module is imported
load_catalog()
