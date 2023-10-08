from utils import read_template_contents, replace_strings, get_cell_ranges

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "C11:E11"


def get_populated_community_box():
    print("Populating Community Box section")

    template = read_template_contents("./templates/community-box.html")

    title, description, link = get_data()
    section = replace_strings(template, [
        ("{{COMMUNITY-CONTENT}}", title),
        ("{{COMMUNITY-LINK-DESCRIPTION}}", description),
        ("{{COMMUNITY-LINK}}", link)
    ])

    return section


def get_data():
    range_values = get_cell_ranges([CONTENT_RANGE])[0]["values"]

    title = range_values[0][0]
    description = range_values[0][1]
    link = range_values[0][2]

    return title, description, link
