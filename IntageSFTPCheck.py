from SGTAMProdTask import SGTAMProd
from config import SGTAM_log_config
import logging
import config
from datetime import date, timedelta, datetime, time
import json
import pysftp
#import paramiko

files_ok = {}
files_not_ok = {}
files_not_found = {}

def connect_check_sftp():
    #ignore known hosts check
    cnOpts = pysftp.CnOpts()
    cnOpts.hostkeys = None

    #print(paramiko.__version__) #have to downgrade to paramiko version 2.8.1 else will not work, pip install paramiko==2.8.1
    
    if (time(hour=0, minute=0, second=0, microsecond=0) <= config.timenow <= time(hour=0, minute=59, second=59, microsecond=0)):
        logging.info("Please start checking from 1:00AM to 11:59PM, thank you!")    
    else:
        with pysftp.Connection(host=config.hostname, username=config.user, private_key=config.private_key_file_path, cnopts=cnOpts) as sftp:
            logging.info("\nAccessing Intage SFTP.")
            logging.info("Connected.")

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
                                logging.info(file_subkeys[0][i]+ " not found!")
                                files_not_found['File'+str(i+1)] = {
                                        'Name':file_subkeys[0][i],
                                        'Expected minimum filesize (byte)':file_subkeys[1][i]
                                    }


    if len(files_not_ok)==0 and len(files_not_found)==0 and len(files_ok)>=1 :
        config.SGTAM_log_config['logMsg'] = "Intage SFTP check completed, no missing file and all files above minimum size, no email will be sent out."
        logging.info(config.SGTAM_log_config['logMsg'])
        logging.info("All files are ok: ")
        logging.info(json.dumps(files_ok, indent=2, default=str))

    elif (len(files_not_ok)>=1 or len(files_not_found)>=1) and len(files_ok)>=1:
        config.SGTAM_log_config['statusFlag'] = 2
        config.SGTAM_log_config['logMsg'] = "Some of the files might be missing or having the below minimum file size."
        config.email['subject'] = "[ERROR] Intage SFTP Check"
        config.email['body'] = f"Some of the Intage files might be missing or having the below minimum file size, please check.\nInvalid File Size: \n{json.dumps(files_not_ok, indent=2, default=str)}\n\nMissing Files: \n{json.dumps(files_not_found, indent=2, default=str)}\n\nFiles OK: \n{json.dumps(files_ok, indent=2, default=str)}\n*This is an auto generated email, do not reply to this email."
        logging.warning(config.SGTAM_log_config['logMsg'])
        logging.info("Files with below minimum size threshold: ")
        logging.info(json.dumps(files_not_ok, indent=2, default=str))
        logging.info("Missing Files: ")
        logging.info(json.dumps(files_not_found, indent=2, default=str))
        logging.info("Files that are ok:")
        logging.info(json.dumps(files_ok, indent=2, default=str))

    elif (len(files_not_ok)>=1 or len(files_not_found)>=1) and len(files_ok)==0:
        config.SGTAM_log_config['statusFlag'] = 2
        config.SGTAM_log_config['logMsg'] = "No files passed the size requirement or they are missing from the SFTP, please check."
        config.email['subject'] = "[ERROR] Intage SFTP Check"
        config.email['body'] = f"No files passes the requirement as some of them are missing or having below minimum file size, please check.\nInvalid File Size: \n{json.dumps(files_not_ok, indent=2, default=str)}\n\nMissing Files: \n{json.dumps(files_not_found, indent=2, default=str)}\n*This is an auto generated email, do not reply to this email."
        logging.warning(config.SGTAM_log_config['logMsg'])
        logging.info("Missing Files: ")
        logging.info(json.dumps(files_not_found, indent=2, default=str))
        logging.info("Files with file sizes below minimum threshold:")
        logging.info(json.dumps(files_not_ok, indent=2, default=str))

            
if __name__ == '__main__':

    # setup logging
    logging.basicConfig(
      filename= f"log\{datetime.now().strftime('%Y%m%d%H%M')}_IntageSFTPCheck.log",
      format='%(asctime)s %(levelname)s %(message)s',
      level=logging.INFO
    )

    s = SGTAMProd()
    config.SGTAM_log_config['statusFlag'], config.SGTAM_log_config['logID']  = s.insert_tlog(**config.SGTAM_log_config)

    logging.info("Intage SFTP Check Started.")

    try:
        connect_check_sftp()
    except Exception as e:
        config.SGTAM_log_config['statusFlag'] = 2
        config.SGTAM_log_config['logMsg'] = "[Error] There is/are exception(s), please check."
        config.email['subject'] = "[ERROR] Intage SFTP Check"
        config.email['body'] = f"{config.SGTAM_log_config['logMsg']}\n{e}"
        logging.error(config.SGTAM_log_config['logMsg'])
        logging.error(e)

    finally:
        if config.SGTAM_log_config['statusFlag'] in [2]:
            s.send_email(**config.email)
            logging.info('Email sent.')
            s.update_tlog(**config.SGTAM_log_config)
            logging.info('SGTAM log updated.')
        else:
            s.update_tlog(**config.SGTAM_log_config)
            logging.info('SGTAM log updated.')    