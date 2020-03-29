#!python3

"""
Example code to upload and download files from AWS S3.

Documentation:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

Compatible with Python 3.x

---
Author: Ali Al-Hakim
Last Updated: 21 March 2020
"""


# Standard library imports
import os
import logging

# Logger configuration
if __name__ == "__main__":
    import logging.config
    logger_config = "logging_{}.conf".format(os.name)
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logger", logger_config))

# Control which modules are allowed to the application log files. This
# will block all logs except Critical logs from the defined group.
for name in ['boto', 'urllib3', 's3transfer', 'boto3', 'botocore', 'nose']:
    logging.getLogger(name).setLevel(logging.CRITICAL)
debugLogger = logging.getLogger(__name__)

# Third-party library imports
from boto3.session import Session
from botocore.exceptions import ClientError


########################################################################
class S3Session(object):
    """
    Create an AWS S3 client.
    """

    def __init__(self, bucket_name, access_key, secret_key):
        """ Initialise the S3Session object.
        """
        self.connect(bucket_name, access_key, secret_key)
        self._initialise()

        self.most_recent_object = None

    def connect(self, bucket_name, access_key, secret_key):
        """ Start an S3 session.

        Parameters
        ==========
        bucket_name: <string>
            Name of the bucket to connect to.

        access_key: <string>
            AWS Access Key with permission to access 'bucket_name'.

        secret_key: <string>
            AWS Secret Key with permission to access 'bucket_name'.

        Returns
        =======
        Nothing is returned, but the object variables 'self.s3',
        'self.bucket' and 'self.bucket_name' will be updated.
        """
        session = Session()
        self.s3 = session.resource("s3",aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_key)
        self.set_bucket(bucket_name)

    def set_bucket(self, bucket_name):
        """ Set which S3 bucket to access.

        Parameters
        ==========
        bucket_name: <string>
            Name of the bucket to connect to.

        Returns:
        Nothing is returned, but the object variables 'self.bucket' and
        'self.bucket_name' will be updated.
        """
        self.bucket = self.s3.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def get_bucket_name(self):
        """
        Return the name of the active bucket.

        Returns
        =======
        <string>
        Name of currently selected bucket.
        """
        return self.bucket_name

    def _initialise(self):
        """
        Make a dud request to the bucket to initiliase the session.
        """
        self._key_exists("x", "y")

    def _get_object(self, s3_directory, filename, renew=True):
        """
        Retrieve an S3 Object.

        Description
        ===========
        For more information about an S3 Object, see:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always request an object from S3. Set False to
            only request an object if the key has changed from the
            since the last _get_object() call.

        Returns
        =======
        If file is found: <boto3.resources.factory.s3.Object>

        If file is not found: <None>
            This is only returned if an 404 error is recieved. Any other
            error will raise an exception.

        Raises
        ======
        If an error other than HTTP 404 is returned, an exception will
        be raised.
        """
        s3_filepath = posix_filepath(s3_directory, filename)

        # Only retrieve new object information if forced to do so or if
        # the key has changed.
        if renew is False:
            if self.most_recent_object is not None:
                renew = s3_filepath != self.most_recent_object.key

        if renew is True:
            result = self.s3.Object(self.bucket_name, s3_filepath)

            # Check if the object exists in S3.
            try:
                result.load()
            except ClientError as err:
                # ClientError: Object not found
                if err.response["Error"]["Code"] != "404":
                    raise
                debugLogger.debug("File not found: {}".format(err))
                result = None

            self.most_recent_object = result

        else:
            # Continue to use previous information because the key is
            # the same as before and a force renew was not given.
            result = self.most_recent_object

        return result

    def _key_exists(self, s3_directory, filename):
        """
        Check if a key exists in S3.

        Returns
        =======
        <boolean> True if it exists, False if it doesn't.
        """
        exists = self._get_object(s3_directory, filename) is not None
        return exists

    #------------------------------------------------------------------
    def get_contents(self, s3_directory, include_subdirectories=True):
        """
        Retrieve the contents located inside the specified directory.

        Parameters
        ==========
        s3_directory: <string>
            Path to the directory whose contents is of interest. This
            should not include the bucket name.

        include_subdirectories: <boolean>
            Indicate whether files in sub-directories should also be
            returned or not. If set to False then only files immediately
            inside 's3_directory' will be returned.

        Returns
        =======
        <list> of <strings>
        A list of filepaths located inside 'self.bucket_name/s3_directory'
        """
        # Return all contents extending from 's3_directory'
        root = posix_filepath(s3_directory)
        contents = [s3_object.key for s3_object in self.bucket.objects.filter(Prefix=root)]

        # Return only contents found immediately in 's3_directory',
        # including folder names.
        if include_subdirectories is False:

            root_items = []
            for filepath in contents:
                root_item = filepath.split("/")[1]
                root_item_filepath = posix_filepath(root, root_item)
                if root_item_filepath not in root_items:
                    root_items.append(root_item_filepath)
            contents = root_items

        return contents

    def get_all_contents(self):
        """
        Retrieve all contents inside the bucket.

        Returns
        =======
        <list> of <strings>
        A list of filenames located inside `self.bucket_name`.
        """
        contents = [s3_object.key for s3_object in self.bucket.objects.all()]
        return contents

    #------------------------------------------------------------------
    def upload_file(self, src_directory, s3_directory, filename):
        """
        Upload 'src_directory/filename' to 's3_directory/filename'.

        The s3 file will be overwritten if it already exists in the
        destination location ('s3_directory').

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.upload_file

        Parameters
        ==========
        src_directory: <string>
            Filepath to the directory on the local machine where
            'filename' is found.

        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' will be
            uploaded to.

        filename: <string>
            Name of the file of interest, including file extension.

        Returns
        =======
        File exists locally, Upload successful: <boolean> True

        File exists locally, Upload failed: <boolean> False
            # TODO: (AHA) HOW IS THIS SITUATION HANDLED?

        File does not exist locally: <None>
        """
        # Create a filepath from the source directory and filename.
        src_filepath = posix_filepath(src_directory, filename)

        # If the file exists in S3
        if os.path.exists(src_filepath) is True:

            # Create a filepath from the destination directory and filename.
            s3_filepath = posix_filepath(s3_directory, filename)
            s3_object = self.s3.Object(self.bucket_name, s3_filepath)

            # Upload the target file to S3.
            try:
                s3_object.upload_file(src_filepath)
            except Exception as err:
                debugLogger.error("Upload file failed.", err)
                result = False
            else:
                result = True

        # If the file doesn't exist in S3
        else:
            result = None

        return result

    def download_file(self, s3_directory, dst_directory, filename):
        """
        Download 's3_directory/filename' to 'dst_directory/filename'.

        The local filepath ('dst_directory') will be created if it
        does not already exist. If 'filename' already exists in this
        location it will be overwritten.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.download_file

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        dst_directory: <string>
            Filepath to the directory on the local machine where
            'filename' should be saved to.

        filename: <string>
            Name of the file of interest, including file extension.

        Returns
        =======
        File exists in S3, Download successful: <boolean> True
            Filepath where the file was saved on the local machine.

        File exists in S3, Download failed: <boolean> False
            # TODO: (AHA) HOW IS THIS SITUATION HANDLED?

        File does not exist in S3: <None>
        """
        s3_object = self._get_object(s3_directory, filename)

        # If the file exists in S3
        if s3_object is not None:

            # Create a filepath from the source directory and filename.
            dst_filepath = posix_filepath(dst_directory, filename)

            # If the file already exists copy the existing file contents
            # for data recovery.
            if os.path.exists(dst_filepath) is True:
                with open(dst_filepath, "rb") as rf:
                    backup_data = rf.read()

            # Create the destination filepath if it doesn't exist
            elif os.path.exists(dst_directory) is not True:
                os.makedirs(dst_directory)

            # Download the target file.
            try:
                s3_object.download_file(dst_filepath)
            except Exception as err:
                result = False
                debugLogger.error("Download file failed.", err)
                with open(dst_filepath, "wb") as wf:
                    wf.write(backup_data)
            else:
                result = True

        # If the file doesn't exist in S3
        else:
            result = None

        return result

    def delete_file(self, s3_directory, filename):
        """
        Delete the file at 's3_directory/filename'.

        This method is currently written to operate with S3 where
        versioning is not enabled. If versioning is enabled delete
        functionality behaves a little differently and this method
        may not return accurate information.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.delete

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        Returns
        =======
        File exists in S3, Delete successful: <boolean> True

        File exists in S3, Delete failed: <boolean> False
            # TODO: (AHA) HOW IS THIS SITUATION HANDLED?

        File does not exist in S3: <None>
        """
        s3_object = self._get_object(s3_directory, filename)

        # If the file exists in S3
        if s3_object is not None:

            # Delete the target file.
            try:
                response = s3_object.delete()
            except Exception as err:
                debugLogger.error("Delete file failed.", err)
                result = False
            else:
                result = True

        # If the file doesn't exist in S3
        else:
            result = None

        return result

    #------------------------------------------------------------------
    def get_attribute(self, attribute, s3_directory, filename, renew=True):

        s3_object = self._get_object(s3_directory, filename, renew)

        if s3_object is not None:

            if attribute == "content_length":
                result = s3_object.content_length

            elif attribute == "content_type":
                result = s3_object.content_type

            elif attribute == "e_tag":
                result = s3_object.e_tag

            elif attribute == "expiration":
                result = s3_object.expiration

            elif attribute == "expires":
                result = s3_object.expires

            elif attribute == "last_modified":
                result = s3_object.last_modified

            elif attribute == "version_id":
                result = s3_object.version_id

            else:
                result = None

        else:
            result = None

        return result

    def get_size(self, s3_directory, filename, renew=True):
        """
        Return the size in bytes of an S3 Object.

        Description
        ===========
        Retrieve an S3 Object and return the result of the
        content_length method.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists: <integer>
            The size of the S3 object in bytes.
        If the file doesn't exist: <None>
        """
        size_in_bytes = self.get_attribute("content_length", s3_directory, filename, renew)
        return size_in_bytes

    def get_etag(self, s3_directory, filename, renew=True):
        """
        Return the ETag (entity tag) of an S3 Object.

        Description
        ===========
        Retrieve an S3 Object and return the result of the e_tag method.
        The returned result will be an MD5 checksum for all files which
        were uploaded in a single part.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists: <string>
            A character string, representing the MD5 checksum if the
            file was uploaded in a single part.
        If the file doesn't exist: <None>
        """
        etag = self.get_attribute("e_tag", s3_directory, filename, renew)
        return etag

    def get_content_type(self, s3_directory, filename, renew=True):
        """
        Return the MIME type of the S3 Object.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists: <string>
            Multipurpose internet mail extension (MIME) of the content
            type.
        If the file doesn't exist: <None>
        """
        content_type = self.get_attribute("content_type", s3_directory, filename, renew)
        return content_type

    def get_version(self, s3_directory, filename, renew=True):
        """
        Return the version of the S3 Object.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists: <string>
            A 32-character (alpha-numeric and special characters)
            string.

        If the file doesn't exist: <None>
        """
        version_id = self.get_attribute("version_id", s3_directory, filename, renew)
        return version_id

    def get_expiration(self, s3_directory, filename, renew=True):
        """
        Return the expiration information of an S3 Object.

        Description
        ===========
        If the object expiration is configured, the response includes
        the expiry-date and rule-id key-value pairs providing object
        expiration information. The value of the rule-id is URL
        encoded.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists and expiration is configured: <string>
            Unknown format - needs to be tested
        If the file exists and expiration is not configured: <None>
        If the file doesn't exist: <None>
        """
        expiration_data = self.get_attribute("expiration", s3_directory, filename, renew)
        return expiration_data

    def get_expiry_date(self, s3_directory, filename, renew=True):
        """
        Return the date and time when the S3 Object will expire.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists and expiration is configured: <datetime>
            Unknown format - needs to be tested
        If the file exists and expiration is not configured: <None>
        If the file doesn't exist: <None>
        """
        expiry_date = self.get_attribute("expires", s3_directory, filename, renew)
        return expiry_date

    def get_modified_date(self, s3_directory, filename, renew=True):
        """
        Return the date and time when the S3 Object was last modified.

        Parameters
        ==========
        s3_directory: <string>
            Filepath to the directory in S3 where 'filename' is found.

        filename: <string>
            Name of the file of interest, including file extension.

        renew: <boolean>
            Set True to always submit a server request for the S3
            Object. Set False to only request an object if the key has
            changed from the since the last _get_object() call.

        Returns
        =======
        If the file exists: <datetime>
        If the file doesn't exist: <None>
        """
        last_modified_date = self.get_attribute("last_modified", s3_directory, filename, renew)
        return last_modified_date


