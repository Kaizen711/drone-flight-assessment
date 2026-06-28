"""
report.py

Generate HTML reports using Jinja2 templates.
"""

import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)


def generate_html_report(
    statistics: dict,
    validation_summary: dict,
    map_file: str,
    output_file: str,
) -> None:
    """
    Generate the HTML report.
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
        map_file=Path(map_file).name,
    )

    Path(output_file).write_text(
        html,
        encoding="utf-8",
    )

    logger.info(
        "HTML report generated successfully."
    )