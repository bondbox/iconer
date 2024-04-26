# coding:utf-8

import os
import shutil
from urllib.parse import urlparse
from uuid import uuid4

import favicon
import requests
from xarg import add_command
from xarg import argp
from xarg import color
from xarg import commands
from xarg import csv
from xarg import form
from xarg import run_command


def generate_uuid() -> str:
    return ('%032x' % uuid4().int)[:8]  # pylint: disable=C0209


def save_icon(icon: favicon.Icon, path: str) -> str:
    resp: requests.Response = requests.get(icon.url, stream=True, timeout=15)
    with open(path, "wb") as image:
        for chunk in resp.iter_content(4096):
            image.write(chunk)
    return icon.url


@add_command("download", help="download the favicon of a website")
def add_cmd_download(_arg: argp):
    _arg.add_argument("--output", type=str, nargs=1, metavar="DIR",
                      default=["."], help="the directory to save the icon")
    _arg.add_argument(dest="urls", type=str, nargs="+", metavar="URL",
                      help="the url of a website")


@run_command(add_cmd_download)
def run_cmd_download(cmds: commands) -> int:  # pylint: disable=unused-argument
    output: str = cmds.args.output[0]
    for url in cmds.args.urls:
        domain: str = urlparse(url).netloc
        directory: str = os.path.join(output, domain)
        favicons: form[str, str] = form(domain, ("file", "url"))
        if os.path.isdir(directory):
            red_dir: str = color.red(directory)
            message: str = f"remove already existing directory: {red_dir}"
            cmds.stderr(color.yellow(message))
            shutil.rmtree(directory)
        os.makedirs(directory)
        for icon in favicon.get(url):
            uuid: str = generate_uuid()
            name: str = f"{uuid}.{icon.format}"
            path: str = os.path.join(directory, name)
            cmds.stdout(f"download {color.green(domain)} {color.yellow(icon)} "
                        f"to {color.black(path)}")
            favicons.append((uuid, save_icon(icon, path)))
        csv.dump(os.path.join(directory, "favicons.csv"), favicons)
    return 0