#######################################################################
def posix_filepath(*args):
    """
    Return a normalised filepath format.

    Description
    ===========
    Create a posix format filepath. All backslahes are replaced with
    forward slashes which is the format used by AWS S3 keys.

    Parameters
    ==========
    args: series of <strings>
        Folder and file names in the order they should be concatenated.

    Returns
    =======
    <string>: a filepath with only '/' for separators.

    """
    path = os.path.join(*args)

    return path.replace("\\", "/")


########################################################################
if __name__ == "__main__":

    import dotenv  # python3 -m pip install python-dotenv
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    # Collect login details from .env file
    S3_ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
    S3_SECRET_KEY = os.environ["S3_SECRET_KEY"]
    S3_BUCKET = os.environ["S3_BUCKET"]

    TEST_FILE = "test.txt"
    LOCAL_DIRECTORY = "./s3files"
    S3_DIRECTORY = "test-dir"
    LOCAL_FILEPATH = posix_filepath(LOCAL_DIRECTORY, TEST_FILE)
    S3_FILEPATH = posix_filepath(S3_BUCKET, S3_DIRECTORY, TEST_FILE)

    print("\n Local: {}".format( LOCAL_FILEPATH))
    print("Remote: {}\n".format(S3_FILEPATH))

    # Create an Amazon Web Services S3 Client
    s3_client = S3Session(S3_BUCKET, S3_ACCESS_KEY, S3_SECRET_KEY)

    # # Run some basic tests on the code.
    # from tests import BadlyWrittenTestClass
    # Tester = BadlyWrittenTestClass(s3_client, LOCAL_DIRECTORY, S3_BUCKET, S3_DIRECTORY, TEST_FILE)
    # Tester.test_noLocal_noRemote()
    # Tester.test_yesLocal_noRemote()
    # Tester.test_noLocal_yesRemote()
    # Tester.test_yesLocal_yesRemote()
    # Tester.test_objectAttributeDump()
    # print("")
