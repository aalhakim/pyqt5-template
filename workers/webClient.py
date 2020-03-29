#!python3

"""
A separate thread to handle Amazon S3 actions.

Last Updated: 29 March 2020 (Ali Al-Hakim)
"""

# Standard library Imports
import os
import time
import logging
debugLogger = logging.getLogger(__name__)

# Third-Party Library Imports
from PyQt5 import QtCore

# Local Libray imports
from modules.amazonS3Client import S3Session
from modules.pyGithubClient import PyGithubClient


########################################################################
GH_REPO_ORGANISATION = "BBOXX"
GH_REPO_NAME = "battery-test-bench"


########################################################################
class WebClient(QtCore.QObject):

    sigShutdown = QtCore.pyqtSignal()
    sigReleaseList = QtCore.pyqtSignal(list)
    sigReleaseLatest = QtCore.pyqtSignal(str)

    def __init__(self, s3_bucket, s3_access_key, s3_secret_key, gitub_access_token):
        super(WebClient, self).__init__()
        self.daemon = True

        self.s3 = S3Session(s3_bucket, s3_access_key, s3_secret_key)
        self.gh = PyGithubClient(gitub_access_token)

    @QtCore.pyqtSlot()
    def shutdown(self):
        """
        Begin the shutdown sequence for this thread.
        """
        # -------------------------- #
        # Kill active processes here #
        # -------------------------- #
        self.sigShutdown.emit()

    @QtCore.pyqtSlot(str, str, str)
    def s3_download(self, s3_directory, dst_directory, filename):
        """
        Download a file from Amazon S3.
        """
        self.s3.download_file(s3_directory, dst_directory, filename)

    @QtCore.pyqtSlot(str, str, str)
    def s3_upload(self, src_directory, s3_directory, filename):
        """
        Upload a file to Amazon S3.
        """
        self.s3.upload_file(src_directory, s3_directory, filename)

    @QtCore.pyqtSlot(str)
    def handle_release_query(self, query):
        """
        Handle a the request to retrieve release data.
        """
        if query == "all":
            self._gh_release_list()
        elif query == "latest":
            self._gh_release_latest()
        else:
            raise RuntimeError("Invalid query to `get_release` method: {}".format(query))

    def _gh_release_latest(self):
        """
        Retrieve the latest software release from GitHub.
        """
        release = self.gh.get_latest_release(GH_REPO_ORGANISATION, GH_REPO_NAME)
        self.sigReleaseLatest.emit(release.tag_name)

    def _gh_release_list(self):
        """
        Retrieve a list of available software releases from GitHub.
        """
        release_list = []
        releases = self.gh.get_releases(GH_REPO_ORGANISATION, GH_REPO_NAME)
        for release in releases:
            release_list.append(release.tag_name)
        self.sigReleaseList.emit(release_list)
