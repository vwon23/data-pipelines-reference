import sys, os
import datetime
import configparser
import logging, logging.config

import datetime as dt
import pytz
from pytz import timezone


def init(path_app_run: str):
    '''
    creates global variable class to handle the variables across scripts and functions. Sets the provided application run path as dnam in gvar

    Parameters
    ---------------
        path_app_run: str
            directory path of app_run (e.g. app/app_run) returned from os.path.dir() function
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

    gvar.path_app = os.path.dirname(gvar.dname)
    #gvar.path_app = config.get('Paths', 'HOME_DIR')

    gvar.path_log = os.path.join(gvar.path_app, 'logs')
    gvar.path_logconfig = os.path.join(gvar.dname, 'config', 'logging.cfg')
    #gvar.path_log = config.get('Paths', 'LOG_DIR')

    ## mysql variables ##
    gvar.mysql_hostname = config.get('mysql_info', 'hostname')
    gvar.mysql_port = config.get('mysql_info', 'port')
    gvar.mysql_database = config.get('mysql_info', 'database')

    ## AWS variables ##
    gvar.aws_rgn = os.environ['aws_rgn']
    gvar.aws_s3_bucket_name = config.get('aws_info', 's3_bucket_name').format(env = gvar.env, aws_rgn = gvar.aws_rgn)
    #print(f'AWS s3 bucket name: {gvar.aws_s3_bucket_name}')


def set_logger(loggername: str, filename: str):
    '''
    Sets logger based on selected loggername & Outputs to provided filename

    Parameters
    ---------------
        loggername: str
            The name of logger to set as. (The log name will be searched in logging.cfg to check config setting)
        filename: str
            the name of filename to store logfile as
    Return
    ---------------
        logger: logging.getLogger(loggername)
    '''
    
    if not os.path.exists(gvar.path_log):
        os.makedirs(gvar.path_log)

    gvar.path_logfile = os.path.join(gvar.path_log, filename)
    logging.config.fileConfig(gvar.path_logconfig, defaults={'logfilename': gvar.path_logfile})

    global logger
    logger = logging.getLogger(loggername)
    logger.info(f'logs being written to {gvar.path_logfile}')

    return logger


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