from .pacman import check_pkgs
from .logger import logError, logSuccess
from .configs import baseGen, isoGen
from os import mkdir, getenv, path, getcwd, chdir
from shutil import copy


def copyIfNot(src, dest):
    if not path.exists(dest):
        copy(src, dest)


def getMangedInput(prompt, default, check, failMsg):
    val = ""
    while not check(val):
        try:
            val = input(prompt)
            if not check(val):
                print(failMsg)
        except:
            val = default
    return val


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


def init_proj():
    name = getMangedInput("Type name of your project: ", "",
                          lambda p: len(p.strip()) > 0, "Enter project name")
    name = name.strip()

    if path.exists(name):
        logError(f"Directory \"{name}\" already exists!")

    mkdir(name)
    chdir(name)
    cwd = getcwd()
    home = getenv("HOME")

    with open(f"{home}/.config/artools/artools-base.conf", "w") as f:
        f.write(baseGen(cwd))

    chdir("..")
