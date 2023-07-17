from .pacman import check_pkgs
from .logger import logError
from os import mkdir, getenv, path


def prepare():
    if not check_pkgs(["artools-pkg", "iso-profiles"]):
        logError("Either \"artools\" or \"iso-profiles\" package is missing!")

    home = getenv("HOME")

    if not path.exists(f"{home}/artools-workspace"):
        mkdir(f"{home}/artools-workspace")
