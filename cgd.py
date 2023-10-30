from utils import read_template_contents, replace_strings, get_cell_ranges, rangify
from math import ceil

A_TEAMS = ["Creative", "Strategy", "UX Design", "Digital Media", "Development"]
B_TEAMS = ["Graphic Design and UI", "Social Media", "Business & Tech", "Analytics and Insights", "SEO and Performance Content"]

HEADER_RANGE = "A2:H2"
CONTENT_RANGE = "B9:B33"

PROFILE_PICTURE_SHEET = "profilképek"
PROFILE_PICTURE_RANGE = "A2:B200"

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


## Range implementation

def get_cgd_cell_ranges(teams):
    cell_ranges = []
    cell_ranges.append(rangify(PROFILE_PICTURE_SHEET, PROFILE_PICTURE_RANGE))
    for team in teams:
        cell_ranges.append(rangify(team, CONTENT_RANGE))
        cell_ranges.append(rangify(team, HEADER_RANGE))
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


def extract_header_data(header_range):
    range_values = header_range[0]["values"][0]
    team = range_values[0]
    name = range_values[5]
    url = range_values[7] if len(range_values) > 7 else ""
    banner_image_url = url if "http" in url else ""

    return team, name, banner_image_url


def extract_data_from_ranges(ranges):
    team, name, banner_image_url = extract_header_data(filter_ranges(ranges, HEADER_RANGE))
    data_list = extract_data_from_content(filter_ranges(ranges, CONTENT_RANGE))

    return team, name, banner_image_url, data_list


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


def fetch_profile_url_by_name(range_values, name):
    profile_values = filter_ranges(range_values, PROFILE_PICTURE_SHEET)[0]["values"]
    return [item[1] for item in profile_values if name in item[0]][0]


def populate_section(team, name, banner_image_url, profile_image_url, data_list):
    cgd_section = replace_strings(cgd_section_template, [
        ("{{CGD-CONTENT-SECTIONS}}", populate_entries(data_list)),
        ("{{CGD_TEAM_NAME}}", team),
        ("{{CGD-NAME}}", name),
        ("{{CGD-REP-IMAGE-URL}}", profile_image_url),
        ("{{CGD-BANNER-IMAGE-URL}}", banner_image_url),
        ("'{{CGD-BANNER-DISPLAY}}'", "block" if banner_image_url != "" else "none"),
    ])

    return cgd_section


def get_cgd_sections(week):
    teams = A_TEAMS if week == "A" else B_TEAMS
    range_values = get_cell_ranges(get_cgd_cell_ranges(teams))

    cgd_sections = ""
    for team_name in teams:
        print(f"Populating CGD section for team: {team_name}")
        team_ranges = filter_ranges(range_values, team_name)
        team, name, banner_image_url, data_list = extract_data_from_ranges(team_ranges)
        
        profile_image_url = fetch_profile_url_by_name(range_values, name)
        cgd_sections += populate_section(team, name, banner_image_url, profile_image_url, data_list)

    return cgd_sections
