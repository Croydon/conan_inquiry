import json
import os
# from conan_inquiry.util.cache import Cache
from conan_inquiry.util.github import get_github_client
from sortedcontainers import SortedDict


class Wishlist:
    def __init__(self, development=False):
        self.github = get_github_client(3)
        self.dev = development

    def generate(self):
        """Generates the wishlist.json data"""

        repo = self.github.get_repo("conan-io/wishlist")
        issues = repo.get_issues(state="open", sort="updated", direction="desc")
        issuesSorted = SortedDict()
        jsonIssues = dict()

        for issue in issues:
            upvotes = 0
            for reaction in issue.get_reactions():
                if reaction.content == "+1":
                    upvotes += 1

            issuesSorted.update(dict({(upvotes, issue.number): issue.title}))

        for upvotes, issuetitle in reversed(issuesSorted.items()):
            print("{} : #{} {}".format(upvotes[0], upvotes[1], issuetitle))
            #jsonIssues.update(dict({upvotes[1]: (dict({'upvotes': upvotes[0]}), dict({'issue': upvotes[1]}), dict({'issuetitle': issuetitle}))}))
            jsonIssues.update(dict({upvotes[1]: dict({'upvotes': upvotes[0], 'issue': upvotes[1], 'issuetitle': issuetitle})}))

        if not os.path.exists("build/"):
            os.makedirs("build/")

        data = json.dumps(jsonIssues, indent=4)
        with open('build/wishlist.json', 'w') as file:
            file.write(data)

        with open('build/wishlist.js', 'w') as file:
            file.write('var wishlist_data = \n')
            file.write(data)
            file.write(';')
