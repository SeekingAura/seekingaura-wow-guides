import html

from docutils import nodes
from docutils.parsers.rst import (
    Directive,
    directives,
)


class WowTooltipDirective(Directive):
    """
    Based on https://www.wowhead.com/tooltips

    ..sourcecode:: html
       <a href="https://www.wowhead.com/item=25697" class="q3" \
data-wowhead="gems=23121&amp;ench=2647&amp;pcs=25695:25696:25697">\
Felstalker Bracers</a>

    Then with this directive is equivalent to

    .. sourcecode:: rst
        .. wowtooltip::
           https://www.wowhead.com/item=25697
           :name: Felstalker Bracers
           :q: rare
           :gems: 23121
           :ench: 2647, 2648
           :pcs: 25695, 25696, 25697
    """

    required_arguments = 1  # URL
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "name": directives.unchanged,
        "q": directives.unchanged,
        "gems": directives.unchanged,
        "ench": directives.unchanged,
        "pcs": directives.unchanged,
    }

    def run(self):
        url: str = self.arguments[0]

        name: str = self.options.get("name", url)
        q: str = self.options.get("q", "").lower().replace(" ", "_")

        # Build class="qX"
        class_attr = ""
        if q:
            q_map = {
                "poor": "q0",  # Poor
                "common": "q1",  # Common
                "uncommon": "q2",  # Uncommon
                "rare": "q3",  # Rare
                "epic": "q4",  # Epic
                "legendary": "q5",  # Legendary
                "artifact": "q6",  # Artifact
                "heirloom": "q7",  # Heirloom
                "wow_token": "q8",  # WoW Token
            }
            class_attr = q_map.get(q, "")

        # Build data-wowhead="..."
        params = []

        for key in ("gems", "ench", "pcs"):
            if key in self.options:
                # Convert "1, 2, 3" → "1:2:3"
                values = self.options[key].replace(",", ":").replace(" ", "")
                params.append(f"{key}={values}")

        data_attr = ""
        if params:
            joined = "&".join(params)
            data_attr = html.escape(joined, quote=True)

        # Build final HTML
        html_code = f'<a href="{url}"'
        if class_attr:
            html_code += f' class="{class_attr}"'
        if data_attr:
            html_code += f' data-wowhead="{data_attr}"'
        html_code += f">{name}</a>"

        return [nodes.raw("", html_code, format="html")]


def setup(app):
    app.add_directive("wowtooltip", WowTooltipDirective)
