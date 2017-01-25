#!/usr/bin/env python

"""The stix-elevator is a work-in-progress. It should be used to explore how
existing STIX 1.x would potentially be represented in STIX 2.0. Using the
current version of the elevator will provide insight to issues that might need
to be mitigated to convert your STIX 1.x content.
"""

import argparse
import textwrap

from elevator import elevate_file
from elevator.options import initialize_options
from elevator.version import __version__


CODE_TABLE = """
The following table shows all elevator messages. Use the associate code number
to --enable or --disable a message. By default, the elevator displays all
messages. Note: disabling the message does not disable the functionality.

Refer to elevator_log_messages.xlsx for error codes.
"""


class NewlinesHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom help formatter to insert newlines between argument help texts.
    """
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        txt = textwrap.wrap(text, width)
        txt[-1] += '\n'
        return txt


def _get_arg_parser(is_script=True):
    """Create and return an ArgumentParser for this application."""

    desc = "stix-elevator v{0}\n\n".format(__version__)

    parser = argparse.ArgumentParser(
        description=desc + __doc__,
        formatter_class=NewlinesHelpFormatter,
        epilog=CODE_TABLE
    )

    if is_script:
        parser.add_argument(
            "file_",
            help="The input STIX document to be elevated.",
            metavar="file"
        )

    parser.add_argument(
        "--incidents",
        help="Incidents will be included in the conversion.",
        dest="incidents",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--no-squirrel-gaps",
        help="Do not include STIX 1.x content that cannot be represented "
             "directly in STIX 2.0 using the description property.",
        dest="no_squirrel_gaps",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--infrastructure",
        help="Infrastructure will be included in the conversion.",
        dest="infrastructure",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "--package-created-by-id",
        help="Use provided identifier for \"created_by_ref\" properties. \n\n"
             "Example: --package-created-by-id \"identity--1234abcd-1a12-12a3-0ab4-1234abcd5678\"",
        dest="package_created_by_id",
        action="store",
        default=None
    )

    parser.add_argument(
        "--default-timestamp",
        help="Use provided timestamp for properties that require a timestamp. "
             "\n\nExample: --default-timestamp \"2016-11-15T13:10:35.053000Z\"",
        dest="default_timestamp",
        action="store",
        default=None
    )

    parser.add_argument(
        "--validator-args",
        help="Arguments to pass stix-validator. Default: --strict-types",
        dest="validator_args",
        action="store",
        default="--strict-types"
    )

    parser.add_argument(
        "-v"
        "--verbose",
        help="Print information messages and more verbose error messages.",
        dest="verbose",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "-e",
        "--enable",
        help="A comma-separated list of the elevator messages to enable. "
             "If the --disable option is not used, no other messages will be "
             "shown. \n\nExample: --enable 250",
        dest="enable",
        default=""
    )

    parser.add_argument(
        "-d",
        "--disable",
        help="A comma-separated list of the elevator messages to disable. \n\n"
             "Example: --disable 212,220",
        dest="disable",
        default=""
    )

    parser.add_argument(
        "-s",
        "--silent",
        help="If this flag is set. All elevator messages will be disabled.",
        dest="silent",
        action="store_true",
        default=False
    )

    return parser


def main():
    # Parse stix-elevator command-line args
    elevator_parser = _get_arg_parser()
    elevator_args = elevator_parser.parse_args()

    initialize_options(elevator_args)
    print(elevate_file(elevator_args.file_))


if __name__ == '__main__':
    main()