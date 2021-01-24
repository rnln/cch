#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2020 Roman Ilin <me@romanilin.me>.
# This work is free. You can redistribute and modify it under the terms of the
# Do What The Fuck You Want To Public License, Version 2, as published by Sam
# Hocevar. You may obtain a copy of the license in the COPYING file or at
# https://github.com/rnln/everyday_commit/COPYING
"""Everyday Commit.

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

import math


with open('config.json', 'r') as config_file:
    MEAN = load(config_file)['contributionsPerDay']
SHAPE = 0.3
MEAN_SHIFT = 0.02144067294
RATE = (MEAN + MEAN_SHIFT) / SHAPE  # Fix mean value shift caused by rounding

PARENT_PATH = Path(__file__).resolve().parent
COMMENT = 'Change Unix time'


def get_path(*path):
    """Join arguments and full path to module parent directory"""

    return PurePath.joinpath(PARENT_PATH, *list(map(str, path)))


REPO = Repo(get_path('.git'))
UNIX_PATH = get_path('unix_time.txt')


def commit(path, comment):
    """Commit and push changes in file by path"""

    REPO.index.add(str(path))
    REPO.index.commit(comment)
    Remote(REPO, 'origin').push()


def round_half_away_from_zero(number):
    """Round number half away from zero"""

    return int(Decimal(number).quantize(Decimal(0), rounding=ROUND_HALF_UP))


def main():
    """Generate a random number of commits and push them."""

    commits_number = round_half_away_from_zero(gammavariate(SHAPE, RATE))

    for _ in range(0, commits_number):
        with open(UNIX_PATH, 'w') as unix_file:
            unix_file.write(str(time()))
        commit(UNIX_PATH, COMMENT)


if __name__ == '__main__':
    main()
