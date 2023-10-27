from utils import read_template_contents, replace_strings, get_cell_ranges, rangify

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "B7:E7"


def get_populated_featured_content():
    print("Populating Featured Content section")

    template = read_template_contents("./templates/featured-content.html")

    image_url, title, description, link = get_fc_data()
    section = replace_strings(template, [
        ("{{FEATURED-CONTENT-IMAGE-URL}}", image_url),
        ("{{FEATURED-CONTENT-TITLE}}", title),
        ("{{FEATURED-CONTENT-DESCRIPTION}}", description),
        ("{{FEATURED-CONTENT-LINK}}", link)
    ])

    return section


def get_fc_data():
    range_values = get_cell_ranges([rangify(KEYWORDS_SHEET, CONTENT_RANGE)])[0]["values"]

    cells = range_values[0]
    image_url = cells[0]
    title = cells[1]
    description = cells[2]
    link = "#" if len(cells) <= 3 else cells[3]

    return image_url, title, description, link
