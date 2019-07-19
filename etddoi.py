#! /usr/bin/env python
"""Run in same working directory as files. See README.md for usage examples."""
from argparse import ArgumentParser
import sys
from doiparse import doiparse
from csvparse import csvparse
from mintdoi import mintdoi


def main():
    """main operation of script."""
    parser = ArgumentParser(usage='%(prog)s [options] ecommonsMetadata.csv')
    parser.add_argument("-d", "--date", dest="date",
                        help="Date on or after that an ETD was published for \
                        creating DOIs. Put in format YYYY-MM")
    parser.add_argument("-u", "--username", dest="username",
                        help="EZID creation username")
    parser.add_argument("-p", "--password", dest="password",
                        help="EZID creation password.")
    parser.add_argument("-s", "--address", dest="server",
                        default="https://ez.test.datacite.org",
                        help="Server defaults to https://ez.test.datacite.org for test. Set server to https://ez.datacite.org for production")
    
    parser.add_argument("datafile", help="eCommons metadata worked from.")

    args = parser.parse_args()

    if not len(sys.argv) > 0:
        parser.print_help()
        parser.exit()

    workingdir = csvparse(args.datafile, args.date)
    output = doiparse(workingdir)
    mintdoi(output, workingdir, args)


if __name__ == '__main__':
    # eventually add tests?
    main()
