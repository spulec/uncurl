import argparse
from typing_extensions import override


class ArgumentParser(argparse.ArgumentParser):
    @override
    def error(self, message):
        raise ValueError(message)