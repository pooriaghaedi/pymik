import paramiko
import socket
import os
import re
import datetime
import time as ti


class mikssh():
    def connect(self, address, username, password):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, int(22)))
            s.shutdown(2)
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=address, username=username, password=password, timeout=10)
            remote = self.ssh.invoke_shell()
            print("connected")
            return (remote)
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to {}".format(address))
        except Exception as e:
            print(e)

    def backup(self, name):
        try:
            rfile = '/{}.rsc'.format(name)
            # stdin, stdout, stderr = self.ssh.exec_command("/system backup save name={} dont-encrypt=yes".format(name) + "\n")
            stdin, stdout, stderr = self.ssh.exec_command("/export file={}".format(name) + "\n")
            print("------------")
            ftp_client = self.ssh.open_sftp()
            ftp_client.get('{}'.format(rfile), '/path/to/backup/{}'.format(rfile))
            ti.sleep(5)
            ftp_client.close()
        except Exception as e:
            print(e)

    def update(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command("system resource print" + "\n")
            output = stdout.read()
            mips = (re.search(r'mipsbe', str(output)))
            tile = (re.search(r'tile', str(output)))
            ppc = (re.search(r'powerpc', str(output)))
            if mips:
                name = "mipsbe.npk"
                print(name)
            elif tile:
                name = "tile.npk"
                print(name)
            elif ppc:
                name = "powerpc.npk"
                print(name)
            print("------------")
            ftp_client = self.ssh.open_sftp()
            ftp_client.put(r"/path/to/files/{}".format(name), '{}'.format(name))
            ti.sleep(2)
            ftp_client.close()
        except Exception as e:
            print(e)
            pass

    def generate_file_name(self, address):
        try:
            stdin, stdout, stderr = self.ssh.exec_command("/system identity print" + "\n")
            output = stdout.read()
            print(re.search(r'name:.*', str(output)).group())
            identity = str(output).split('name: ')[1]
            name = identity[:14]
            return (name)
        except Exception as e:
            print(e)

    def send_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command + "\n")
            output = stdout.read()
            output = (str(output))
            return output
        except Exception as e:
            print(e)
