import sys, os
import datetime
import configparser
import logging, logging.config

import datetime as dt
import pytz
from pytz import timezone

import pymysql
import boto3
import snowflake.connector


def init(path_app_run):
    '''
    creates global variable class to handle the variables across scripts and functions. Sets the provided application run path as dnam in gvar

    Parameters
    ---------------
    path_app_run: path
        Directory path of app_run (e.g. app/app_run) returned from os.path.dir() function
    '''
    ## create a class to hold global variables ##
    class global_variables:
        variable_1 = 'value'

    global gvar
    gvar = global_variables()
    gvar.dname = path_app_run
    print(f'Application run path set as: {path_app_run}')


def get_config():
    '''
    Adds variables to global variable gvar based on values derived from environment variables and config.cfg file

    Parameters
    ---------------
    None
    '''
    config = configparser.ConfigParser()
    config.read(os.path.join(gvar.dname, 'config', 'config.cfg'))

    gvar.env = os.environ['env']

    ## path variables ##
    gvar.path_app = os.path.dirname(gvar.dname)
    #gvar.path_app = config.get('Paths', 'HOME_DIR')
    gvar.path_log = os.path.join(gvar.path_app, 'logs')
    gvar.path_logconfig = os.path.join(gvar.dname, 'config', 'logging.cfg')
    gvar.path_data = os.path.join(gvar.path_app, 'data')

    ## create directories during run time
    if not os.path.exists(gvar.path_log):
        os.makedirs(gvar.path_log)
    if not os.path.exists(gvar.path_data):
        os.makedirs(gvar.path_data)

    ## mysql variables ##
    gvar.mysql_hostname = config.get('mysql_info', 'hostname')
    gvar.mysql_port = config.get('mysql_info', 'port')
    gvar.mysql_username = os.environ['mysql_username']
    gvar.mysql_password = os.environ['mysql_password']
    gvar.mysql_database = config.get('mysql_info', 'database')

    ## AWS variables ##
    gvar.aws_rgn = os.environ['aws_rgn']
    gvar.aws_s3_bucket = config.get('aws_info', 's3_bucket').format(env = gvar.env, aws_rgn = gvar.aws_rgn)
    gvar.aws_s3_bucket_name = gvar.aws_s3_bucket.split('//')[1]

    ## Snowflake variables ##
    gvar.snowflake_account = config.get('snowflake_info', 'account')
    gvar.snowflake_username = os.environ['snowflake_username']
    gvar.snowflake_password = os.environ['snowflake_password']
    gvar.snowflake_role = config.get('snowflake_info', 'role')
    gvar.snowflake_wh = config.get('snowflake_info', 'warehouse')
    gvar.snowflake_database = config.get('snowflake_info', 'database')
    

def set_logger(loggername, filename):
    '''
    Sets logger based on selected loggername & Outputs to provided filename

    Parameters
    ---------------
    loggername: str
        The name of logger to set as. (The log name will be searched in logging.cfg to check config setting)
    filename: str
        the name to store logfile as

    Returns
    ---------------
    logger
        logger derived from logging.getLogger(loggername)
    '''
    
    # if not os.path.exists(gvar.path_log):
    #     os.makedirs(gvar.path_log)

    gvar.path_logfile = os.path.join(gvar.path_log, filename)
    logging.config.fileConfig(gvar.path_logconfig, defaults={'logfilename': gvar.path_logfile})

    gvar.logger = logging.getLogger(loggername)
    global logger
    logger = logging.getLogger(__name__)
    logger.info(f'logs being written to {gvar.path_logfile}')

    return gvar.logger


def get_current_datetime():
    '''
    Sets variables for current date/time values.

    Parameters
    ---------------
    None
    '''
    ## UTC Time variables ##
    gvar.current_utc = dt.datetime.now()
    gvar.current_datetime_utc = gvar.current_utc.strftime("%Y-%m-%d %H:%M:%S")

    ## PST Time variables
    gvar.current_pst = dt.datetime.now().astimezone(timezone('US/Pacific'))
    gvar.current_year_pst = gvar.current_pst.strftime("%Y")
    gvar.current_date_pst = gvar.current_pst.strftime("%Y-%m-%d")
    gvar.current_datetime_pst = gvar.current_pst.strftime("%Y-%m-%d %H:%M:%S")

    print(f'Current Time in PST: {gvar.current_datetime_pst}')


def connect_mysql():
    '''
    Creates connection to mysql and returns connection

    Parameters
    ---------------
    None

    Returns
    ---------------
    conn
        connection returned using function pymysql.connect
    '''

    conn = pymysql.connect(host=gvar.mysql_hostname,
                           user=gvar.mysql_username,
                           password=gvar.mysql_password,
                           db=gvar.mysql_database,
                           port=int(gvar.mysql_port))
    if conn is None:
        logger.error(f'Error connecting to the MySQL database {gvar.mysql_hostname}')
    else:
        logger.info(f'MySQL connection established to {gvar.mysql_hostname}')
    return conn


def connect_snowflake():
    '''
    Creates connection to snowflake and returns connection

    Parameters
    ---------------
    None

    Returns
    ---------------
    conn
        connection returned using function snowflake.connector.connect
    '''

    conn = snowflake.connector.connect(account=gvar.snowflake_account,
                           user=gvar.snowflake_username,
                           password=gvar.snowflake_password,
                           warehouse=gvar.snowflake_wh,
                           role=gvar.snowflake_role,
                           database=gvar.snowflake_database)
    if conn is None:
        logger.error(f'Error connecting to the Snowflake database {gvar.mysql_hostname}')
    else:
        logger.info(f'Snowflake connection established to {gvar.mysql_hostname}')
    return conn


def s3_upload_file(file_path, bucket_name, key):
    '''
    uploads file to aws s3 bucket

    Parameters
    ---------------
    file_path: str
        The path of file to upload
    bucket_name: str
        The name of aws s3 bucket
    key: str
        The key value to upload file as
    '''

    s3c = boto3.client('s3')
    try:
        s3c.upload_file(file_path, bucket_name, key)
    except:
        logger.error(f'Error occured while uploading {file_path} to aws s3 bucket {bucket_name}')
    else:
        logger.info(f'Successfully uploaded {file_path} to aws s3 bucket {bucket_name} as {key}')
    

def s3_clean_bucket(bucket_name, prefix, n=365):
    '''
    Deletes objects older than n days inside s3 bucket. Filters objects based on prefix

    Parameters
    ---------------
    bucket_name: str
        The name of aws s3 bucket
    prefix: str
        String prefix to filter objects
    n: int
        The number of days older than current date to remove objects
    '''

    s3r = boto3.resource('s3')
    s3_bucket = s3r.Bucket(bucket_name)

    logger.info(f'Removing objects older than {n} days inside s3 bucket {bucket_name} with prefix {prefix}')
    for obj in s3_bucket.objects.filter(Prefix=prefix):
        if obj.last_modified < gvar.current_pst - dt.timedelta(days=n):
            logger.info(f'{obj.key} is older than {n} days and is deleted')
            obj.delete()