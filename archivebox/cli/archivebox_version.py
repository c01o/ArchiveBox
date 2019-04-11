#!/usr/bin/env python3

__package__ = 'archivebox.cli'
__command__ = 'archivebox version'
__description__ = 'Print the ArchiveBox version and dependency information'

import os
import re
import sys
import argparse

from ..legacy.util import reject_stdin
from ..legacy.config import (
    ANSI,
    VERSION,
    FOLDERS,
    DEPENDENCIES,
    check_dependencies,
)


def main(args=None):
    args = sys.argv[1:] if args is None else args

    parser = argparse.ArgumentParser(
        prog=__command__,
        description=__description__,
        add_help=True,
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only print ArchiveBox version number and nothing else.',
    )
    command = parser.parse_args(args)
    reject_stdin(__command__)
    
    if command.quiet:
        print(VERSION)
    else:
        print('ArchiveBox v{}'.format(VERSION))
        print()

        print('{white}[i] Dependency versions:{reset}'.format(**ANSI))
        for name, dependency in DEPENDENCIES.items():
            print_dependency_version(name, dependency)
        print()
        print('{white}[i] Folder locations:{reset}'.format(**ANSI))
        for name, folder in FOLDERS.items():
            print_folder_status(name, folder)

        print()
        check_dependencies()


def print_folder_status(name, folder):
    if folder['enabled']:
        if folder['is_valid']:
            color, symbol, note = 'green', '√', 'valid'
        else:
            color, symbol, note, num_files = 'red', 'X', 'invalid', '?'
    else:
        color, symbol, note, num_files = 'lightyellow', '-', 'disabled', '-'

    if folder['path']:
        if os.path.exists(folder['path']):
            num_files = (
                f'{len(os.listdir(folder["path"]))} files'
                if os.path.isdir(folder['path']) else
                'exists'
            )
        else:
            num_files = '?'

    print(
        ANSI[color],
        symbol,
        ANSI['reset'],
        name.ljust(24),
        (folder["path"] or '').ljust(70),
        num_files.ljust(14),
        ANSI[color],
        note,
        ANSI['reset'],
    )


def print_dependency_version(name, dependency):
    if dependency['enabled']:
        if dependency['is_valid']:
            color, symbol, note = 'green', '√', 'valid'
            version = 'v' + re.search(r'[\d\.]+', dependency['version'])[0]
        else:
            color, symbol, note, version = 'red', 'X', 'invalid', '?'
    else:
        color, symbol, note, version = 'lightyellow', '-', 'disabled', '-'

    print(
        ANSI[color],
        symbol,
        ANSI['reset'],
        name.ljust(24),
        (dependency["path"] or '').ljust(70),
        version.ljust(14),
        ANSI[color],
        note,
        ANSI['reset'],
    )


if __name__ == '__main__':
    main()
