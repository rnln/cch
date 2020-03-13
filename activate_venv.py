# -*- coding: utf-8 -*-
"""Activate virtual environment for current interpreter.

This is modified version of activate_this.py from virtualenv package.

Usage:
with open(this_file) as f:
    code = compile(f.read(), this_file, 'exec')
    exec(code, dict(__file__=this_file))
"""

from pathlib import Path
import os
import sys


base = os.path.dirname(os.path.abspath(__file__))

# prepend bin to PATH (this file is inside the bin directory)
os.environ['PATH'] = os.pathsep.join([base] + os.environ['PATH'].split(os.pathsep))
os.environ['VIRTUAL_ENV'] = base  # virtual env is right above bin directory

# add the virtual environments libraries to the host python import mechanism
sys.path.append(os.fspath(list(Path(base).parent.rglob('site-packages'))[0]))

sys.real_prefix = sys.prefix
sys.prefix = base
sys.executable = os.path.join(sys.prefix, 'python')

print(sys.real_prefix)
print(sys.prefix)
print(sys.executable)
