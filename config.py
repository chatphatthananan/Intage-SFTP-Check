from datetime import date, timedelta, datetime

hostname = 'xxx'
user = 'xxx'
private_key_file_path = r"D:\SGTAM_DP\Working Project\Intage SFTP Check\DO_NOT_DELETE\id_rsa"

today = date.today().strftime("%Y-%m-%d")
yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
next_day = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
tdy_minusOne = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
tdy_minusTwo = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
tdy_addonnwm_minusOne = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
tdy_addonnwm_minusTwo = (date.today() - timedelta(days=2)).strftime("%Y%m%d")
timenow = datetime.now().time()

#Check locations
dir_addon_dayMinusTwo = "/gxl-intage/data/exports/addon/X-2/"
dir_addon_dayMinusOne = "/gxl-intage/data/exports/addon/X-1/"
dir_nwm_dayMinusTwo = "/gxl-intage/data/exports/nwm/X-2/"
dir_nwm_dayMinusOne = "/gxl-intage/data/exports/nwm/X-1/"
dir_ldm = "/gxl-intage/data/exports/ldm/"

#ldm 
intage_ldm_install_status_tdy = f'install_status_2_{today}.tsv'                    #check at 2:30pm
intage_ldm_activity_history_tdy = f'activity_history_daily_2_{today}.tsv'          #check at 2:30pm
intage_ldm_waypoint_history_tdy = f'waypoint_history_daily_2_{today}.tsv'          #check at 2:30pm
intage_ldm_install_status_dayPlusOne = f'install_status_{today}.tsv'                   #check at 1:35am next day
intage_ldm_activity_history_dayPlusOne = f'activity_history_daily_{today}.tsv'         #check at 1:35am next day
intage_ldm_waypoint_history_dayPlusOne = f'waypoint_history_daily_{today}.tsv'         #check at 1:35am next day

#addon
intage_addon_day_minus_2 = f'jp_intage_addon{tdy_addonnwm_minusTwo}.csv.gz'                 #check at 8:15am
intage_addon_day_minus_1 = f'jp_intage_addon{tdy_addonnwm_minusOne}.csv.gz'                 #check at 11:15am

#nwm
intage_nwm_day_minus_2 = f'jp_intage_nwm{tdy_addonnwm_minusTwo}.csv.gz'                     #check at 1:00pm
intage_nwm_day_minus_1 = f'jp_intage_nwm{tdy_addonnwm_minusOne}.csv.gz'                     #check at 5:00pm

files_to_check_135am = [(dir_ldm+intage_ldm_install_status_dayPlusOne), (dir_ldm+intage_ldm_activity_history_dayPlusOne), (dir_ldm+intage_ldm_waypoint_history_dayPlusOne)]
files_to_check_815am = [(dir_addon_dayMinusTwo+intage_addon_day_minus_2)]
files_to_check_1115am = [(dir_addon_dayMinusTwo+intage_addon_day_minus_2),(dir_addon_dayMinusOne+intage_addon_day_minus_1)]
files_to_check_1pm = [(dir_addon_dayMinusTwo+intage_addon_day_minus_2),(dir_addon_dayMinusOne+intage_addon_day_minus_1),(dir_nwm_dayMinusTwo+intage_nwm_day_minus_2)]
files_to_check_230pm = [(dir_addon_dayMinusTwo+intage_addon_day_minus_2),(dir_addon_dayMinusOne+intage_addon_day_minus_1),(dir_nwm_dayMinusTwo+intage_nwm_day_minus_2),(dir_ldm+intage_ldm_install_status_tdy), (dir_ldm+intage_ldm_activity_history_tdy), (dir_ldm+intage_ldm_waypoint_history_tdy)]
files_to_check_5pm = [(dir_addon_dayMinusTwo+intage_addon_day_minus_2),(dir_addon_dayMinusOne+intage_addon_day_minus_1),(dir_nwm_dayMinusTwo+intage_nwm_day_minus_2),(dir_ldm+intage_ldm_install_status_tdy), (dir_ldm+intage_ldm_activity_history_tdy), (dir_ldm+intage_ldm_waypoint_history_tdy),(dir_nwm_dayMinusOne+intage_nwm_day_minus_1)]

