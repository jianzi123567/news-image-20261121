#!/usr/bin/env python3
"""news-image-20261121: copy the 21 November 2026 world-news image.

The artwork is bundled in this repository as entry.png. Running this
program writes those exact bytes to the output directory. It performs
no network access, reads no clock, and uses no randomness, so repeated
runs always produce the same file.
"""

import os
import sys

SOURCE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024


def read_source():
    """Load the bundled image bytes from next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    with open(source, "rb") as handle:
        return handle.read()


def is_supported_image(data):
    """Accept only a small PNG or JPEG payload."""
    if len(data) > MAX_BYTES:
        return False
    if data[:2] == b"\xff\xd8":
        return True
    return data[:8] == b"\x89PNG\r\n\x1a\n"


def write_output(data):
    """Write the bytes to the output directory and check the copy."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE_NAME)
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        if handle.read() != data:
            raise SystemExit("output copy does not match the source")


def main():
    data = read_source()
    if not data:
        raise SystemExit("entry.png is empty")
    if not is_supported_image(data):
        raise SystemExit("entry.png is not a PNG or JPEG under 1 MiB")
    write_output(data)
    print(f"wrote /output/entry.png ({len(data)} bytes)")


if __name__ == "__main__":
    main()
