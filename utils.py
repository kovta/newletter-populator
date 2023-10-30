import requests
import os
from dotenv import load_dotenv
from urllib import parse

load_dotenv()
api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL')

def build_cell_range_url(ranges):
    base = f"{base_url}/values:batchGet?"
    for range in ranges:
        base += f"ranges={range}&"
    return f"{base}key={api_key}"


def get_cell_ranges(cell_ranges):
    try:
        # Construct the URL to fetch data from the specified cell
        response = requests.get(build_cell_range_url(cell_ranges))

        if response.status_code == 200:
            data = response.json()
            return data.get('valueRanges', [])

        else:
            print(f"Failed to fetch data from {cell_ranges}. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None


def build_cell_url(sheet_name, cell_id):
    return f"{base_url}/values/{sheet_name}!{cell_id}?key={api_key}"


def get_text_from_cell(sheet_name, cell_id):
    try:
        # Construct the URL to fetch data from the specified cell
        response = requests.get(build_cell_url(sheet_name, cell_id))

        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            if values:
                return values[0][0] # Assuming we're fetching a single cell

        else:
            print(f"Failed to fetch data from {cell_id}. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None


def replace_strings(input_str, replacements):
    """
    Replace old strings with new strings in the input string.

    Parameters:
    input_str (str): The input string where replacements will be made.
    replacements (list): A list of tuples, each containing (old_str, new_str).

    Returns:
    str: The input string with replacements made.
    """
    for old_str, new_str in replacements:
        input_str = input_str.replace(old_str, new_str)
    return input_str


def read_template_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied. You may not have access to read the file."
    except Exception as e:
        return "An error occurred: " + str(e)


def substitue_template_contents(file_path, replacements):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Replace each old string with the corresponding new string
        updated_contents = replace_strings(file_contents, replacements)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_contents)

        print("Successfully replaced strings in the file.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied. You may not have access to write to the file.")
    except Exception as e:
        print("An error occurred:", str(e))


def write_to_file(file_path, content):
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print("Successfully wrote to the new file.")
    except PermissionError:
        print("Permission denied. You may not have access to write to the file.")
    except Exception as e:
        print("An error occurred:", str(e))


def concatenate_arrays(*arrays):
    concatenated_array = []
    for array in arrays:
        concatenated_array += array
    return concatenated_array


def flatten_single_level(arr):
    return [item for sublist in arr for item in sublist]


def urlify(string):
    return parse.quote(string)


def rangify(sheet, range):
    return f"{urlify(sheet)}!{range}"
