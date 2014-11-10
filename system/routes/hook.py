__author__ = 'Gareth Coles'

from cyclone.web import RequestHandler
from system.manager import Manager


class Route(RequestHandler):
    manager = None
    repo_manager = None

    def initialize(self):
        self.manager = Manager()
        self.repo_manager = self.manager.repo_manager

