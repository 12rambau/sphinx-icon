"""Handler to install the fontawesome resources in the build."""

from pathlib import Path
from textwrap import dedent

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging
from sphinx.util.osutil import copyfile, ensuredir
from yaml import safe_load

HERE = Path(__file__).parent

logger = logging.getLogger(__name__)


class Fontawesome:
    """All the parameter related to Fontawesome grouped in a singleton class."""

    fa_dir = HERE / "node_modules" / "@fortawesome" / "fontawesome-free"
    regex = "^(?P<font>fa[\\w-]*) fa-(?P<glyph>[\\w-]+)$"
    metadata = safe_load((fa_dir / "metadata" / "icons.yml").read_text())
    css_file = fa_dir / "css" / "all.min.css"
    js_file = fa_dir / "js" / "all.min.js"
    webfont_folder = fa_dir / "webfonts"
    fonts = {
        "fa": "fa-solid",
        "fas": "fa-solid",
        "far": "fa-regular",
        "fab": "fa-brands",
        "fa-solid": "fa-solid",
        "fa-regular": "fa-regular",
        "fa-brands": "fa-brands",
    }
    deprecated_fonts = ["fa", "fas", "far", "fab"]

    def add_latex_font_files(self, app: Sphinx) -> None:
        """Copy the fontawesome files to the build repository for latex build."""
        if app.builder.name != "latex":
            return

        for f in self.webfont_folder.glob("*.ttf"):
            dst = Path(app.builder.outdir) / f.name
            logger.info(f"Writing: {f.name}")
            ensuredir(app.builder.outdir)
            copyfile(f.resolve(), dst.resolve())

    def add_latex_font(self, app: Sphinx, config: Config) -> None:
        """Add the fontawesome fontfamily in the preamble of the .tex file."""
        if "preamble" not in config.latex_elements:
            config.latex_elements["preamble"] = ""

        config.latex_elements["preamble"] += dedent(
            r"""
        \newfontfamily{\fasolid}{fa-solid-900.ttf}
        \newfontfamily{\faregular}{fa-regular-400.ttf}
        \newfontfamily{\fabrands}{fa-brands-400.ttf}
        """
        )

    def enforce_xelatex(self, app: Sphinx, config: Config) -> None:
        """Force the builder to use the XeLaTex builder instead of vanilla Latex.

        Compulsory to access the fontspec package
        """
        config.latex_engine = "xelatex"  # type: ignore

    @classmethod
    def search_alias(cls, icon_name: str) -> str:
        """Search for the text in the potential aliases of fontawesome.

        This method should only be called after checking the name against metadata to avoid
        calling it for each icon.

        Args:
            icon_name: the name of the icon to search for. it should not be a label

        Returns:
            the name of the icon, empty string if not found
        """
        latest_name = ""
        for label, meta in cls.metadata.items():
            aliases = meta.get("aliases", {}).get("names", [])
            if icon_name in aliases:
                latest_name = label
                break

        return latest_name
