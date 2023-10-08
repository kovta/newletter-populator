from utils import get_text_from_cell, read_template_contents, replace_strings, get_cell_ranges
from urllib import parse
from math import ceil

A_TEAMS = ["Creative", "Strategy", "UX Design", "PPC", "Development"]
B_TEAMS = ["Graphic Design", "Business & Tech", "UX Design", "Analytics", "Programmatic"]

CGD_TEAM_CELL = "A2"
CGD_NAME_CELL = "F2"
CONTENT_COLUMN = "B"
CONTENT_RANGE = "B9:B33"

CGD_ROOTS = [9, 16, 23, 30]
CONTENT_GRID_LENGTH = 7

cgd_entry_template = read_template_contents("./templates/cgd-content-entry.html")
cgd_section_template = read_template_contents("./templates/cgd-section.html")


class CGDData:
    def __init__(self, title, description, url, content_url):
        """
        Initialize a CGD Data object.

        Parameters:
        title (str): The title of the article.
        description_url (str): The URL for the article description.
        content_url (str): The URL for the full content of the article.
        """
        self.title = title
        self.description = description
        self.url = url
        self.content_url = content_url

    def display(self):
        """
        Display the details of the data.
        """
        print("URL:", self.url)
        print("Content URL:", self.content_url)
        print("Title:", self.title)
        print("Description:", self.description)


def fetch_section_data(sheet_name, root_row_number):
    content_url = get_text_from_cell(sheet_name, f"{CONTENT_COLUMN}{root_row_number}")

    if not content_url or content_url == "":
        return None

    url = get_text_from_cell(sheet_name, f"{CONTENT_COLUMN}{root_row_number+1}")
    title = get_text_from_cell(sheet_name, f"{CONTENT_COLUMN}{root_row_number+2}")
    description = get_text_from_cell(sheet_name, f"{CONTENT_COLUMN}{root_row_number+3}")

    return CGDData(title, description, url, content_url)


def fetch_sections_data_for_team(team_name):
    data_list = []
    for root in CGD_ROOTS:
        data = fetch_section_data(sheet_name=team_name, root_row_number=root)
        if data:
            data_list.append(data)
    return data_list


def get_populated_cgd_content_sections(team):
    sections_content = ""
    cgd_data_list = fetch_sections_data_for_team(team)
    cgd_template = read_template_contents(
        "./templates/cgd-content-entry.html")
    for cgd_data in cgd_data_list:
        sections_content += replace_strings(cgd_template, [
            ("{{CGD-CONTENT-TITLE}}", cgd_data.title),
            ("{{CGD-CONTENT-DESCRIPTION}}", cgd_data.description),
            ("{{CGD-CONTENT-SHORTLINK}}", cgd_data.content_url),
            ("{{CGD-CONTENT-LINK}}", cgd_data.url),
        ])
    return sections_content


def get_populated_section(team):
    print(f"Populating CGD section for team: {team}")

    cgd_template = read_template_contents("./templates/cgd-section.html")

    team_name = get_text_from_cell(team, CGD_TEAM_CELL)
    cgd_name = get_text_from_cell(team, CGD_NAME_CELL)

    cgd_content_sections = get_populated_cgd_content_sections(team)
    cgd_section = replace_strings(cgd_template, [("{{CGD-CONTENT-SECTIONS}}", cgd_content_sections)])
    cgd_section = replace_strings(cgd_section, [("{{CGD_TEAM_NAME}}", team_name)])
    cgd_section = replace_strings(cgd_section, [("{{CGD-NAME}}", cgd_name)])
    
    return cgd_section



## Range implementation

def get_cgd_cell_ranges(teams):
    cell_ranges = []
    for team in teams:
        cell_ranges.append(f"{parse.quote(team)}!{CONTENT_RANGE}")
        cell_ranges.append(f"{parse.quote(team)}!{CGD_TEAM_CELL}")
        cell_ranges.append(f"{parse.quote(team)}!{CGD_NAME_CELL}")
    return cell_ranges


def filter_ranges(ranges, predicate):
    return [item for item in ranges if predicate in item.get("range")]


def extract_data_from_content(content_range):
    data_list = []
    range_values = content_range[0]["values"]
    data_length = ceil(len(range_values) / CONTENT_GRID_LENGTH)

    for i in range(data_length):
        cursor = CONTENT_GRID_LENGTH * i
        content_url = range_values[cursor][0]

        if not content_url or content_url == "":
            return None

        url = range_values[cursor+1][0]
        title = range_values[cursor+2][0]
        description = range_values[cursor+3][0]

        data_list.append(CGDData(title, description, url, content_url))

    return data_list


def extract_data_from_ranges(ranges):
    team = filter_ranges(ranges, CGD_TEAM_CELL)[0]["values"][0][0]
    name = filter_ranges(ranges, CGD_NAME_CELL)[0]["values"][0][0]
    data_list = extract_data_from_content(filter_ranges(ranges, CONTENT_RANGE))

    return team, name, data_list


def populate_entries(data_list):
    entries = ""
    for cgd_data in data_list:
        entries += replace_strings(cgd_entry_template, [
            ("{{CGD-CONTENT-TITLE}}", cgd_data.title),
            ("{{CGD-CONTENT-DESCRIPTION}}", cgd_data.description),
            ("{{CGD-CONTENT-SHORTLINK}}", cgd_data.content_url),
            ("{{CGD-CONTENT-LINK}}", cgd_data.url),
        ])
    return entries

def populate_section(team, name, data_list):
    cgd_section = cgd_section_template
    
    cgd_entries = populate_entries(data_list)
    cgd_section = replace_strings(cgd_section, [("{{CGD-CONTENT-SECTIONS}}", cgd_entries)])
    cgd_section = replace_strings(cgd_section, [("{{CGD_TEAM_NAME}}", team)])
    cgd_section = replace_strings(cgd_section, [("{{CGD-NAME}}", name)])
    
    return cgd_section


def get_cgd_sections(week):
    teams = A_TEAMS if week == "A" else B_TEAMS
    range_values = get_cell_ranges(get_cgd_cell_ranges(teams))
    
    cgd_sections = ""
    for team_name in teams:
        print(f"Populating CGD section for team: {team_name}")
        team_ranges = filter_ranges(range_values, team_name)
        team, name, data_list = extract_data_from_ranges(team_ranges)
        cgd_sections += populate_section(team, name, data_list)

    return cgd_sections
