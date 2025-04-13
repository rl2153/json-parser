import json
import os
import argparse
import re

class CarOwner:
    def __init__(self, id, first_name, last_name, email, gender, ip_address, bank, car_make, car_model):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.ip_address = ip_address
        self.bank = bank
        self.car_make = car_make
        self.car_model = car_model

    def __str__(self):
        return (f"Car Owner [ID: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, "
                f"Email: {self.email}, Gender: {self.gender}, IP: {self.ip_address}, "
                f"Bank: {self.bank}, Car Make: {self.car_make}, Car Model: {self.car_model}]")
    

def load_json_file(filename=None):
    """Prompts the user for a file path and attempts to load a JSON file."""
    while True:
        if filename is None:
            filename = input("📂 Please enter the path to the JSON file: ").strip()

        if not os.path.exists(filename):
            print(f"❌ Error: The file '{filename}' does not exist. Please check the filename and try again.")
            filename = None
            continue
            
        try:
            print("Parsing . . .")
            with open(filename, "r") as input_file:
                return json.load(input_file)  # Load and return JSON data
        except json.JSONDecodeError:
            print(f"❌ Error: The JSON structure in '{filename}' is invalid or corrupted. Please fix the file and retry.")
            filename = None
 
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            filename = None
  

def validate_record(json_obj):
    """Validates the JSON record and prints warnings for missing attributes or incorrect bank values."""
    required_keys = {'id', 'first_name', 'last_name', 'email', 'gender', 'ip_address', 'bank', 'car_make', 'car_model'}
    missing_keys = required_keys - json_obj.keys()

    if missing_keys:
        print(f"⚠️ Warning: Missing expected keys {missing_keys} in JSON record. Skipping this entry.")
        return False  # Skip corrupt records

    # Check if 'bank' value starts with "$"
    bank_value = json_obj.get('bank', '')
    if not bank_value.startswith("$"):
        print(f"⚠️ Warning: Bank value '{bank_value}' is missing a dollar sign ($). Using raw value.")

    gender_value = json_obj.get('gender', '')
    if not (gender_value.capitalize() == "Male" or gender_value.capitalize() == "Female" or gender_value.capitalize() == "Other"):
        print(f"⚠️ Warning: Gender value '{gender_value}' is unusual.")

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email = json_obj.get('email', '')
    correct_email_format = bool(re.match(pattern, email))
    if not correct_email_format:
        print(f"⚠️ Warning: Email format '{email}' is incorrect.")

    return True

def write_to_file(filename, data):
    """Attempts to write data to a file"""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)
        print(f"✅ Successfully wrote data to '{filename}'")
    
    except PermissionError:
        print(f"❌ Error: Permission denied. Cannot write to '{filename}'. Check file permissions.")
    
    except OSError as e:
        print(f"❌ OS Error: {e}")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


def main():

    # Set up parser for script arguments
    parser = argparse.ArgumentParser(description="Load a JSON file")
    parser.add_argument("filename", nargs="?", help="Path to the JSON file")
    args = parser.parse_args()

    # List of inputs that fit the criteria 
    car_owners = []
    
    data = load_json_file(args.filename)

    if data is None:
        print("⛔ Exiting program due to errors.")
        return
    
    print("✅ Input parsed successfully.")
    #print(data[0])

    for json_obj in data:
        valid = validate_record(json_obj)  # Validate each record before adding

        if valid:
            person_id = json_obj.get('id')
            first_name = json_obj.get('first_name')
            last_name = json_obj.get('last_name')
            email = json_obj.get('email')
            gender = json_obj.get('gender')
            ip_address = json_obj.get('ip_address')
            bank = json_obj.get('bank')
            car_make = json_obj.get('car_make')
            car_model = json_obj.get('car_model')
        
            balance = float(bank.strip("$"))
            if balance > 5000 and car_make.capitalize() == "Honda":
                owner = CarOwner(person_id, first_name, last_name, email, gender, ip_address, bank, car_make, car_model)
                car_owners.append(owner)


    # string builder for output
    output_builder = []
    output_builder.append("=====================================\n")
    for owner in car_owners:
        output_builder.append(f"ID: {owner.id}\n")
        output_builder.append(f"Name: {owner.first_name}\n")
        output_builder.append(f"Surname: {owner.last_name}\n")
        output_builder.append(f"Email: {owner.email}\n")
        output_builder.append(f"Gender: {owner.gender}\n")
        formatted_number = "{:,.2f}".format(float(owner.bank.strip("$"))).replace(",", "X").replace(".", ",").replace("X", ".")
        output_builder.append(f"Bank state in USD: {formatted_number}\n")
        output_builder.append("=====================================\n")

    output_string = "".join(output_builder)

    output_file = "output.txt"
    write_to_file(output_file, output_string)

        

if __name__ == "__main__":
    main()