expected_file_sizes_135am = [40000000,0,1750000]

#Uncomment and use these 5 threshold after Friday 5pm run
expected_file_sizes_815am = [120000000]
expected_file_sizes_1115am = [120000000]+[120000000]
expected_file_sizes_1pm = [120000000]+[120000000]+[7000000000]
expected_file_sizes_230pm = [120000000]+[120000000]+[7000000000]+[40000000,0,1750000]
expected_file_sizes_5pm = [120000000]+[120000000]+[7000000000]+[40000000,0,1750000]+[7000000000]

#delete these threshold below after Friday 5pm run and use above threshold instead
#expected_file_sizes_815am = [117000000]
#expected_file_sizes_1115am = [117000000]+[115000000]
#expected_file_sizes_1pm = [117000000]+[115000000]+[7000000000]
##expected_file_sizes_230pm = [117000000]+[115000000]+[7000000000]+[40000000,0,2300000]
#expected_file_sizes_5pm = [117000000]+[115000000]+[7000000000]+[40000000,0,2300000]+[7000000000]


timings = {

    'period1' : {
        'h1':1,
        'm1':0,
        's1':0,
        'ms1':0,
        'h2':7,
        'm2':59,
        's2':59,
        'ms2':0,
        'files':{
            'file_names':[files_to_check_135am,expected_file_sizes_135am]
            #,'expected_file_sizes':expected_file_sizes_1am
        }
    }
    ,'period2' : {
        'h1':8,
        'm1':0,
        's1':0,
        'ms1':0,
        'h2':11,
        'm2':14,
        's2':59,
        'ms2':0,
        'files':{
            'file_names':[files_to_check_815am,expected_file_sizes_815am]
            #,'expected_file_sizes':expected_file_sizes_815am
        }
    },
    'period3' : {
        'h1':11,
        'm1':15,
        's1':0,
        'ms1':0,
        'h2':12,
        'm2':59,
        's2':59,
        'ms2':0,
        'files':{
            'file_names':[files_to_check_1115am,expected_file_sizes_1115am]
            #,'expected_file_sizes':expected_file_sizes_1115am
        }
    },
    'period4' : {
        'h1':13,
        'm1':0,
        's1':0,
        'ms1':0,
        'h2':14,
        'm2':29,
        's2':59,
        'ms2':0,
        'files':{
            'file_names':[files_to_check_1pm,expected_file_sizes_1pm]
            #,'expected_file_sizes':expected_file_sizes_1pm
        }
    },
    'period5' : {
        'h1':14,
        'm1':30,
        's1':0,
        'ms1':0,
        'h2':16,
        'm2':59,
        's2':59,
        'ms2':0,
        'files':{
            'file_names':[files_to_check_230pm,expected_file_sizes_230pm]
            #,'expected_file_sizes':expected_file_sizes_230pm
        }
    },
    'period6' : {
        'h1':17,
        'm1':0,
        's1':0,
        'ms1':0,
        'h2':23,
        'm2':59,
        's2':59,
        'ms2':0,
        'files': {
            'file_names':[files_to_check_5pm,expected_file_sizes_5pm]
            #,'expected_file_sizes':expected_file_sizes_5pm
        }
        
    }
}

email = {
        'sender' : 'xxx',
        'to' : 'xxx',
        'subject' : '',
        'body' : '',
        'is_html' : False
    }


SGTAM_log_config = {
                    'logTaskID' : 113,
                    'statusFlag' : 2,
                    'logMsg' : 'Intage SFTP Check Started.',
                    'logID' : None
                }
