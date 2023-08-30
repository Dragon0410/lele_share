# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/30
# create time: 20:21
# create author: 93207
# describe:
import socket
import sys
import time
import traceback

import paramiko
from loguru import logger


class SSH2Client():

    def __init__(self, hostname=None, port=22, username=None, password=None, **server_info):
        super().__init__()
        if all([hostname, port, username, password]):
            self.hostname = hostname
            self.port = port
            self.username = username
            self.password = password

        elif server_info:
            self.hostname = server_info.get('hostname')
            self.port = server_info.get('port')
            self.username = server_info.get('username')
            self.password = server_info.get('password')
        else:
            raise Exception("没有发现参数")
        self._ssh_client = None
        self._sftp_client = None
        self._channel_client = None

    def _connect(self):
        try:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(hostname=self.hostname, port=self.port, username=self.username,
                                     password=self.password,
                                     timeout=60)
        except Exception as e:
            error_msg = f"链接{self.hostname}失败"
            logger.info(error_msg)
            raise

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if all([exc_type, exc_val, exc_tb]):
            logger.error(f"{exc_type, exc_val, exc_tb}")
        self._close()

    def _close(self):
        if self._sftp_client:
            self._sftp_client.close()
        if self._ssh_client:
            self._ssh_client.close()

    def execute_command(self, cmd) -> tuple:
        stdin, stdout, stderr = self._ssh_client.exec_command(cmd)

        results = ''
        if stdout:
            for line in iter(stdout):
                results += line

        if stderr:
            for line in iter(stderr):
                results += line

        status = stdout.channel.exit_status
        execute_status = not status

        return execute_status, results

    def __match(self, out_str, end_str) -> (bool, str):
        for i in end_str:
            if out_str.endswith(i):
                return True, out_str
        return False, out_str

    def __recv(self, channel_client, end_str, timeout):
        result = ''
        out_str = ''
        max_wait_time = timeout * 100

        channel_client.settimeout(timeout)

        while max_wait_time > 0:
            try:
                out = channel_client.recv(1024 * 1024).decode()

                if not out:
                    continue

                out_str += out

                match, result = self.__match(out_str, end_str)
                if match:
                    return result
                else:
                    max_wait_time -= 50
            except socket.timeout:
                max_wait_time -= 50

        raise Exception("recv data timeout")

    def channel_command(self, cmd, end_str=('$ ', '# ', '? ', '% '), timeout=30):
        if not self._ssh_client:
            self._connect()

        if not self._channel_client:
            self._channel_client = self._ssh_client.invoke_shell()
            time.sleep(2)

            out_put = self._channel_client.recv(1024).decode()

        if not cmd.endswith('\n'):
            cmd = f"{cmd}\n"
        logger.info(f"执行命令：{cmd}")
        self._channel_client.send(cmd)

        return self.__recv(self._channel_client, end_str, timeout)


def main():
    try:
        server_info_dict = {
            'hostname': '192.168.172.129',
            'port': 22,
            'username': 'lele',
            'password': 'wang3180'
        }

        with SSH2Client(**server_info_dict) as ssh:

            res1 = ssh.channel_command("pwd")
            res2 = ssh.channel_command("cd Downloads")
            res3 = ssh.channel_command("pwd")
            logger.info(res1)
            logger.info(res2)
            logger.info(res3)


    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        logger.info(" 程序结束 ")
        sys.exit()


if __name__ == "__main__":
    main()
