#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import argparse
import tempfile
import subprocess

def get_message(editor=None):
    """Launch the editor with an empty file, returning its contents on exit.

    If this function encounters an error -- if the editor isn't found, or
    if no message is written -- then the function returns None.
    """
    if editor is None:
        editor = os.getenv('EDITOR', 'nano')
    with tempfile.NamedTemporaryFile() as f_in:
        f_in.close()
        try:
            subprocess.check_call([editor, f_in.name])
            with open(f_in.name) as f_out:
                return f_out.read()
        except IOError, subprocess.CalledProcessError:
            return None

def file_with_message(in_file, message=None):
    """Adds the given message to the given file, returning the result.

    This function always removes any message already there, so calling
    this without a message will clear any message already there.
    """
    # Load the input file and convert to lines.
    lines = in_file.readlines()
    in_file.close()

    # Create the binary data for the message
    if message is None: message = ''
    binary = (''.join(format(ord(x), 'b') for x in message))
    len_binary = len(binary)

    # Add the angst binary data.
    for i, line in enumerate(lines):
        lines[i] = line.rstrip() + (
            ' ' if i < len_binary and binary[i] == '1' else ''
            )

    # Combine the lines. TODO: using the same line ending as we found.
    result = '\n'.join(lines)
    return result

def get_out_fn(args):
    """Returns the output filename for the given input and suffix."""
    suffix = '.%s' % args.suffix if args.suffix else ''
    filename, ext = os.path.splitext(args.file.name)
    return ''.join([filename, suffix, ext])

def run_write_message(args, message=None):
    """Changes the message in the referenced file and writes it."""
    out_fn = get_out_fn(args)
    out_content = file_with_message(args.file, message)
    with open(out_fn, 'w') as f:
        f.write(out_content)

def run_add(args):
    message = get_message() if args.message is None else args.message
    if not message:
        sys.stderr.write(
            'No message to add, use `angst remove` to remove angst.'
            )
        sys.exit(-1)
    run_write_message(args, message)

def run_remove(args):
    run_write_message(args, message=None)

def run_read(args):
    print('Reading angst')

def _create_argument_parser():
    """Creates the argument parser."""
    # Arguments present in multiple commands.
    def _add_file_argument(subparser, help):
        subparser.add_argument(
            'file',
            type=argparse.FileType('r'),
            help=help
            )
    def _add_suffix_argument(subparser, default, help):
        subparser.add_argument(
            '-s', '--suffix',
            default=default, type=str,
            help=help
            )

    # Create the argument parser for all commands.
    parser = argparse.ArgumentParser(
        description='Adds a secret message to a source code file.'
        )
    subparsers = parser.add_subparsers()

    # angst add
    add_angst = subparsers.add_parser(
        'add', help='Adds angst to a file (removes any angst alread present).'
        )
    _add_file_argument(add_angst, "The file to add angst to.")
    _add_suffix_argument(
        add_angst, "angst",
        "A suffix to add to the angst file, to avoid overwriting the orignal."
        )
    add_angst.add_argument(
        "-m", "--message", default=None, type=str,
        help="The message to add as angst to the file."
        )
    add_angst.set_defaults(func=run_add)

    # angst remove
    remove_angst = subparsers.add_parser(
        'remove',
        help='Removes angst from a file (i.e. trims trailing whitespace).'
        )
    _add_file_argument(remove_angst, "The file to remove angst from.")
    _add_suffix_argument(
        remove_angst, "clean",
        "A suffix to add to the clean file, to avoid overwriting the angst.")
    remove_angst.set_defaults(func=run_remove)

    # angst read
    read_angst = subparsers.add_parser(
        'read', help='Reads the angst from a file.'
        )
    _add_file_argument(read_angst, "The file containing the angst to read.")
    read_angst.set_defaults(func=run_read)
    return parser

def main():
    parser = _create_argument_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
