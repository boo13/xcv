
def print_version() -> None:
    from xcv import __version__
    print(f"xcv version: {__version__}")

def print_info() -> None:
    from xcv import __version__, __doc__, __author__, __email__
    print(f"{__doc__}\nxcv version: {__version__}\nAuthor: {__author__}\nEmail: {__email__}\n")

def print_all_constants() -> None:
    from xcv.constants import(
        PACKAGE_NAME,
        XCV_VERSION,
        XCV_AUTHOR,
        XCV_EMAIL,
        XCV_DESCRIPTION,
        DEFAULT_PYTHON,
        HOME_PATH,
        XCV_HOME,
        WINDOWS,
        SERIAL_BAUD,
        SERIAL_PORT,
        WIN_DEFAULT_SERIAL_PORT,
        MAC_DEFAULT_SERIAL_PORT,
        TIMEZONE,
        ABSPATH,
    )
    print(f"""
            INFO
            Package Name: {PACKAGE_NAME}
            Version: {XCV_VERSION}
            Author: {XCV_AUTHOR}
            Email: {XCV_EMAIL}
            Description: {XCV_DESCRIPTION}
            
            SYSTEM
            Python: {DEFAULT_PYTHON}
            Home Path: {HOME_PATH}
            XCV Home: {XCV_HOME}
            Absolute Path: {ABSPATH}
            Windows Machine? {WINDOWS}

            SERIAL
            Serial Baud: {SERIAL_BAUD} 
            Windows Serial Port Default: {WIN_DEFAULT_SERIAL_PORT}
            Mac Serial Port Default: {MAC_DEFAULT_SERIAL_PORT}

            SETTINGS
            Timezone: {TIMEZONE}
            """)

if __name__ == "__main__":
    print_all_constants()