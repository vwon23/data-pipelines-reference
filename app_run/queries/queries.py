##### SQL queries to be executed by python scrip ######

select_orders_full_query = """
    SELECT * FROM Orders;
"""

select_orders_incremental_query = """
    SELECT * FROM Orders
    WHERE LastUpdated > %(max_update_orders)s;
"""

get_max_update_orders = """SELECT COALESCE(MAX(LastUpdated),
    '1900-01-01') FROM my_app.Orders;
"""

copy_s3_orders = """COPY INTO data_lake.my_app.Orders (id, first_name, last_name)
    from 's3://dbt-tutorial-public/jaffle_shop_customers.csv'
    file_format = (
        type = 'CSV'
        field_delimiter = ','
        skip_header = 1
        ); 
"""
