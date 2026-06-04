import base64
import io
import logging
import paramiko


class _ParamikoSFTPConnection:
    def __init__(self, transport, sftp):
        self._transport = transport
        self._sftp = sftp

    def close(self):
        try:
            self._sftp.close()
        finally:
            self._transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __getattr__(self, name):
        return getattr(self._sftp, name)


class SFTPClient:
    def __init__(self, host, username, password=None, key_base64=None, key_pass=None):
        self.host = host
        self.username = username
        self.password = password

        if key_base64:
            self.key = self._make_key(key_base64, key_pass)
        else:
            self.key = None

        self.logger = logging.getLogger(__name__)

    def _make_key(self, key_base64, key_pass=None):
        decoded_key = base64.b64decode(key_base64).decode("utf-8")
        private_key_file = io.StringIO()
        private_key_file.write(decoded_key)
        private_key_file.seek(0)
        return paramiko.RSAKey.from_private_key(private_key_file, password=key_pass)

    def get_connection(self):
        try:
            transport = paramiko.Transport((self.host, 22))
            if self.key is not None and self.password is not None:
                transport.connect(username=self.username, password=self.password, pkey=self.key)
            elif self.key is not None:
                transport.connect(username=self.username, pkey=self.key)
            else:
                transport.connect(username=self.username, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(transport)
            return _ParamikoSFTPConnection(transport, sftp)
        except Exception as e:
            self.logger.error(e)
            return None
