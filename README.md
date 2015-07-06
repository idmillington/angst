# Angst

Add secret messages (in ASCII) to source code.

    $ angst add my_raw_file.c -m "This wasn't paid for."

And retreive them later

    $ angst read my_raw_file.c

The messages use trailing whitespace, so they won't be noticed easily.

For more help, do

    $ angst -h

The system isn't designed to be robust. Editing lines, saving with stripped
whitespace, or running through some lint tools will cause problems.

Its a fun toy based on code originally written in an hour or so for an
Alternate Reality Game.

I'd very much welcome push requests with code that makes it more robust to
changes, or allows a wider range of encodings (such as UTF-8) particularly.
