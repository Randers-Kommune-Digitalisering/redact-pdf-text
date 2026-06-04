from utils.sftp import SFTPClient
from unittest.mock import patch, MagicMock


@patch('paramiko.SFTPClient.from_transport')
@patch('paramiko.Transport')
def test_get_connection_success(mock_transport_cls, mock_from_transport):
    client = SFTPClient('host', 'user', 'pass')
    mock_transport = MagicMock()
    mock_transport_cls.return_value = mock_transport
    mock_from_transport.return_value = MagicMock()

    result = client.get_connection()

    assert result is not None
    mock_transport_cls.assert_called_once_with(('host', 22))
    mock_transport.connect.assert_called_once_with(username='user', password='pass')
    mock_from_transport.assert_called_once_with(mock_transport)


@patch('paramiko.Transport')
def test_get_connection_exception(mock_transport_cls):

    client = SFTPClient('host', 'user', 'pass')
    mock_transport_cls.side_effect = Exception("Connection failed")

    result = client.get_connection()

    assert result is None


@patch('base64.b64decode')
@patch('paramiko.RSAKey.from_private_key')
def test_make_key(mock_from_private_key, mock_b64decode):
    mock_b64decode.return_value = b'decoded_key'
    mock_from_private_key.return_value = 'RSAKey'

    client = SFTPClient('host', 'user', key_base64='base64key', key_pass='keypass')

    assert client.key == 'RSAKey'
    mock_b64decode.assert_called_once_with('base64key')
    mock_from_private_key.assert_called_once()
