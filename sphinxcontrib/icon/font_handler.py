from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from pathlib import Path
from shutil import rmtree
from yaml import safe_load


class Fontawesome:

    FONT_VERSION = "5.15.4"
    ASSET = "https://github.com/FortAwesome/Font-Awesome/releases/download/{version}/fontawesome-free-{version}-{type}.zip"
    TYPES = {"html": "web", "latex": "desktop"}

    icons_metadata = None
    dir = None

    def download_asset(self, format, path):

        type = self.TYPES[format]
        asset = self.ASSET.format(version=self.FONT_VERSION, type=type)

        self.dir = path / "fontawesome"
        self.dir.mkdir(exist_ok=True)
        rmtree(self.dir)

        # read the zip
        resp = urlopen(asset)
        zip_file = ZipFile(BytesIO(resp.read()))
        for file in zip_file.namelist():

            if Path(file).suffix == "":
                continue

            # get the data
            data = zip_file.read(file)

            # create the appropriate folder if needed
            src_name = Path(file).name
            src_dir = Path(*Path(file).parts[1:-1])
            dst_dir = self.dir / src_dir
            dst_dir.mkdir(exist_ok=True, parents=True)
            dts_file = dst_dir / src_name
            dts_file.write_bytes(data)

        # set the fontawsome metadata variable
        # it should be read only once
        with (self.dir / "metadata/icons.yml").open("r") as f:
            self.icons_metadata = safe_load(f)

        return

    def get_css(self):

        return str(self.dir / "css/all.min.css")

    def get_js(self):

        return str(self.dir / "js/all.min.js")
