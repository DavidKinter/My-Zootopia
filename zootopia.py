"""Processes animal data from 'animals_data.json' and prints key details for
each animal."""

import json


def load_data(file_path="animals_data.json"):
    """
    Loads data from the specified JSON file.
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None # Compliance with pylint rules
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not valid JSON.")
        return None # Compliance with pylint rules


def print_items():
    """
    Calls 'load_data' to load animal data from 'animals_data.json' and prints
    animal's, 'name', 'diet', 'first location from the locations list',
    and type
    """
    data = load_data()
    for animal in data:  # Iterate through 'animals_data.json'
        animal_name = animal.get("name", "N/A")
        locations_list = animal.get("locations")
        animal_location = locations_list[0]
        animal_diet = animal["characteristics"].get("diet", "N/A")
        animal_type = animal["characteristics"].get("type", "N/A")
        if animal_type.lower() != "n/a":  # Capitalize if actual data
            animal_type = animal_type.capitalize()
        print(f"Name: {animal_name}")
        print(f"Diet: {animal_diet}")
        print(f"Location: {animal_location}")
        print(f"Type: {animal_type}\n")


def main():
    """
    Main program:
    Loads animal data from JSON and prints animal's, 'name', 'diet',
    'location' and 'type'
    and type
    """
    print_items()


if __name__ == "__main__":
    main()
