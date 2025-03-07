import os
from datetime import datetime
import json

def get_newest_outland_journal_file(folder_path):
    try:
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not text_files:
            print(f"No .txt files found in {folder_path}")
            return None
        
        newest_file = max(text_files,key=lambda f: os.path.getmtime(os.path.join(folder_path, f)))
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

def get_latest_inventory_summary_file(folder_path):
    try:# List files that contain base_name and end with .json
        files = [f for f in os.listdir(folder_path) if "inventory_summary" in f and f.endswith(".json")]
        if not files:
            print(f"No .txt files found in {folder_path}")
            return
            # Find the file with the latest modification time
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
        return os.path.join(folder_path, latest_file)
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
                if "[Razor]: …OutlandMall Start" in line:
                    in_scan_section = True
                    continue

                # Fin de la section de scan
                if "[Razor]: …OutlandMall End" in line:
                    break

                if in_scan_section:
                    # Détection du début d'un vendeur
                    if "[Razor]: …vendorStart" in line:
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
                    if "[Razor]: …vendorEnd" in line and current_vendor:
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
                    if "[Razor]: …item" in line and current_vendor:
                        # Filtre les tags inutiles
                        line = line.replace("(used to increase a player's skill cap for a skill by 1)", "")
                        # Vérifier si la ligne contient "|| Stack Price:" ou "|| Price:"
                        if " Stack Price:" in line:
                            parts = line.split(" Stack Price:")
                            is_stack = True
                        elif " Price:" in line:
                            parts = line.split(" Price:")
                            is_stack = False
                        else:
                            print(f"Error at line {line_num}: Missing price information in item line: {line}")
                            continue

                        item_id_part = parts[0].strip().split()
                        if len(item_id_part) < 4:
                            print(f"Error at line {line_num}: Malformed item ID in line: {line}")
                            continue
                        item_id = item_id_part[5]  # Ajuster l'indice selon le format réel

                        price_desc = parts[1].strip()

                        if is_stack:
                            # Traitement spécifique pour les lignes contenant "Stack Price:"
                            stack_parts = price_desc.split(" each ", 1)
                            if len(stack_parts) < 2:
                                print(f"Error at line {line_num}: Malformed stack price line: {line}")
                                continue
                            stack_price = stack_parts[0].strip().replace(",", "")
                            desc_amount = stack_parts[1].strip()
                            
                            extra_info = ""
                            if "(" in desc_amount and ")" in desc_amount:
                                start = desc_amount.index("(")
                                end = desc_amount.index(")")
                                extra_info = desc_amount[start:end+1].strip()
                                desc_amount = desc_amount[:start].strip() + desc_amount[end+1:].strip()
                            
                            if " : " in desc_amount:
                                description, amount = desc_amount.split(" : ", 1)
                                description = description.strip()
                                amount = amount.strip()
                            else:
                                description = desc_amount
                                amount = "1"  # Valeur par défaut si aucune quantité n'est spécifiée
                                
                            if extra_info:
                                description += f" {extra_info}"
                                    
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
                            desc_amount = price_parts[1].strip()
                            
                            extra_info = ""
                            if "(" in desc_amount and ")" in desc_amount:
                                start = desc_amount.index("(")
                                end = desc_amount.index(")")
                                extra_info = desc_amount[start:end+1].strip()
                                desc_amount = desc_amount[:start].strip() + desc_amount[end+1:].strip()
                            
                            if " : " in desc_amount:
                                description, amount = desc_amount.split(" : ", 1)
                                description = description.strip()
                                amount = amount.strip()
                            else:
                                description = desc_amount
                                amount = "1"  # Valeur par défaut si aucune quantité n'est spécifiée
                                
                            if extra_info:
                                description += f" {extra_info}"
                                    
                            item = {
                                "id": item_id,
                                "price": price,
                                "description": description,
                                "amount": amount
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

        timestamp = datetime.now().strftime("%Y-%m-%d")
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
                            f.write(f"  - Item ID: {item['id']}, Description: {item['description']}, Amount: {item['amount']}, Stack Price: {item['stack_price']}\n")
                        else:
                            f.write(f"  - Item ID: {item['id']}, Description: {item['description']}, Amount: {item['amount']}, Price: {item['price']}\n")
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
    
def save_inventory_data(inventory_summary, total_inventory_value, output_dir, input_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d")
        base_name = os.path.splitext(os.path.basename(input_file_name))[0]
        output_file = os.path.join(output_dir, f"{base_name}_inventory_summary_{timestamp}.txt")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Processed Vendor Data from {input_file_name}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("====================== Inventory Summary ======================\n\n")
            for description, details in inventory_summary.items():
                prices_str = ', '.join(str(p) for p in details['prices'])
                f.write(f"- Item Description: {description}, Total Amount: {details['amount']}, Prices: [{prices_str}], Average Price: {details['avg_unit_price']:.1f}, Total Value: {details['total_value']}\n")
            
            f.write(f"\nOverall Total Value: {total_inventory_value}\n")
            f.write("\n===============================================================")

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
                    print(f"  - Item ID: {item['id']}, Description: {item['description']}, Amount: {item['amount']}, Stack Price: {item['stack_price']}")
                else:
                    print(f"  - Item ID: {item['id']}, Description: {item['description']}, Amount: {item['amount']}, Price: {item['price']}")
        else:
            print("  (No items listed)")
        print("-" * 50)
   
   
def display_inventory_data(inventory_summary, total_inventory_value):
    print("\n====================== Inventory Summary ======================\n")
    for description, details in inventory_summary.items():
        print(f"- Item Description: {description}, Total Amount: {details['amount']}, Prices: {details['prices']}, Average Unit Price: {details['avg_unit_price']:.1f}, Total Value: {details['total_value']}")

    print(f"\nOverall Total Value: {total_inventory_value}")
    print("\n===============================================================")
    
def save_vendor_data_json(vendors, output_dir, input_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_file_name))[0]
        output_file = os.path.join(output_dir, f"{base_name}_processed_{timestamp}.json")

        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(vendors, json_file, indent=4, ensure_ascii=False)

        print(f"JSON Data saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return None
    
def summarize_inventory(vendors):
    inventory_summary = {}
    total_value = 0

    for vendor in vendors:
        for item in vendor["items"]:
            description = item["description"]
            # Determine price based on stack_price or price
            if "stack_price" in item:
                price = int(item["stack_price"].replace(",", ""))
            else:
                price_total = int(item.get("price", "0").replace(",", ""))
                amount_temp = int(item.get("amount", "1").replace(",", ""))
                price = int(price_total / amount_temp) #if amount_temp != 0 else price_total

            amount = int(item.get("amount", "1").replace(",", ""))
            item_total_value = price * amount
            total_value += item_total_value

            if description in inventory_summary:
                # Update existing entry
                inventory_summary[description]["amount"] += amount
                inventory_summary[description]["total_value"] += item_total_value
                # Track multiple prices if they differ
                if price not in inventory_summary[description]["prices"]:
                    inventory_summary[description]["prices"].append(price)
            else:
                # Create new entry
                inventory_summary[description] = {
                    "amount": amount,
                    "prices": [price],  # List to store different prices
                    "total_value": item_total_value
                }

    # Optional: Calculate average price per item after processing
    for description in inventory_summary:
        prices = inventory_summary[description]["prices"]
        inventory_summary[description]["avg_unit_price"] = (
            sum(prices) / len(prices) if prices else 0
        )

    return inventory_summary, total_value

def save_inventory_json(inventory_summary, total_value, output_dir, input_file_name):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(input_file_name))[0]
        output_file = os.path.join(output_dir, f"{base_name}_inventory_summary_{timestamp}.json")
        
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump({"inventory": inventory_summary, "total_value": total_value}, json_file, indent=4, ensure_ascii=False)
        
        print(f"Inventory JSON saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error saving inventory JSON: {e}")
        return None
    
def main():
    input_folder_path = r"C:\Program Files (x86)\Ultima Online Outlands\ClassicUO\Data\Client\JournalLogs"
    output_directory = os.path.join(r"C:\Users\xxxx\Documents", "Processed")
    
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' does not exist. Please check the path.")
        return

    newest_file = get_newest_outland_journal_file(input_folder_path)
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
    
    json_file = save_vendor_data_json(vendors, output_directory, newest_file)
    if not json_file:
        print("Failed to save the JSON data. Check error messages above.")
        return
    
    inventory_summary, total_inventory_value = summarize_inventory(vendors)
    if inventory_summary is None:
        print("Error: Failed to summarize inventory.")
        return
    
    inventory_json = save_inventory_json(inventory_summary, total_inventory_value, output_directory, newest_file)
    if not inventory_json:
        print("Failed to save the inventory summary. Check error messages above.")
        return
    
    inventory_data = save_inventory_data(inventory_summary, total_inventory_value, output_directory, newest_file)
    if not inventory_data:
        print("Failed to save the inventory summary. Check error messages above.")
        return
    
    display_vendor_data(vendors)
    display_inventory_data(inventory_summary, total_inventory_value)

if __name__ == "__main__":
    main()
