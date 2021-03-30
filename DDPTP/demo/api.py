import re
from DP_library import laplace
from django.db import connection

def make_query(query):
    if check_query(query, "experiments_statlog") == True:
        if "where" in query.lower():
            try:
                condition = re.split("where", query, flags=re.IGNORECASE)[1]
                count_query = "select count(*) from experiments_statlog where" + condition
                if get_query_result(count_query)<10:
                    result = "Unable to return a result because the number of entries that satisfy the 'WHERE' condition is less than 10."
                    return result
            except:
                result = "Invalid query! Please enter a MySQL query that returns a number with correct syntax."
                return result
        try:
            result = get_query_result(query)
            result = float(result)
        except:
            result = "Invalid query! Please enter a MySQL query that returns a number with correct syntax."
            return result
    else:
        result = "Invalid query! Please refer to the rules of making queries."
        return result
    
    # query is valid, process the result with differential privacy
    epsilon = 1
    if "count" in query.lower():
        epsilon = 0.5
    result = laplace(result, epsilon=epsilon)
    return result

def check_query(query, table_name):
    lowered_query = query.lower()
    if any(keyword in lowered_query for keyword in ("limit", "join", "insert", "update", "delete", " on ", "result")):
        return False
    if "select" and table_name in lowered_query:
        if any(keyword in lowered_query for keyword in ("count", "sum", "avg", "stddev", "variance")):
            return True
    return False

def get_query_result(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result)>1 or len(result[0])>1:
            raise Exception
    return float(result[0][0])

# A demo of making queries through python code
def query_demo():
    query = "SELECT AVG(age) FROM experiments_statlog"
    import urllib.parse
    encoded_query = urllib.parse.quote_plus(query)
    url = "thediscriminationfreemodel.uk/demo/api/result?query="+encoded_query
    # TODO: Test after deployment 