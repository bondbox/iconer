# coding:utf-8

from typing import Optional
from typing import Sequence

from xkits_command import ArgParser
from xkits_command import Command
from xkits_command import CommandArgument
from xkits_command import CommandExecutor

from iconer.attribute import __description__
from iconer.attribute import __project__
from iconer.attribute import __urlhome__
from iconer.attribute import __version__
from iconer.download import add_cmd_download


@CommandArgument(__project__, description=__description__)
def add_cmd(_arg: ArgParser):  # pylint: disable=unused-argument
    pass


@CommandExecutor(add_cmd, add_cmd_download)
def run_cmd(cmds: Command) -> int:  # pylint: disable=unused-argument
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = Command()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, epilog=f"For more, please visit {__urlhome__}.")  # noqa:E501
