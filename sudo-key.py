#!/usr/bin/python

from StringIO import StringIO
import paramiko 

class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, port, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            print key
            f = open(key,'r')
            s = f.read()
            #key = paramiko.DSSKey.from_private_key(StringIO(key), password=passphrase)
            #key = paramiko.RSAKey.from_private_key(StringIO(s), password=passphrase)
            key = paramiko.DSSKey.from_private_key(StringIO(s), password=passphrase)
            f.close()
        self.client.connect(host, port, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(), 
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

if __name__ == "__main__":
    client = SshClient(host='10.68.3.2', port=22, username='liangshuhua', password='llll',key='/usr/local/Auto_deploy/keydir/id_rsa',passphrase='lllllll') 
    try:
       ret = client.execute('ls /data', sudo=True)
       print "  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"]
    finally:
      client.close() 
