# -*- coding: utf-8 -*-


import argparse


def get_args():
     # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query",
        type=str,
        help="query to look for images"
    )
    parser.add_argument(
        "-p",
        "--path",
        action="store",
        help="folder to store the images"
    )
    return parser.parse_args()
