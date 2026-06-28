"""
report.py

Generate HTML reports using Jinja2.
"""

import logging
from pathlib import Path

from jinja2 import Environment
from jinja2 import FileSystemLoader

logger = logging.getLogger(__name__)


def generate_html_report(
    statistics: dict,
    validation_summary: dict,
    map_filename: str,
    output_file: str,
) -> None:
    """
    Generate an HTML report using Jinja2.
    """

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "report_template.html"
    )

    html = template.render(
        statistics=statistics,
        validation=validation_summary,
        map_filename=map_filename,
    )

    output_path = Path(output_file)

    output_path.write_text(
        html,
        encoding="utf-8",
    )

    logger.info(
        "Report generated successfully: %s",
        output_path,
    )