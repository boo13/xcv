"""The implementation of xcv commands"""

from xcv.tools.print_sysinfo import print_version, print_info, print_all_constants


class XcvError(Exception):
    pass


if __name__ == "__main__":
    print_all_constants()
