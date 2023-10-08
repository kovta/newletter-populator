from utils import get_text_from_cell, read_template_contents, replace_strings


KEYWORDS_SHEET = "Keywords and Promo blokk"

TITLE_CELL = "C7"
DESCRIPTION_CELL = "D7"
LINK_CELL = "E7"


class FCData:
    def __init__(self, title, description, link):
        """
        Initialize an Article object.

        Parameters:
        title (str): The title of the article.
        description_url (str): The URL for the article description.
        content_url (str): The URL for the full content of the article.
        """
        self.title = title
        self.description = description
        self.link = link

    def display(self):
        """
        Display the details of the data.
        """
        print("Link:", self.link)
        print("Title:", self.title)
        print("Description:", self.description)


def get_populated_featured_content():
    print("Populating Featured content section")

    fc_template = read_template_contents("./templates/featured-content.html")

    title = get_text_from_cell(KEYWORDS_SHEET, TITLE_CELL)
    description = get_text_from_cell(KEYWORDS_SHEET, DESCRIPTION_CELL)
    link = get_text_from_cell(KEYWORDS_SHEET, LINK_CELL)

    fc_section = replace_strings(
        fc_template, [("{{FEATURED-CONTENT-TITLE}}", title)])
    fc_section = replace_strings(
        fc_section, [("{{FEATURED-CONTENT-DESCRIPTION}}", description)])
    fc_section = replace_strings(
        fc_section, [("{{FEATURED-CONTENT-LINK}}", link)])

    return fc_section


def get_fc_cell_ranges():
    return [f"{KEYWORDS_SHEET}!{TITLE_CELL}",
            f"{KEYWORDS_SHEET}!{DESCRIPTION_CELL}",
            f"{KEYWORDS_SHEET}!{LINK_CELL}"]
