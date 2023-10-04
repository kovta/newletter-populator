from utils import replace_strings, read_template_contents, write_to_file
from datetime import datetime

from cgd import get_populated_section, A_TEAMS
from featured_content import get_populated_featured_content


def populate():
    mail_template = read_template_contents("./templates/mail.html")
    newsletter = mail_template

    featured_content = get_populated_featured_content()
    newsletter = replace_strings(newsletter, [("{{FEATURED-CONTENT-SECTION}}", featured_content)])
    
    cgd_sections = ""
    for team in A_TEAMS:
        cgd_sections += get_populated_section(team)
    newsletter = replace_strings(newsletter, [("{{CGD-SECTIONS}}", cgd_sections)])

    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime('%Y%m%d-%H%M%S')
    write_to_file(f'./output/{current_datetime_string}.html', newsletter)
    

populate()
