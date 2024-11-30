import platform
from pathlib import Path

from pynpm import NPMPackage
from setuptools import Command, setup
from setuptools.command.egg_info import egg_info

ROOT = Path(__file__).parent

# create a global variable to check if we are on windows
# to pilot the shell option to run the tests
is_windows = platform.system() == "Windows"


def update_package_data(distribution) -> None:
    """Update package_data to catch changes during setup."""
    distribution.get_command_obj("build_py").finalize_options()


def js_prerelease(command: Command, strict: bool = False) -> Command:
    """Decorator for building minified js/css prior to another command."""

    class DecoratedCommand(command):
        """Decorated command to install jsdeps first."""

        def run(self) -> None:
            """Run the command."""
            package = ROOT / "sphinxcontrib" / "icon" / "package.json"
            NPMPackage(package.resolve(), shell=is_windows).install()
            update_package_data(self.distribution)
            command.run(self)

    return DecoratedCommand


setup(cmdclass={"egg_info": js_prerelease(egg_info)})
