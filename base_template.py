from utils import read_template_contents, replace_strings, fetch_cell_range_values
from datetime import datetime

KEYWORDS_SHEET = "Keywords and Promo blokk"
ISSUE_RANGE = "B5:C5"


def get_populated_base_template():
    print("Populating base newsletter template")

    template = read_template_contents("./templates/mail.html")

    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_year = current_datetime.year
    full_date = current_datetime.strftime(' %d %B %Y').replace(' 0', ' ')

    issue_number, keywords = get_data()
    template = replace_strings(template, [
        ("{{ISSUE}}", str(issue_number)),
        ("{{SUBJECT}}", keywords),
        ("{{MONTH}}", str(current_month)),
        ("{{DATE}}", str(current_year)),
        ("{{FULL-DATE}}", full_date),
        
        # View in browser URL
        ("{{URL}}", "https://www.mailjet.com/"),
        
        # Feedback
        ("{{POSITIVE-FEEDBACK-LINK}}", "https://mito.us7.list-manage.com/track/click?u=2efacdbf6db4d3dc8d6ab63bb&amp;id=e497d15b80&amp;e=9a7cdb3223"),
        ("{{NEGATIVE-FEEDBACK-LINK}}", "https://mito.us7.list-manage.com/track/click?u=2efacdbf6db4d3dc8d6ab63bb&amp;id=eb26a1d782&amp;e=9a7cdb3223"),
        
        # Share
        ("{{SHARE-LINK}}", "https://mito.us7.list-manage.com/track/click?u=2efacdbf6db4d3dc8d6ab63bb&id=f6232968c8&e=9a7cdb3223"),
    ])

    return template


def get_data():
    range_values = fetch_cell_range_values([ISSUE_RANGE])[0]["values"]

    issue_number = range_values[0][0]
    keywords = range_values[0][1]

    return issue_number, keywords
