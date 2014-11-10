__author__ = 'Gareth Coles'

import yaml

from cyclone.web import Application
from twisted.internet import reactor
from github import Github

from system.singleton import Singleton
from system.repos import Repos
from util.log import getLogger


class Manager(object):
    __metaclass__ = Singleton

    app = None
    log = None
    github = None
    ready = False
    repos = {}

    repo_manager = None

    def __init__(self):
        self.log = getLogger("Manager")
        self.log.info("Loading..")

        config = yaml.load(open("config/settings.yml"))

        gh = config["github"]
        self.github = Github(gh["username"], gh["password"])

        try:
            self.log.info("Logged in as '%s'" % self.github.get_user().name)
        except Exception:
            self.log.exception("Unable to login: %s")

        self.app = Application(
            [],  # Routes
            log_function=self.log_request
        )

        self.port = reactor.listenTCP(
            config["networking"]["port"], self.app
        )

        self.repos = config["repos"]
        if len(self.repos) > 1:
            self.log.info("Tracking repos: %s" % ", ".join(self.repos.keys()))
        else:
            self.log.info("Tracking repo: %s" % ", ".join(self.repos.keys()))

        self.ready = True

        self.repo_manager = Repos(self)

        del config

    def run(self):
        self.log.info("Reactor started.")
        reactor.run()

    def log_request(self, request):
        log = self.log.info

        status_code = request.get_status()

        if status_code >= 500:
            log = self.log.error
        elif status_code >= 400:
            log = self.log.warn

        log(
            "[%s] %s %s -> HTTP %s"
            % (
                request.request.remote_ip,
                request.request.method,
                request.request.path,
                request.get_status()
            )
        )
