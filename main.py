import asyncio
from argparse import ArgumentParser
from pathlib import Path

from command_interface import CommandInterface
from commons import StoreJSON
from tracker import Tracker


async def main():
    argument_parser = ArgumentParser(
        prog="task-cli",
        description="A command-line interface for managing tasks.",
    )
    tracker = Tracker(
        StoreJSON(Path("tasks.json"))
    )
    command_interface = CommandInterface(argument_parser, tracker)
    await command_interface.execute()


if __name__ == '__main__':
    asyncio.run(main())
