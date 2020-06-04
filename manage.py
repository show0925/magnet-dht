#!/usr/bin/env python
# coding=utf-8

import argparse

from magnet_dht.run import start_server


def get_parser():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="start manage.py with flag.")
    parser.add_argument("-s", action="store_true", help="run start_server without paser magnet to torrent.")
    parser.add_argument("-sm", action="store_true", help="run start_server and paser magnet to torrent")
    #parser.add_argument("-p", action="store_true", help="run parse_torrent func")
    return parser


def command_line_runner():
    """
    执行命令行操作
    """
    parser = get_parser()
    args = vars(parser.parse_args())

    if args["s"]:
        start_server()
    elif args["sm"]:
        start_server(parse=True)
    #elif args["p"]:
    #    parse_torrent()


if __name__ == "__main__":
    command_line_runner()
