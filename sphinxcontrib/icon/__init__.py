"""Icon extention to embed icon in sphinx outputs."""

from typing import Any, Dict

from sphinx.application import Sphinx

from .font_handler import Fontawesome
from .icon import _NODE_VISITORS, Icon, icon_node

__version__ = "0.2.2"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


def setup(app: Sphinx) -> Dict[str, Any]:
    """Add icon node to the sphinx builder."""
    # load the icon node/role
    app.add_node(icon_node, **_NODE_VISITORS)  # type: ignore
    app.add_role("icon", Icon())

    # load the font
    font_handler = Fontawesome()

    # install html related files
    app.add_css_file(str(font_handler.css_file.resolve()))
    app.add_js_file(str(font_handler.js_file.resolve()))

    # install latex files
    app.add_latex_package("fontspec")
    app.connect("config-inited", font_handler.add_latex_font)
    app.connect("config-inited", font_handler.enforce_xelatex)
    app.connect("builder-inited", font_handler.add_latex_font_files)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
