import os, sys
import csv
#import boto3

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import row_event
import pymysqlreplication

## Find path of the script then find the path of parent folder and add it to system path ##
path_script = os.path.abspath(__file__)
path_app_run = os.path.dirname(os.path.dirname(path_script))
sys.path.append(path_app_run)

## use common functions to initalize global variable and set logger ##
import utilities.common_functions as cf
import queries.queries as queries

cf.init(path_app_run)
cf.get_config()
cf.get_current_datetime()

loggername = 'bstream'
logfile_name = f'{loggername}_{cf.gvar.current_date_pst}.log'
logger = cf.set_logger(loggername, logfile_name)

## dump BinLog from mysql ##
mysql_settings = {
 "host": cf.gvar.mysql_hostname,
 "port": int(cf.gvar.mysql_port),
 "user": cf.gvar.mysql_username,
 "passwd": cf.gvar.mysql_password
}

b_stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    server_id=100,
    only_events =[row_event.DeleteRowsEvent,
        row_event.WriteRowsEvent,
        row_event.UpdateRowsEvent]
 )

for event in b_stream:
    event.dump()

b_stream.close()


# ## Connect to target and extract max last updated
# max_update_query = queries.get_max_update_orders
# target_connection = cf.connect_snowflake()
# target_cursor = target_connection.cursor()
# target_cursor.execute(max_update_query)
# logger.info('Executed query: {}'.format(target_cursor.query))
# result = target_cursor.fetchone()
# last_updated_target = result[0]
# logger.info(f'last updated from target selected as: {last_updated_target}')

# target_cursor.close()
# target_connection.close()

# ## Connect to source and extract data
# extract_orders_query = queries.extract_orders_query
# source_connection = cf.connect_mysql()
# source_cursor = source_connection.cursor()
# source_cursor.execute(extract_orders_query, {'max_update_orders' : last_updated_target})
# logger.info('Executed query: {}'.format(source_cursor._executed))
# results = source_cursor.fetchall()

# extract_file_name = f'order_extract_{cf.gvar.current_date_pst}.csv'
# extract_file_path = os.path.join(cf.gvar.path_data, extract_file_name)

# with open(extract_file_path, 'w') as extract_file:
#     csv_w = csv.writer(extract_file, delimiter='|')
#     csv_w.writerows(results)
# logger.info(f'extracted data from source and written to {extract_file_path}')

# extract_file.close()
# source_cursor.close()
# source_connection.close()

# ## Upload file to AWS S3 bucket
# bucket_name = cf.gvar.aws_s3_bucket_name
# cf.s3_upload_file(extract_file_path, bucket_name, extract_file_name)
