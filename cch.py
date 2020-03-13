#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2020 Roman Ilin <@romanilin.me>.
# This work is free. You can redistribute and modify it under the terms of the
# Do What The Fuck You Want To Public License, Version 2, as published by Sam
# Hocevar. You may obtain a copy of the license in the COPYING file or at
# https://github.com/rnln/cch/COPYING
"""GitHub contributions cheat.

Generates a random number of commits and push them following a gamma
distribution.
"""

from decimal import Decimal
from decimal import ROUND_HALF_UP
from json import load
from pathlib import Path
from pathlib import PurePath
from random import gammavariate
from time import time

from git import Repo
from git.remote import Remote


with open('config.json', 'r') as f: MEAN = load(f)['contributionsPerDay']
SHAPE = 0.3
MEAN_SHIFT = 0.02195121951
RATE = (MEAN + MEAN_SHIFT) / SHAPE  # Fix mean value shift caused by rounding

PROJECT_PATH = Path(__file__).resolve().parent
COMMENT = 'Change Unix time'


def get_path(*path):
    """Join arguments to full path relative to module parent directory"""

    return PurePath.joinpath(PROJECT_PATH, *list(map(str, path)))


REPO = Repo(get_path('.git'))
UNIX_TIME_PATH = get_path('unix-time.txt')


def commit(path, comment):
    """Commit and push changes in file by path"""

    REPO.index.add(path)
    REPO.index.commit(comment)
    Remote(REPO).push()


def round_half_away_from_zero(number):
    """Round number half away from zero"""

    return int(Decimal(number).quantize(Decimal(0), rounding=ROUND_HALF_UP))


def main():
    """Generate a random number of commits and push them."""

    commits_number = round_half_away_from_zero(gammavariate(SHAPE, RATE))

    with open(UNIX_TIME_PATH, 'w') as f:
        for i in range(0, commits_number):
            f.write(time())
            commit(UNIX_TIME_PATH, COMMENT)


if __name__ == '__main__':
    main()
