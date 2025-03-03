import os
from datetime import datetime
import json

def get_newest_file(folder_path):
    try:
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not text_files:
            print(f"No .txt files found in {folder_path}")
            return None
        
        newest_file = max(
            text_files,
            key=lambda f: os.path.getmtime(os.path.join(folder_path, f))
        )
        return os.path.join(folder_path, newest_file)
    except FileNotFoundError:
        print(f"Error: The folder '{folder_path}' does not exist.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to access '{folder_path}'.")
        return None
    except Exception as e:
        print(f"Error accessing folder '{folder_path}': {e}")
        return None

def process_vendor_data(file_path):
    vendors = []
    current_vendor = None
    in_scan_section = False

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for line_num, line in enumerate(lines, 1):
                line = line.strip()

                # Démarrage de la section de scan
                if "[Razor]: Simple Vendor Scan" in line:
                    in_scan_section = True
                    continue

                # Fin de la section de scan
                if "[Razor]: OutlandMall End" in line:
                    break

                if in_scan_section:
                    # Détection du début d'un vendeur
                    if "[Razor]: Start" in line:
                        parts = line.split()
                        # Vérifier qu'on a bien au moins 6 éléments (par exemple : "[Razor]:", "Start", "<timestamp>", "<ID>", "<vendor_id>", "<vendor_name>")
                        if len(parts) < 6:
                            print(f"Error at line {line_num}: Malformed vendor start line: {line}")
                            continue
                        vendor_id = parts[4]
                        vendor_name = " ".join(parts[5:]).strip()
                        current_vendor = {"id": vendor_id, "name": vendor_name, "location": None, "items": []}
                        continue

                    # Fin d'un vendeur
                    if "[Razor]: End" in line and current_vendor:
                        vendors.append(current_vendor)
                        current_vendor = None
                        continue

                    # Extraction de la localisation
                    if "System: Current location is" in line and current_vendor:
                        _, _, location = line.partition("System: Current location is")
                        if not location.strip():
                            print(f"Error at line {line_num}: Malformed location line: {line}")
                            continue
                        current_vendor["location"] = location.strip()
                        continue

                    # Extraction des articles
                    if "[Razor]: Item:" in line and current_vendor:
                        # Vérifier si la ligne contient "|| Stack Price:" ou "|| Price:"
                        if "|| Stack Price:" in line:
                            parts = line.split("|| Stack Price:")
                            is_stack = True
                        elif "|| Price:" in line:
                            parts = line.split("|| Price:")
                            is_stack = False
                        else:
                            print(f"Error at line {line_num}: Missing price information in item line: {line}")
                            continue

                        item_id_part = parts[0].strip().split()
                        if len(item_id_part) < 3:
                            print(f"Error at line {line_num}: Malformed item ID in line: {line}")
                            continue
                        item_id = item_id_part[4]  # Ajuster l'indice selon le format réel

                        price_desc = parts[1].strip()

                        if is_stack:
                            # Traitement spécifique pour les lignes contenant "Stack Price:"
                            stack_parts = price_desc.split(" each ", 1)
                            if len(stack_parts) < 2:
                                print(f"Error at line {line_num}: Malformed stack price line: {line}")
                                continue
                            stack_price = stack_parts[0].strip().replace(",", "")
                            desc_amount = stack_parts[1].strip()
                            if " : " in desc_amount:
                                description, amount = desc_amount.split(" : ", 1)
                                description = description.strip()
                                amount = amount.strip()
                            else:
                                description = desc_amount
                                amount = "1"  # Valeur par défaut si aucune quantité n'est spécifiée
                            item = {
                                "id": item_id,
                                "stack_price": stack_price,
                                "description": description,
                                "amount": amount
                            }
                        else:
                            # Traitement pour les lignes contenant "Price:"
                            price_parts = price_desc.split(maxsplit=1)
                            if len(price_parts) < 2:
                                print(f"Error at line {line_num}: Missing price/description in line: {line}")
                                continue
                            price = price_parts[0].replace(",", "")
                            description = price_parts[1].strip()
                            item = {
                                "id": item_id,
                                "price": price,
                                "description": description
                            }
                        current_vendor["items"].append(item)

        return vendors
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
        return []
    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return []

def save_vendor_data(vendors, output_dir, input_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_file_name))[0]
        output_file = os.path.join(output_dir, f"{base_name}_processed_{timestamp}.txt")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Processed Vendor Data from {input_file_name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for vendor in vendors:
                f.write(f"Vendor: {vendor['name']} (ID: {vendor['id']})\n")
                f.write(f"Location: {vendor['location']}\n")
                f.write("Inventory:\n")
                if vendor['items']:
                    for item in vendor['items']:
                        if "stack_price" in item:
                            f.write(f"  - Item ID: {item['id']}, Stack Price: {item['stack_price']}, "
                                    f"Description: {item['description']}, Amount: {item['amount']}\n")
                        else:
                            f.write(f"  - Item ID: {item['id']}, Price: {item['price']}, "
                                    f"Description: {item['description']}\n")
                else:
                    f.write("  (No items listed)\n")
                f.write("-" * 50 + "\n")
        
        print(f"Data saved to: {output_file}")
        return output_file
    except PermissionError:
        print(f"Error: Permission denied to write to '{output_dir}'.")
        return None
    except Exception as e:
        print(f"Error saving data to '{output_dir}': {e}")
        return None

def display_vendor_data(vendors):
    for vendor in vendors:
        print(f"\nVendor: {vendor['name']} (ID: {vendor['id']})")
        print(f"Location: {vendor['location']}")
        print("Inventory:")
        if vendor['items']:
            for item in vendor['items']:
                if "stack_price" in item:
                    print(f"  - Item ID: {item['id']}, Stack Price: {item['stack_price']}, Description: {item['description']}, Amount: {item['amount']}")
                else:
                    print(f"  - Item ID: {item['id']}, Price: {item['price']}, Description: {item['description']}")
        else:
            print("  (No items listed)")
        print("-" * 50)

def main():
    input_folder_path = r"C:\Program Files (x86)\Ultima Online Outlands\ClassicUO\Data\Client\JournalLogs"
    output_directory = os.path.join(r"C:\Users\xxxx\Documents", "Processed")
    
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' does not exist. Please check the path.")
        return

    newest_file = get_newest_file(input_folder_path)
    if not newest_file:
        print("No further processing due to missing files or access issues.")
        return

    print(f"Processing file: {newest_file}")
    
    vendors = process_vendor_data(newest_file)
    if vendors is None:
        print("Processing failed. Check error messages above.")
        return
    
    saved_file = save_vendor_data(vendors, output_directory, newest_file)
    if not saved_file:
        print("Failed to save the data. Check error messages above.")
        return
    
    display_vendor_data(vendors)

if __name__ == "__main__":
    main()
