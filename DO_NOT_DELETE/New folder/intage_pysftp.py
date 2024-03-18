import pysftp
import config
#import paramiko
from datetime import date, timedelta, datetime, time
import json

files_ok = {}
files_not_ok = {}

def connect_check_sftp():
    #ignore known hosts check
    cnOpts = pysftp.CnOpts()
    cnOpts.hostkeys = None

    #print(paramiko.__version__) #have to downgrade to paramiko version 2.8.1 else will not work, pip install paramiko==2.8.1
    
    if (time(hour=0, minute=0, second=0, microsecond=0) <= config.timenow <= time(hour=0, minute=59, second=59, microsecond=0)):
        print("Please start checking from 1:00AM to 11:59PM, thank you!")    
    else:
        with pysftp.Connection(host=config.hostname, username=config.user, private_key=config.private_key_file_path, cnopts=cnOpts) as sftp:
            print("\nAccessing Intage SFTP.")
            print("Connected.")
            print()

            for period, period_subkeys in config.timings.items():
                if(time(hour=period_subkeys['h1'], minute=period_subkeys['m1'], second=period_subkeys['s1'], microsecond=period_subkeys['ms1']) < config.timenow < time(hour=period_subkeys['h2'], minute=period_subkeys['m2'], second=period_subkeys['s2'], microsecond=period_subkeys['ms2'])):
                    for file, file_subkeys in period_subkeys['files'].items():
                        #print(file_subkeys)
                        for i in range(len(file_subkeys[0])):
                            if sftp.exists(file_subkeys[0][i]):
                                file_full_info = str(sftp.lstat(file_subkeys[0][i]))
                                file_full_info_split = file_full_info.split()
                                fsize = int(file_full_info_split[4])
                                if(fsize < file_subkeys[1][i]):
                                
                                    files_not_ok['File'+str(i+1)] = {

                                        'Name':file_subkeys[0][i],
                                        'File size (byte)':fsize,
                                        'Expected minimum filesize (byte)':file_subkeys[1][i]
                                    }
                                else:
                                    files_ok['File'+str(i+1)] = {
                                        'Name':file_subkeys[0][i],
                                        'File size (byte)':fsize,
                                        'Expected minimum filesize (byte)':file_subkeys[1][i]
                                    }
                            else:
                                print(file_subkeys[0][i]+ " not found!")
            
    if len(files_not_ok)==0 and len(files_ok)>=1:
        print("All files are present in SFTP and are above minimum size threshold.\n")
        print(json.dumps(files_ok, indent=2, default=str))
    elif len(files_not_ok)>=1 and len(files_ok)>=1:
        print("Files with file sizes below minimum threshold:")
        print(json.dumps(files_not_ok, indent=2, default=str))
        print("Files that are ok:")
        print(json.dumps(files_ok, indent=2, default=str))
    elif len(files_not_ok)>=1 and len(files_ok)==0:
        print("All files are below minimum size threshold.")
        print(json.dumps(files_not_ok, indent=2, default=str))
                    
if __name__ == '__main__':
    connect_check_sftp()