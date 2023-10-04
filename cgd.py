from utils import get_text_from_cell, read_template_contents, replace_strings

A_TEAMS = ["Creative", "Strategy", "UX Design", "PPC", "Development"]
B_TEAMS = ["Graphic Design", "Business & Tech", "UX Design", "Analytics", "Programmatic"]

CGD_TEAM_CELL = "A2"
CGD_NAME_CELL = "F2"
CONTENT_COLUMN = "B"

CGD_ROOTS = [9, 16, 23, 30]


class CGDData:
    def __init__(self, title, description, url, content_url):
        """
        Initialize an Article object.

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
