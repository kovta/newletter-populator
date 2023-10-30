import sys
from datetime import datetime
from utils import replace_strings, write_to_file

from base_template import get_populated_base_template
from featured_content import get_populated_featured_content
from cgd import get_cgd_sections
from highlighted_job import get_populated_highlighted_job
from community import get_populated_community_box


def populate(week_id):
    template = get_populated_base_template()
    newsletter = replace_strings(template, [
        ("{{FEATURED-CONTENT-SECTION}}", get_populated_featured_content()),
        ("{{CGD-SECTIONS}}", get_cgd_sections(week_id)),
        ("{{HIGHLIGHTED-JOB-SECTION}}", get_populated_highlighted_job()),
        ("{{COMMUNITY-BOX-SECTION}}", get_populated_community_box())
    ])

    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime('%Y%m%d-%H%M%S')
    write_to_file(f'./output/{current_datetime_string}.html', newsletter)


if __name__ == "__main__":
    populate("B")

    ## For running locally:
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <week_argument>")
    # else:
    #     week = sys.argv[1]
    #     if week == "week_a":
    #         populate("A")
    #     elif week == "week_b":
    #         populate("B")