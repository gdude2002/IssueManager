"""
This is a bot designed to work with GitHub issues for certain repos.

This was designed for use with the GlowstoneMC project, but it may be generic
enough for you to use with your own projects as well.
"""

__author__ = 'Gareth Coles'

from system.manager import Manager
from util import log

log.set_level()

m = Manager()

if m.ready:
    m.run()
