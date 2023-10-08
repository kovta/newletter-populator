from utils import read_template_contents, replace_strings, get_cell_ranges

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "C7:E7"


def get_populated_featured_content():
    print("Populating Featured Content section")

    template = read_template_contents("./templates/featured-content.html")

    title, description, link = get_fc_data()
    section = replace_strings(template, [
        ("{{FEATURED-CONTENT-TITLE}}", title),
        ("{{FEATURED-CONTENT-DESCRIPTION}}", description),
        ("{{FEATURED-CONTENT-LINK}}", link)
    ])

    return section


def get_fc_data():
    range_values = get_cell_ranges([CONTENT_RANGE])[0]["values"]

    title = range_values[0][0]
    description = range_values[0][1]
    link = range_values[0][2]

    return title, description, link
