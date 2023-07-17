import sys

COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def logError(msg: str):
    eprint(f"[{COLOR_RED}FAIL{COLOR_RESET}]: {msg}")
    exit(1)
