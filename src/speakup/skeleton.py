"""Speak Up CLI."""

import sys

from hydra import compose, initialize
from omegaconf import OmegaConf

from speakup import __version__

__author__ = "GaviniSumanth"
__copyright__ = "GaviniSumanth"
__license__ = "MIT"


def run() -> None:
    """Speak Up CLI."""
    with initialize(version_base=None, config_path="conf"):
        cfg = compose("config.yaml", overrides=sys.argv[1:])
        print(f"SpeakUp CLI: {__version__}")
        print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    run()
