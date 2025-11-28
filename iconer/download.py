# coding:utf-8

import os
import shutil
from urllib.parse import urlparse
from uuid import uuid4

import favicon
import requests
from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor
from xkits_logger import Color
from xkits_sheet import CSV
from xkits_sheet import Form


def generate_uuid() -> str:
    return ('%032x' % uuid4().int)[:8]  # pylint: disable=C0209


def save_icon(icon: favicon.Icon, path: str) -> str:
    resp: requests.Response = requests.get(icon.url, stream=True, timeout=15)
    with open(path, "wb") as image:
        for chunk in resp.iter_content(4096):
            image.write(chunk)
    return icon.url


@CommandArgument("download", help="download the favicon of a website")
def add_cmd_download(_arg: ArgParser):
    _arg.add_argument("--output", type=str, nargs=1, metavar="DIR",
                      default=["."], help="the directory to save the icon")
    _arg.add_argument(dest="urls", type=str, nargs="+", metavar="URL",
                      help="the url of a website")


@CommandExecutor(add_cmd_download)
def run_cmd_download(cmds: Command) -> int:  # pylint: disable=unused-argument
    output: str = cmds.args.output[0]
    for url in cmds.args.urls:
        domain: str = urlparse(url).netloc
        directory: str = os.path.join(output, domain)
        favicons: Form[str, str] = Form(domain, ("file", "url"))
        if os.path.isdir(directory):
            cmds.stderr_yellow(f"remove already existing directory: {Color.red(directory)}")  # noqa:E501
            shutil.rmtree(directory)
        os.makedirs(directory)
        for icon in favicon.get(url):
            uuid: str = generate_uuid()
            name: str = f"{uuid}.{icon.format}"
            path: str = os.path.join(directory, name)
            cmds.stdout(f"download {Color.green(domain)} {Color.yellow(icon)} to {Color.black(path)}")  # noqa:E501
            favicons.append((uuid, save_icon(icon, path)))
        CSV.dump(os.path.join(directory, "favicons.csv"), favicons)
    return 0
