from utils import read_template_contents, replace_strings, get_cell_ranges, rangify

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "B11:E11"


def get_populated_community_box():
    print("Populating Community Box section")

    template = read_template_contents("./templates/community-box.html")

    image_url, title, description, link = get_data()
    section = replace_strings(template, [
        ("{{COMMUNITY-IMAGE-URL}}", image_url),
        ("{{COMMUNITY-CONTENT}}", title),
        ("{{COMMUNITY-LINK-DESCRIPTION}}", description),
        ("{{COMMUNITY-LINK}}", link)
    ])

    return section


def get_data():
    range_values = get_cell_ranges([rangify(KEYWORDS_SHEET, CONTENT_RANGE)])[0]["values"]

    image_url = range_values[0][0]
    title = range_values[0][1]
    description = range_values[0][2]
    link = range_values[0][3]

    return image_url, title, description, link
