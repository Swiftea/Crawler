#!/usr/bin/python3

from socket import timeout
import paramiko


class SFTPError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr('SFTP error: ' + self.message)


class SFTPManager(object):
    """Class to connect to a sftp server with SSH using paramiko.

    :param host: hostname server
    :type host: str
    :param user: username to use for connexion
    :type user: str
    :param password: password to use for connexion
    :type password: str

    """
    def __init__(self, host, user='', password=''):
        self.host = host
        self.user = user
        self.password = password

        self.transport = None
        self.sftp = None

    def connexion(self):
        """Connect to server."""
        try:
            self.transport = paramiko.Transport((self.host, 2222))
            self.transport.connect(username=self.user, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except timeout:
            raise SFTPError('Timeout error')
        except Exception as error:
            raise SFTPError('connect; ' + str(error))

    def disconnect(self):
        """Close connexion to sftp server."""
        self.sftp.close()
        self.transport.close()
        self.sftp = None
        self.transport = None


    def cd(self, path):
        """Set the current directory on the server.

        :param path: path to set
        :type path: str

        """
        try:
            self.sftp.chdir(path)
        except Exception as error:
            raise SFTPError('cd; {} {}'.format(path, str(error)))

    def mkdir(self, dirname):
        """Create directory."""
        try:
            self.sftp.mkdir(dirname)
        except Exception as error:
            raise SFTPError('mkdir; ' + str(error))

    def listdir(self, path='.'):
        """Return a list containing the names of the entries in the given path."""
        try:
            result = self.sftp.listdir(path)
        except Exception as error:
            raise SFTPError('lisdir; ' + str(error))
        else:
            # Must be test:
            return result

    def listdir_attr(self, path='.'):
        """List the given path.

        Return the names and other informations about entries.

        """
        try:
            result = self.sftp.listdir_attr(path)
        except Exception as error:
            raise SFTPError('lisdir attrs; ' + str(error))
        else:
            return result

    def put(self, local_filename, server_filename):
        """Upload a file into server.

        :param local_filename: local filename to upload
        :type local_filename: str
        :param server_filename: server filename to upload
        :type server_filename: str
        :return: ok or error message

        """
        try:
            self.sftp.put(local_filename, server_filename)
        except Exception as error:
            raise SFTPError('upload; ' + str(error))

    def get(self, local_filename, server_filename):
        """Download a file from server.

        :param local_filename: local filename to create
        :type local_filename: str
        :param server_filename: server filename to download
        :type server_filename: str
        :return: server ok or error message

        """
        try:
            self.sftp.get(server_filename, local_filename)
        except Exception as error:
            raise SFTPError('download; ' + str(error))

    def countfiles(self, path='.'):
        """Count the file in the given path.

        :param path: path to count
        :type path: str
        :return: number of files

        """
        nb_files = int()
        infos = self.listdir_attr(path)
        for info in infos:
            if '.' in info.filename:
                nb_files += 1
            else:
                nb_files += self.countfiles(path + '/' + info.filename)
        return nb_files
