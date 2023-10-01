import requests

api_key = ""
base_url = ""
sheets = ["Creative"]

CREATIVE_NAME = "F2"
CGD_TITLE = "B11"

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


def read_template_contents(file_path):
    try:
        # Open the file in read mode ('r')
        with open(file_path, 'r') as file:
            # Read the entire contents of the file
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied. You may not have access to read the file."
    except Exception as e:
        return "An error occurred: " + str(e)


for sheet in sheets:
    get_text_from_cell(sheet, "B9")
