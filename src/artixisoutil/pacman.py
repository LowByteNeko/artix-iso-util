from os import popen

pkgs = []


def check_pkgs(packages: list) -> bool:
    if len(pkgs) == 0:
        temp_pkgs = popen("pacman -Q").read().splitlines()
        for pkg in temp_pkgs:
            pkgs.append(pkg.split(" ")[0])

    for pkg in packages:
        if pkg not in pkgs:
            return False
    return True
