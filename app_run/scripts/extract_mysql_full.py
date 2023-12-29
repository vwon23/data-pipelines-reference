import os, sys

## Find path of the script then find the path of parent folder and add it to system path ##
path_script = os.path.abspath(__file__)
path_app_run = os.path.dirname(os.path.dirname(path_script))
sys.path.append(path_app_run)

## use common functions to initalize global variable ##
import utilities.common_functions as cf
cf.init(path_app_run)

cf.get_config()
cf.get_current_datetime()

logname = 'extract_mysql'
logfile_name = f'{logname}_{cf.gvar.current_date_pst}.log'
logger = cf.set_logger(logname, logfile_name)