import sys

COLOR_RED = "\x1b[31m"
COLOR_RESET = "\x1b[0m"
COLOR_GREEN = "\x1b[32m"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def logError(msg: str):
    eprint(f"[{COLOR_RED}FAIL{COLOR_RESET}]: {msg}")
    exit(1)


def logSuccess(msg: str):
    print(f"[{COLOR_GREEN}DONE{COLOR_RESET}]: {msg}")
