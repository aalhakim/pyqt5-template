#!python3

"""
Example code to use the GitHub REST API.

GitHub has deprecated the use of basic athentication via the API (i.e.
username and password method). Therefore, authentication must be made
using an Access Token. For instruction on how to create an access token
follow the guide here:
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

Once you have created an access token, save the value in a local .env
file under the tag ACCESS_TOKEN. To run this example code, the token
will need to be given 'repo: Full control of private repositories'
permission.

---
Documentation for PyGitHub
https://pygithub.readthedocs.io/en/latest/introduction.html

Documentation for GitHub API:
https://developer.github.com/v3/

---
Author: Ali Al-Hakim
Last Updated: 22 March 2020
"""

# Standard library imports
import os
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party library imports
from github import Github


########################################################################

class PyGithubClient(object):

    def __init__(self, access_token):
        self.client = self._authenticate(access_token)
        self.user = self.client.get_user()

    def _authenticate(self, access_token):
        return Github(access_token)

    def print_repo_list(self):
        """
        Print out a list of all available repository names and the
        associated user account.
        """
        repo_list = self.get_repo_list()
        for org_name, repo_list in repo_list.items():
            print("\n >> {}".format(org_name))

            for repo_name in repo_list:
                print("     - {}".format(repo_name))
                pass

    def get_repo_list(self):
        """
        Return a dictionary of all available repositorys.
        """
        repo_list = {}
        for repo in self.user.get_repos():
            org_name, repo_name = repo.full_name.split("/")

            try:
                repo_list[org_name].append(repo_name)
            except KeyError:
                repo_list[org_name] = [repo_name]

        return repo_list

    def get_repo(self, organisation, repo_name):
        """
        Return a repository object.

        Parameters
        ==========
        organisation: <string>
            Name of the repository owner (user or organisation).

        repo_name: <string>
            Name of the repository.
        """
        repo = "{}/{}".format(organisation, repo_name)
        return self.client.get_repo(repo)

    def get_releases(self, organisation, repo_name):
        """
        Return a list of Git Releases for the inserted repository.

        Parameters
        ==========
        organisation: <string>
            Name of the repository owner (user or organisation).

        repo_name: <string>
            Name of the repository.
        """
        repo = self.get_repo(organisation, repo_name)
        return repo.get_releases()

    def get_latest_release(self, organisation, repo_name):
        """
        Return a list of Git Releases for the inserted repository.

        Parameters
        ==========
        organisation: <string>
            Name of the repository owner (user or organisation).

        repo_name: <string>
            Name of the repository.
        """
        repo = self.get_repo(organisation, repo_name)
        return repo.get_latest_release()

#######################################################################
def print_GitRelease(git_release_object):
    print("{:>15s}: {}".format("Title", git_release_object.title))
    print("{:>15s}: {}".format("Tag Name", git_release_object.tag_name))
    print("{:>15s}: {}".format("Author", git_release_object.author))
    print("{:>15s}: {}".format("Published At", git_release_object.published_at))
    print("{:>15s}: {}".format("Created At", git_release_object.created_at))
    print("{:>15s}: {}".format("Pre-release?", git_release_object.prerelease))
    print("{:>15s}: {}".format("Draft?", git_release_object.draft))
    print("{:>15s}: {}".format("URL", git_release_object.url))
    print("{:>15s}:\n\n{}\n".format("Body", git_release_object.body))


#######################################################################
if __name__ == "__main__":

    import dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    REPO_ACCESS_TOKEN = os.environ["REPO_ACCESS_TOKEN"]
    ORGANISATION = "BBOXX"
    REPOSITORY = "battery-test-bench"

    gh = PyGithubClient(ACCESS_TOKEN)

    # Print a list of all repositories USERNAME can access
    print(" ----- REPOSITORIES -----")
    gh.print_repo_list()
    print("")

    # get a list of releases from a repository
    print(" ----- RELEASES -----")
    releases = gh.get_releases(ORGANISATION, REPOSITORY)
    for release in releases:
        print_GitRelease(release)
        print("")

    # Get the latest release from a repository
    print(" ----- LATEST RELEASE -----")
    latest_release = gh.get_latest_release(ORGANISATION, REPOSITORY)
    print_GitRelease(latest_release)
    print("")
