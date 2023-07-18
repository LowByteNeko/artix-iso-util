import argparse
from .artools import prepare, init_proj, build_proj


def main():
    parser = argparse.ArgumentParser(
                    prog="artixisoutil",
                    description="Advanced wrapper for artix's buildiso")

    parser.add_argument("action", metavar="ACTION", type=str, nargs="+",
                        choices=["init-artools", "init", "build",
                                 ],
                        help="Actions to be executed in order")

    args = parser.parse_args()
    arr = args.action

    if "init-artools" in arr:
        prepare()

    if "init" in arr:
        init_proj()

    if "build" in arr:
        build_proj()
