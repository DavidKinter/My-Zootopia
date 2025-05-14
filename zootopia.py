"""
Processes animal data from 'animals_data.json' and prints key details for
each animal.
"""

import json

# Define constants at the module level
ANIMALS_DATA_FILE = "animals_data.json"
ANIMALS_TEMPLATE_FILE = "animals_template.html"
OUTPUT_HTML_FILE = "animals.html"
DEFAULT_NA_VALUE = "N/A"
HTML_PLACEHOLDER_TEXT = "__REPLACE_ANIMALS_INFO__"


def load_json(file_path=ANIMALS_DATA_FILE):
    """
    Loads data from ANIMALS_DATA_FILE.
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None  # Compliance with pylint rules
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not valid JSON.")
        return None  # Compliance with pylint rules


def load_html(file_path=ANIMALS_TEMPLATE_FILE):
    """
    Loads html template from ANIMALS_TEMPLATE_FILE.
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as handle:
            html_str = handle.read()
        return html_str
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except IOError:
        print(f"Error: Could not read file at {file_path}")
        return None


def format_value(value_str):
    """
    Helper function. Checks if 'value_str' is a string and capitalizes all
    words in it, unless it is "N/A" (DEFAULT_NA_VALUE). If it is "N/A",
    the function returns the original 'value_str' unchanged. The function
    makes sure all items from the JSON file are properly, and identically,
    formatted.
    """
    if (isinstance(value_str, str)  # Checks if 'value_str' is type(str)
            and value_str.lower() != DEFAULT_NA_VALUE.lower()):
        title_cased_str = value_str.title()
        # Correct apostrophe followed by 'S' (for Darwin's Fox)
        return title_cased_str.replace("’S", "’s")
    return value_str


def create_template_dict(animal_data):
    """
    Helper function. Takes a raw animal data dictionary, extracts and formats
    relevant details, and returns them as a new dictionary for the HTML
    template.
    """
    # Safely extract data for individual animal
    animal_name = animal_data.get("name", DEFAULT_NA_VALUE)
    locations_list = animal_data.get("locations")
    if locations_list and isinstance(locations_list, list):
        animal_location = locations_list[0]
    else:
        animal_location = DEFAULT_NA_VALUE
    animal_diet = animal_data["characteristics"].get("diet", DEFAULT_NA_VALUE)
    animal_type = animal_data["characteristics"].get("type", DEFAULT_NA_VALUE)

    # Formats extracted data
    formatted_name = format_value(animal_name)
    formatted_diet = format_value(animal_diet)
    formatted_location = format_value(animal_location)
    formatted_type = format_value(animal_type)

    # Returns dict for current animal
    animal_dict = {
        "name":     formatted_name,
        "diet":     formatted_diet,
        "location": formatted_location,
        "type":     formatted_type
        }
    return animal_dict


def return_list_for_template():
    """
    Calls 'load_json' to load animal data from 'animals_data.json' and
    returns list of dicts with animal's 'name', 'diet', 'first location
    from the locations list', and 'type'
    """
    data = load_json()  # Loads data from 'animals_data.json'
    if data is None:  # If None reuturned upon FileNotFound / JSONDecodeError
        return []  # Empty list to prevent subsequent errors
    animals_list = []
    # Iterate through JSON data, extract items, and create new list of dicts
    for animal in data:
        processed_animal_dict = create_template_dict(animal)
        animals_list.append(processed_animal_dict)
    return animals_list


def create_str_for_template():
    """
    Creates raw input for HTML template from new list of dictionaries
    'animals_list' with animal's 'name', 'diet', 'first location from the
    locations list', and 'type'
    """
    animals_list = return_list_for_template()
    animal_strings = []
    for animal in animals_list:
        animal_strings.append(
            f'<li class="cards__item">'
            f'<div class="card__title">{animal["name"]}</div>'
            f'<p class="card__text">'
            f"<strong>Diet:</strong> {animal["diet"]}<br/>"
            f"<strong>Location:</strong> {animal["location"]}<br/>"
            f"<strong>Type:</strong> {animal["type"]}<br/>"
            f"</p>"
            f"</li>"
            )
    return "\n\n".join(animal_strings)


def create_updated_html():
    """
    Generates HTML content by inserting filtered data from 'animals_data.json'
    into the placeholder '__REPLACE_ANIMALS_INFO__' in 'animals_template.html'
    This function first loads the base HTML template and retrieves a
    formatted string of relevant animal details. If the placeholder is not
    found in the template, an empty string is returned.
    """
    # Loads 'animals_template.html'
    html_template = load_html()
    if html_template is None:  # Error reading 'animals_template.html'
        print("Error: HTML template could not be loaded. "
              "Cannot create updated HTML."
              )
        return ""
    replacement_str = create_str_for_template()  # Loads input str for html
    updated_html_str = ""
    if HTML_PLACEHOLDER_TEXT in html_template:
        updated_html_str = (html_template
        .replace(
            HTML_PLACEHOLDER_TEXT,
            replacement_str
            )
        )
    return updated_html_str


def persist_updated_html(updated_html_str, file_path=OUTPUT_HTML_FILE):
    """
    Persists the provided HTML string to the specified file.
    This function will create the file if it does not exist,
    or overwrite it if it does.
    """
    # Handles empty string from create_updated_html
    if not updated_html_str:  # If no new HTML content was created from JSON
        print("No HTML content provided to persist. File will not be written.")
        return False  # Indicate failure or no action

    try:
        with open(file_path, "w", encoding="UTF-8") as handle:
            handle.write(updated_html_str)
        print(f"Successfully saved updated HTML to {file_path}")
        return True  # Indicate success
    except IOError as e:
        print(f"Error: Could not write to file at {file_path}. Reason: {e}")
        return False  # Indicate failure


def main():
    """
    Main program:
    Loads animal data from JSON, generates an HTML representation,
    and saves it to 'animals.html'.
    """
    updated_html_str = create_updated_html()

    # persist_updated_html will handle empty content, but we can be explicit
    if updated_html_str:
        persist_updated_html(updated_html_str, file_path=OUTPUT_HTML_FILE)
    else:
        print(f"HTML content generation failed or resulted in empty content. "
              f"Skipping persistence to {OUTPUT_HTML_FILE}."
              )


if __name__ == "__main__":
    main()
