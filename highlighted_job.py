from utils import read_template_contents, replace_strings, get_cell_ranges, rangify, check_filled

KEYWORDS_SHEET = "Keywords and Promo blokk"
CONTENT_RANGE = "B9:F9"
SECTION_NAME = "Highlighted Job"


def get_populated_highlighted_job():
    print(f"Populating {SECTION_NAME} section")

    template = read_template_contents("./templates/highlighted-job.html")

    try:
        image_url, title, description, description_link, link = get_data()
        check_filled(image_url, title, description, description_link, link)

        section = replace_strings(template, [
            ("{{HIGHLIGHTED-JOB-IMAGE-URL}}", image_url),
            ("{{HIGHLIGHTED-JOB-TITLE}}", title),
            ("{{HIGHLIGHTED-JOB-DESCRIPTION}}", description),
            ("{{HIGHLIGHTED-JOB-LINK-DESCRIPTION}}", description_link),
            ("{{HIGHLIGHTED-JOB-LINK}}", link)
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
    range_values = get_cell_ranges(
        [rangify(KEYWORDS_SHEET, CONTENT_RANGE)])[0]["values"]

    image_url = range_values[0][0]
    title = range_values[0][1]
    description = range_values[0][2]
    description_link = range_values[0][3]
    link = range_values[0][4]

    return image_url, title, description, description_link, link
