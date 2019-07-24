import os
import sys
from pathlib import Path

DEFAULT_PYTHON = sys.executable

SERIAL_BAUD = 115200
SERIAL_PORT = "/dev/cu.usbmodem51875801"

# DEFAULT_PIPX_HOME = Path.home() / ".local/pipx"
# DEFAULT_PIPX_BIN_DIR = Path.home() / ".local/bin"
# PIPX_HOME = Path(os.environ.get("PIPX_HOME", DEFAULT_PIPX_HOME)).resolve()
# PIPX_LOCAL_VENVS = PIPX_HOME / "venvs"
# LOCAL_BIN_DIR = Path(os.environ.get("PIPX_BIN_DIR", DEFAULT_PIPX_BIN_DIR)).resolve()
# PIPX_VENV_CACHEDIR = PIPX_HOME / ".cache"
# PIPX_PACKAGE_NAME = "pipx"
# TEMP_VENV_EXPIRATION_THRESHOLD_DAYS = 14

SPEC_HELP = textwrap.dedent(
    """The package name or specific installation source passed to pip.
    Runs `pip install -U SPEC`.
    For example `--spec mypackage==2.0.0` or `--spec  git+https://github.com/user/repo.git@branch`
    """
)
PIPX_DESCRIPTION = textwrap.dedent(
    f"""
Install and execute binaries from Python packages.
Binaries can either be installed globally into isolated Virtual Environments
or run directly in an temporary Virtual Environment.
Virtual Environment location is {str(PIPX_LOCAL_VENVS)}.
Symlinks to binaries are placed in {str(LOCAL_BIN_DIR)}.
These locations can be overridden with the environment variables
PIPX_HOME and PIPX_BIN_DIR, respectively. (Virtual Environments will
be installed to $PIPX_HOME/venvs)
"""
)

INSTALL_DESCRIPTION = f"""
The install command is the preferred way to globally install binaries
from python packages on your system. It creates an isolated virtual
environment for the package, then ensures the package's binaries are
accessible on your $PATH.
The result: binaries you can run from anywhere, located in packages
you can cleanly upgrade or uninstall. Guaranteed to not have
dependency version conflicts or interfere with your OS's python
packages. 'sudo' is not required to do this.
pipx install PACKAGE
pipx install --python PYTHON PACKAGE
pipx install --spec VCS_URL PACKAGE
pipx install --spec ZIP_FILE PACKAGE
pipx install --spec TAR_GZ_FILE PACKAGE
The argument to `--spec` is passed directly to `pip install`.
The default virtual environment location is {DEFAULT_PIPX_HOME}
and can be overridden by setting the environment variable `PIPX_HOME`
 (Virtual Environments will be installed to `$PIPX_HOME/venvs`).
The default binary location is {DEFAULT_PIPX_BIN_DIR} and can be
overridden by setting the environment variable `PIPX_BIN_DIR`.
"""