from .pacman import check_pkgs
from .logger import logError, logSuccess
from os import mkdir, getenv, path
from shutil import copy


def copyIfNot(src, dest):
    if not path.exists(dest):
        copy(src, dest)


def prepare():
    if not check_pkgs(["artools-pkg", "iso-profiles"]):
        logError("Either \"artools\" or \"iso-profiles\" package is missing!")

    home = getenv("HOME")

    if not path.exists(f"{home}/.config/artools/"):
        mkdir(f"{home}/.config/artools/")

    copyIfNot("/etc/artools/artools-base.conf",
              f"{home}/.config/artools/artools-base.conf")

    copyIfNot("/etc/artools/artools-iso.conf",
              f"{home}/.config/artools/artools-iso.conf")

    copyIfNot("/etc/artools/artools-pkg.conf",
              f"{home}/.config/artools/artools-pkg.conf")

    logSuccess("Basic artools config initialized")
