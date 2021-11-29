import argparse
import config
from .parser import KernelParser
from .utils import TelegramUtils

parser = argparse.ArgumentParser(
    prog="kernel_tracker", description="Utility to track kernel releases"
)
parser.add_argument(
    "-j",
    "--json",
    metavar="N",
    type=int,
    nargs="?",
    const=4,
    help="prints kernel version release table as json (optionally provide indent length N)",
)
parser.add_argument(
    "-g",
    "--get-updated",
    action="store_true",
    help="prints updated kernel versions",
)

parser.add_argument(
    "-n",
    "--notify",
    action="store_true",
    help="send notification to Telegram chat for updated kernels",
)

parser.add_argument(
    "-w",
    "--write-json",
    action="store_true",
    help="write latest releases to json file",
)
args = parser.parse_args()


def main():
    """Main entry-point for program."""

    kernel = KernelParser(config.DB_FILE_NAME)
    util = TelegramUtils(config.BOT_API)
    if args.json is not None:
        print(kernel.to_json(args.json))
    elif args.get_updated:
        print(kernel.to_hooman(kernel.get_updated_kernels()))
    elif args.write_json:
        kernel.write_json()
    elif args.notify:
        util.send_to_tg(config.CHAT_ID, kernel.get_updated_kernels())
        kernel.write_json()  # should always write to json after notifying
    else:
        print(kernel.to_hooman())


if __name__ == "__main__":
    main()
