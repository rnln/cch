#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2020 Roman Ilin <me@romanilin.me>.
# This work is free. You can redistribute and modify it under the terms of the
# Do What The Fuck You Want To Public License, Version 2, as published by Sam
# Hocevar. You may obtain a copy of the license in the COPYING file or at
# https://github.com/rnln/everyday_commit/COPYING
"""Setup script for Everyday Commit."""

from getpass import getuser
from json import dump
from pathlib import Path
from shutil import copyfile
from subprocess import check_call
from subprocess import check_output
from sys import executable
from venv import EnvBuilder

from ec import get_path


MEAN_CALENDAR_YEAR = 365.2425
PARENT_PATH = Path(__file__).resolve().parent
DEFAULT_PER_DAY = 4
DEFAULT_PER_YEAR = 1460
PERIOD_REQUEST = ('Choose period to determine the number of contributions, day '
                  'or year (default is day) [d/y]: ')
NUMBER_REQUEST = ('Enter the desired average number of contributions (default '
                  'is {}): ')
INPUT_ERROR = "I didn't get it, let's try again."

def main():
    """Create virtual environment, install requirements and create cron job"""

    config_path = get_path('config.json')
    if not config_path.is_file():
        while True:
            period = input(PERIOD_REQUEST).lower()
            if not period:
                period = 'd'
            if period not in ['d', 'y']:
                print(INPUT_ERROR)
            else:
                break
        while True:
            contributions_number = input(NUMBER_REQUEST.format(
                DEFAULT_PER_DAY if period == "day" else DEFAULT_PER_YEAR))
            if not contributions_number:
                contributions_number = 9 if period == 'd' else 3287
            try:
                contributions_number = float(contributions_number)
            except ValueError:
                print(INPUT_ERROR)
            else:
                break
        print('Creating configuration file...')
        if period == 'y':
            contributions_number /= MEAN_CALENDAR_YEAR
        with open(config_path, 'w') as config_file:
            dump({'contributionsPerDay': contributions_number}, config_file)

    print('Creating virtual environment...')
    EnvBuilder(with_pip=True).create(get_path('venv'))

    print('Activating virtual environment...')
    activate_path = get_path('venv', 'bin', 'activate_venv.py')
    copyfile(get_path('activate_venv.py'), activate_path)
    with open(activate_path) as activate_file:
        code = compile(activate_file.read(), activate_path, 'exec')
        exec(code, dict(__file__=activate_path))

    print('Updating packages...')
    outdated_packages = check_output([executable, '-m', 'pip', 'list', '-o',
                                      '--format', 'freeze']).decode('utf-8')
    for line in outdated_packages.splitlines():
        package = line.split('=')[0]
        check_call([executable, '-m', 'pip', 'install', '-U', package])
    print('Installing requirements...')
    check_call([executable, '-m', 'pip', 'install', '-r',
                get_path('requirements.txt')])

    print('Creating cron job...')
    from crontab import CronTab
    command = f'"{executable}" "' + str(get_path('everyday_commit.py')) + '"'
    cron = CronTab(user=getuser())
    job = cron.new(command=command, comment='Everyday Commit')
    job.day.every()
    print('Adding job to crontab...')
    # cron.write()
    print(job)


if __name__ == '__main__':
    main()
