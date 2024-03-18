import paramiko
import config

print(paramiko.__version__) #have to downgrade to paramiko version 2.8.1 else will not work, pip install paramiko==2.8.1

host = "external-transfer1-production.hyperlane.gfk.com"
usr = "gxl-admin"
pvkey = "./id_rsa"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key = paramiko.RSAKey.from_private_key_file(pvkey)
ssh.connect(hostname=host, username=usr, pkey=key)

print('connected')

stdin, stdout, stderr = ssh.exec_command('ls')
print (stdout.readlines())

ssh.close()


