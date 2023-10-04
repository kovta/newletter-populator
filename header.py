from utils import get_text_from_cell, read_template_contents, replace_strings


KEYWORDS_SHEET = "Keywords and Promo blokk"
ISSUE_CELL = "B5"
TITLE_CELL = "C7"
DESCRIPTION_CELL = "D7"

def get_populated_header():
    return get_text_from_cell(KEYWORDS_SHEET, ISSUE_CELL)
    print()

def get_issue_number():
    return get_text_from_cell(KEYWORDS_SHEET, ISSUE_CELL)