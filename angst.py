#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
import argparse
import tempfile
import subprocess
import re
import warnings

newline_re = re.compile(r'([\n\t]+)$')
ending_re = re.compile(r'( +)([\n\t]+)$')

bits_per_char = 7
binary_format = '{:0%db}' % bits_per_char

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
        except (IOError, subprocess.CalledProcessError):
            return None

def file_with_message(in_file, message=None):
    """Adds the given message to the given file, returning the result.

    This function always removes any message already there, so calling
    this without a message will clear any message already there.
    """
    # Create the binary data for the message
    if message is None: message = ''
    message = message.decode('ascii', errors='ignore')
    binary = (''.join(binary_format.format(ord(x)) for x in message))
    len_binary = len(binary)

    # Add the angst binary data.
    result = []
    for i, line in enumerate(in_file):
        match = newline_re.search(line)
        # We should only not get one on the last line.
        if match:
            line = line.rstrip() + (
                ' ' if i < len_binary and binary[i] == '1' else ''
                ) + match.group(1)
        result.append(line)

    if i < len_binary:
        sys.stderr.write(
            'Warning: Message needs %d lines to encode, file has %d. '
            'Message has been truncated.\n' %
            (len_binary, i)
            )

    # Combine the lines.
    result = ''.join(result)
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
            'Error: No message to add, use `angst remove` to remove angst.\n'
            )
        sys.exit(-1)
    run_write_message(args, message)

def run_remove(args):
    run_write_message(args, message=None)

def run_read(args):
    data = []
    for i, line in enumerate(args.file):
        x = bits_per_char - 1 - (i % bits_per_char)
        if x == bits_per_char - 1: data.append(0)

        match = ending_re.search(line)
        if match:
            data[-1] += 2**x

    # Write to stdout.
    print(''.join(chr(datum) for datum in data))

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
