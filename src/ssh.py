import traceback
from io import StringIO

from loguru import logger as log
from paramiko import SSHClient, AutoAddPolicy, ssh_exception, RSAKey


class SSH(object):
    """ssh client"""

    def __init__(self, host, port, user, password=None, ssh_key=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssh_key = ssh_key
        self._init_client()

    def _init_client(self):
        self.client = None
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy)

    def connect_via_pw(self, password: str):
        return self._connect(password=password)

    def connect_via_key_file(self, key_file: str):
        return self._connect(key_file=key_file)

    def connect_via_key_content(self, key_content: str):
        rsa_private_key = self._get_rsa_key_from_string(key_content)
        return self._connect(key_content=rsa_private_key)

    def _connect(self, **kwargs) -> bool:
        """connect to SSH client

        Keyword Args:
            password: ssh user password (str)
            key_file: private key file path for ssh user (str)
            key_content: private key file content for ssh user (str)
        Returns:
            connection status of this SSH client (bool)
        """
        auth_methods = [meth for meth in kwargs if meth]
        ssh_info = f'{self.user}@{self.host}:{self.port}'
        try:
            self.client.connect(
                hostname=self.host, port=self.port, username=self.user,
                password=kwargs.get('password'), pkey=kwargs.get('key_content'),
                key_filename=kwargs.get('key_file'), look_for_keys=True)
            log.info(f'ssh {ssh_info} SUCCESS via {auth_methods}.')
        except ssh_exception.AuthenticationException:
            log.error(f'ssh {ssh_info} FAILED (Authentication Failed), '
                      f'please check ssh username={self.user} and auth method={auth_methods}!')
        except Exception as e:
            log.error(f'ssh {ssh_info} FAILED, detail: {str(e)}')
            log.error(traceback.format_exc())
        finally:
            return self.is_connected()

    def disconnect(self):
        if self.is_connected():
            self.client.close()
        self._init_client()

    def is_connected(self):
        transport = self.client.get_transport() if self.client else None
        return bool(transport and transport.is_active())

    def exec_cmd(self, cmd):
        if self.is_connected():
            stdin, stdout, stderr = self.client.exec_command(cmd)
            cmd_result = {'out': stdout.readlines(),
                          'err': stderr.readlines(),
                          'retval': stdout.channel.recv_exit_status()}
            return cmd_result
        else:
            raise ssh_exception.SSHException('SSH client not connected!')

    @staticmethod
    def _get_rsa_key_from_string(key_content_str: str):
        private_key_io_str = StringIO()
        private_key_io_str.write(key_content_str)
        private_key_io_str.seek(0)
        return RSAKey.from_private_key(private_key_io_str)

    def update_authorized_keys_from_private_key(self, private_key_content: str):
        if self.is_connected():
            rsa_private_key = self._get_rsa_key_from_string(private_key_content)
            rsa_public_key = rsa_private_key.get_base64()
            self.update_authorized_keys_from_public_key(rsa_public_key)
        else:
            raise ssh_exception.SSHException('SSH client not connected!')

    def update_authorized_keys_from_public_key(self, public_key_content: str):
        if self.is_connected():
            key_record = f'ssh-rsa {public_key_content}'
            key_summary = f'{public_key_content[:5]}...{public_key_content[-5:]}'
            result = self.exec_cmd(f'cat ~/.ssh/authorized_keys | grep \"{key_record}\"')
            if not result['err'] and key_record in [s.strip() for s in result['out']]:
                log.warning(f'Already authorized for this ssh key, public={key_summary}')
            else:
                log.info(f'Ready to authorize for this ssh key, public={key_summary}')
                self.exec_cmd(f'echo ssh-rsa {public_key_content} >> ~/.ssh/authorized_keys')
                self.exec_cmd(f'chmod 600 .ssh/authorized_keys')
        else:
            raise ssh_exception.SSHException('SSH client not connected!')
