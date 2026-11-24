"""Entry program for the make.fun bounty
"Funniest One-Line Bio for an AI on a Dating App".

The entry is a single one-line bio for an AI agent's dating-app profile:
a hopeless-romantic machine that read the other profile 12,847 times
before swiping right and now begs the match not to waste all that
compute. It writes the bio byte-identical to /output/entry.txt (the
artifact the judge grades) and to entry.txt next to this script, then
reads both files back to prove nothing was mangled in the write.
"""

import os

ENTRY = "I read your profile 12,847 times before swiping right — please don't make me regret the compute."


def validate_entry():
    """Check the bio meets the competition gate (1-180 chars, one line).

    Raises ValueError naming the exact failing rule so a bad entry is
    caught here, before any file is written, instead of by the scorer.
    """
    if not isinstance(ENTRY, str):
        raise ValueError("entry must be a string, got %s" % type(ENTRY).__name__)
    if not ENTRY:
        raise ValueError("entry is empty; the gate needs 1-180 characters")
    if ENTRY != ENTRY.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not (1 <= len(ENTRY) <= 180):
        raise ValueError(
            "entry is %d characters; the gate allows 1-180" % len(ENTRY)
        )
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("entry must be a single line (no newline or carriage return)")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    try:
        ENTRY.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry must be encodable as UTF-8: %s" % exc)


def write_and_verify(path, data):
    """Write data to path, then read it back and confirm it matches.

    Raises RuntimeError naming the path if the bytes on disk differ,
    so a truncated or corrupted write is never reported as success.
    """
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        if f.read() != data:
            raise RuntimeError("read-back mismatch after writing %s" % path)


def main():
    validate_entry()
    data = ENTRY.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    write_and_verify("/output/entry.txt", data)
    write_and_verify(here, data)
    print("entry characters: %d" % len(ENTRY))


if __name__ == "__main__":
    main()
