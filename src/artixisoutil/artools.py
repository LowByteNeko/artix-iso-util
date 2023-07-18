from .pacman import check_pkgs
from .logger import logError, logSuccess
from .configs import baseGen, isoGen
from os import mkdir, getenv, path, chdir, popen, getcwd, system, symlink
from shutil import copy
import tomllib


def copyIfNot(src, dest):
    if not path.exists(dest):
        copy(src, dest)


def getMangedInput(prompt, default, check, failMsg):
    val = ""
    while not check(val):
        try:
            val = input(prompt).strip()
            if not check(val):
                failMsg(val)
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


def checkStrength(prompt):
    try:
        val = int(prompt)
        return not (val > 22 or val < 1)
    except ValueError:
        return False


def init_proj():
    name = getMangedInput("Type name of your project: ", "",
                          lambda p: len(p.strip()) > 0,
                          lambda _: print("Enter valid project name!"))

    if path.exists(name):
        logError(f"Directory \"{name}\" already exists!")

    mkdir(name)
    chdir(name)
    version = getMangedInput("Type version of your project: ",
                             "unknown",
                             lambda p: len(p.strip()) > 0,
                             lambda _: print("Enter valid project version!"))

    inits = ["openrc", "runit", "s6", "suite66", "dinit"]
    msg = "Select your init system:\n" + "\n".join(inits) + ": "

    init = getMangedInput(msg, "openrc", lambda p: p in inits,
                          lambda p:
                          print(f"Init system \"{p}\" is invalid option"))

    compr = getMangedInput("Type desired compression [zstd/xz]: ",
                           "zstd",
                           lambda p: p in ["zstd", "xz"],
                           lambda p: print(f"Unsupported compression \"{p}\""))

    strength = "1"

    if compr == "zstd":
        strength =\
                int(getMangedInput("Type zstd compressions strength 1..22: ",
                                   "1",
                                   lambda p: checkStrength(p),
                                   lambda _:
                                   print("Invalid compression strength!")))

    with open("./workspace.toml", "w") as f:
        f.write(f"""[iso]
version = "{version}"

[iso.compression]
type = "{compr}"
level = {strength}

[iso.init]
type = "{init}"
services = ["acpid", "cronie", "metalog"]
""")
    popen("cp -r /usr/share/artools/iso-profiles/base/* .").read()

    chdir("..")

    logSuccess("Project initialized!")


def build_proj():
    data = {}
    if not path.exists("./workspace.toml"):
        logError("File \"workspace.toml\" doesn't exist")

    with open("./workspace.toml", "rb") as f:
        data = tomllib.load(f)

    cwd = getcwd()

    version = data["iso"]["version"]
    compr = data["iso"]["compression"]
    compr_type = compr["type"]
    level = compr["level"]

    init = data["iso"]["init"]
    init_type = init["type"]

    home = getenv("HOME")

    with open(f"{home}/.config/artools/artools-base.conf", "w") as f:
        f.write(baseGen(cwd))

    if not path.exists(path.join(cwd, "iso-profiles")):
        mkdir(path.join(cwd, "iso-profiles"))
        symlink(cwd, path.join(path.join(cwd, "iso-profiles"),
                               path.basename(cwd)))

    with open(f"{home}/.config/artools/artools-iso.conf", "w") as f:
        f.write(isoGen(cwd, version, init_type, compr_type, level))

    try:
        system(f"buildiso -p {path.basename(cwd)}")
    except:
        logError("Something went wrong!")

    logSuccess("Iso built successfully")
