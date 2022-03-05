import os
import argparse
from .sphistoricparser import sphistoric_parser


def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("Parser")

    general.add_argument(
        '-s', '--host',
        dest='host',
        default='localhost',
        help="MySQL hosted address"
    )

    general.add_argument(
        '-u', '--username',
        dest='username',
        default='root',
        help="MySQL db user name"
    )

    general.add_argument(
        '-p', '--password',
        dest='password',
        default='123456',
        help="MySQL db password"
    )

    general.add_argument(
        '-d', '--projectid',
        dest='projectid',
        help="project id"
    )

    general.add_argument(
        '-o', '--output',
        dest='output',
        help="Name of csv file"
    )

    general.add_argument(
        '-g', '--ignoreresult',
        dest='ignoreresult',
        default="False",
        help="Flag to ignore execution result, by this flag we can restrict storing results into mysql"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_options()
    sphistoric_parser(args)