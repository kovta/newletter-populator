import requests
import os
import sys
from dotenv import load_dotenv
from minify_html import minify
from urllib import parse

# load_dotenv()
# api_key = os.getenv('API_KEY')
# base_url = os.getenv('BASE_URL')

if not api_key:
    print("ERROR: No API key provided")
    sys.exit(1)

if not base_url:
    print("ERROR: Google Sheet base URL not specified")
    sys.exit(1)

# Use for local execution
# script_directory = os.path.dirname(os.path.abspath(__file__))

# Use for binary
script_directory = os.path.dirname(os.path.abspath(sys.executable))


def build_cell_range_url(ranges):
    base = f"{base_url}/values:batchGet?"
    for range in ranges:
        base += f"ranges={range}&"
    return f"{base}key={api_key}"


def fetch_cell_range_values(cell_ranges):
    try:
        # Construct the URL to fetch the data array from the specified cell range
        response = requests.get(build_cell_range_url(cell_ranges))

        if response.status_code == 200:
            data = response.json()
            return data.get('valueRanges', [])

        else:
            print(
                f"Failed to fetch data from {cell_ranges}. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None


def build_cell_url(sheet_name, cell_id):
    return f"{base_url}/values/{sheet_name}!{cell_id}?key={api_key}"


def fetch_text_from_cell(sheet_name, cell_id):
    try:
        # Construct the URL to fetch data from the specified cell
        response = requests.get(build_cell_url(sheet_name, cell_id))

        if response.status_code == 200:
            data = response.json()
            values = data.get('values', [])
            if values:
                return values[0][0]  # Assuming we're fetching a single cell

        else:
            print(
                f"Failed to fetch data from {cell_id}. Status code: {response.status_code}")

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
        with open(f"{script_directory}/{file_path}", 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied. You may not have access to read the file."
    except Exception as e:
        return "An error occurred: " + str(e)


def write_to_file(file_path, content):
    file_path = os.path.normpath(f"{script_directory}/{file_path}")
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Successfully wrote content to: {file_path}")
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


def check_filled(*args):
    for arg in args:
        if arg is None or arg == '':
            raise ValueError("Missing section data")


def minify_html(input: str):
    return minify(input, minify_css=True).replace("                              ", "")
