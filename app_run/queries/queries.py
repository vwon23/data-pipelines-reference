##### SQL queries to be executed by python scrip ######

extract_query = """
    SELECT * FROM Orders;
"""

get_max_update_orders = """SELECT COALESCE(MAX(LastUpdated),
    '1900-01-01') FROM Raw.mysql.Orders;
"""
