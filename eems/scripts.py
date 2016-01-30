from ds18b20 import *
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Help Information for eems.',
                                     prog='eems',
                                     usage='eems <command> [options]')

    parser.add_argument('check',
                        help='Check sensor requirements.')
    parser.parse_args()

if __name__ == "__main__":
    main()
