from utils import read_template_contents, replace_strings, get_cell_ranges, rangify, check_filled

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "B7:E7"
SECTION_NAME = "Featured Content"


def get_populated_featured_content():
    print(f"Populating {SECTION_NAME} section")

    template = read_template_contents("./templates/featured-content.html")

    try:
        image_url, title, description, link = get_fc_data()
        check_filled(image_url, title, description, link)

        section = replace_strings(template, [
            ("{{FEATURED-CONTENT-IMAGE-URL}}", image_url),
            ("{{FEATURED-CONTENT-TITLE}}", title),
            ("{{FEATURED-CONTENT-DESCRIPTION}}", description),
            ("{{FEATURED-CONTENT-LINK}}", link)
        ])

        return section
    except Exception as e:
        if str(e) == "'values'" or str(e) == "Missing section data":
            print(f"WARNING: Skipping {SECTION_NAME} section population due to missing data in sheet")
        else:
            print(
                f"ERROR occurred while populating {SECTION_NAME} section: {e}")
        return ""


def get_fc_data():
    range_values = get_cell_ranges(
        [rangify(KEYWORDS_SHEET, CONTENT_RANGE)])[0]["values"]

    cells = range_values[0]
    image_url = cells[0]
    title = cells[1]
    description = cells[2]
    link = "#" if len(cells) <= 3 else cells[3]

    return image_url, title, description, link
