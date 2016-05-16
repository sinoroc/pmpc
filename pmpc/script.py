""" Script
"""


import argparse
import logging

from . import i18n
from . import pmpc


_ = i18n.translate

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 6600


def run(host, port):
    """ Initialize and start the application.
    """
    logging.basicConfig(level=logging.WARNING)
    the_pmpc = pmpc.Pmpc('pmpc', host, port)
    the_pmpc.start()
    the_pmpc.run_ui_task()
    the_pmpc.join()
    return None


def main():
    """ Parse arguments and start application.
    """
    parser = argparse.ArgumentParser(description=_("Pmpc"))
    parser.add_argument('host', type=str, nargs='?', default=DEFAULT_HOST)
    parser.add_argument('port', type=int, nargs='?', default=DEFAULT_PORT)
    args = parser.parse_args()
    run(args.host, args.port)
    return None


if __name__ == '__main__':
    main()


# EOF
