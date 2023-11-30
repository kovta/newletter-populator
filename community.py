from utils import read_template_contents, replace_strings, fetch_cell_range_values, rangify, check_filled

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "B11:E11"
SECTION_NAME = "Community Box"


def get_populated_community_box():
    print(f"Populating {SECTION_NAME} section")

    template = read_template_contents("./templates/community-box.html")

    try:
        image_url, title, description, link = get_data()
        check_filled(image_url, title, description, link)

        section = replace_strings(template, [
            ("{{COMMUNITY-IMAGE-URL}}", image_url),
            ("{{COMMUNITY-CONTENT}}", title),
            ("{{COMMUNITY-LINK-DESCRIPTION}}", description),
            ("{{COMMUNITY-LINK}}", link)
        ])

        return section
    except Exception as e:
        if str(e) == "'values'" or str(e) == "Missing section data":
            print(f"WARNING: Skipping {SECTION_NAME} section population due to missing data in sheet")
        else:
            print(
                f"ERROR occurred while populating {SECTION_NAME} section: {e}")
        return ""


def get_data():
    range_values = fetch_cell_range_values(
        [rangify(KEYWORDS_SHEET, CONTENT_RANGE)])[0]["values"]

    image_url = range_values[0][0]
    title = range_values[0][1]
    description = range_values[0][2]
    link = range_values[0][3]

    return image_url, title, description, link
