from utils import get_text_from_cell, read_template_contents, replace_strings


KEYWORDS_SHEET = "Keywords and Promo blokk"

TITLE_CELL = "C7"
DESCRIPTION_CELL = "D7"
LINK_CELL = "E7"

def get_populated_featured_content():
    print("Populating Featured content section")
    
    fc_template = read_template_contents("./templates/featured-content.html")

    title = get_text_from_cell(KEYWORDS_SHEET, TITLE_CELL)
    description = get_text_from_cell(KEYWORDS_SHEET, DESCRIPTION_CELL)
    link = get_text_from_cell(KEYWORDS_SHEET, LINK_CELL)

    fc_section = replace_strings(fc_template, [("{{FEATURED-CONTENT-TITLE}}", title)])
    fc_section = replace_strings(fc_section, [("{{FEATURED-CONTENT-DESCRIPTION}}", description)])
    fc_section = replace_strings(fc_section, [("{{FEATURED-CONTENT-LINK}}", link)])

    return fc_section
