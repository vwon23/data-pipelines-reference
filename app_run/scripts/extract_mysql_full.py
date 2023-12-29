import os, sys
import csv

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


## Connect to source and extract data
m_query = "SELECT * FROM Orders;"
local_filename = "order_extract.csv"

source_connection = cf.connect_mysql()
m_cursor = source_connection.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter='|')
    csv_w.writerows(results)

fp.close()
m_cursor.close()
source_connection.close()

