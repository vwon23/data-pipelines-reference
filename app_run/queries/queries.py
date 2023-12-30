##### SQL queries to be executed by python scrip ######

extract_orders_query = """
    SELECT * FROM Orders
    WHERE LastUpdated > %(max_update_orders)s
"""

get_max_update_orders = """SELECT COALESCE(MAX(LastUpdated),
    '1900-01-01') FROM Raw.mysql.Orders;
"""

copy_s3_orders = """copy into Raw.mysql.Orders (id, first_name, last_name)
    from 's3://dbt-tutorial-public/jaffle_shop_customers.csv'
    file_format = (
        type = 'CSV'
        field_delimiter = ','
        skip_header = 1
        ); 
"""
