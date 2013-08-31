
"""

Simple.

"""

import sys
import logging
import argparse

logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('recipient')
    parser.add_argument('sender')
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    logger.info("message from %s to %s with content: %s", args.sender, args.recipient, sys.stdin.read())


if __name__ == '__main__':
    main()


