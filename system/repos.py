__author__ = 'Gareth Coles'

import re

from github.GithubException import UnknownObjectException
from util.log import getLogger


class Repos(object):
    manager = None
    repo_objects = {}

    @property
    def repos(self):
        return self.manager.repos

    def __init__(self, manager):
        """
        :type manager: system.manager.Manager
        """
        self.manager = manager
        self.log = getLogger("Repos")

        for repo in self.repos.keys():
            try:
                r = self.manager.github.get_repo(repo)

                self.log.info("Got repo: %s" % r.name)
                self.repo_objects[repo] = r
            except UnknownObjectException:
                self.log.warn("Unknown repo: %s" % repo)

        self.do_init()

    def do_action(self, target, type, args):
        pass

    def do_checka(self, checka, comment):
        pass

    def do_init(self):
        for key, repo in self.repo_objects.items():
            #: :type repo: Repository

            repo_data = self.repos.get(key)

            label_regex = re.compile(repo_data["label_regex"])
            initial = repo_data.get("initial", {})
            issues = initial.get("issues", [])
            actions = initial.get("actions", {})

            for issue in issues:
                #: :type: github.Issue.Issue
                t = repo.get_issue(issue)

                try:
                    if t.state != "open":
                        continue

                    has_label = False

                    for label in t.get_labels():
                        if re.match(label_regex, label.name):
                            has_label = True
                            break

                    if not has_label:
                        continue

                    self.log.info("New issue: %s" % issue)
                except UnknownObjectException:
                    self.log.warn("Unknown issue: %s/%s" % (key, issue))
