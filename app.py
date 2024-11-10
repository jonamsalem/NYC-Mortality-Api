from flask import Flask, jsonify
from config import Config
from db import init_db_pool
from queries import execute_query

app = Flask(__name__)

#Initialize the connection pool with postgresql database instance in GCP
init_db_pool(
    Config.get('DB_HOST'),
    Config.get('DB_PORT'),
    Config.get('DB_NAME'),
    Config.get('DB_USER'),
    Config.get('PASSWORD')
)


#This route will return the version of the database. Just an example to show how to use the connection pool.
 ##! Write your queries and then just copy and paste the rest with its corresponding path and function name
@app.route('/db_version', methods=['GET']) # path of the request
def db_version():
    query = "SELECT version();"
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/count', methods=['GET']) # path of the request
def count():
    query = "SELECT COUNT(*) FROM nyc_mortality;"
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/all-rows', methods=['GET']) # path of the request
def all_rows():
    query = "SELECT * FROM nyc_mortality;"
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/cause', methods=['GET']) # path of the request
def cause():
    query = """
    SELECT leading_cause, COUNT(*) 
    FROM nyc_mortality
    GROUP BY leading_cause;
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/cause-year', methods=['GET'])  # path of the request
def cause_year():
    query = """
    SELECT Year, leading_cause, COUNT(*) AS death_count
    FROM nyc_mortality
    GROUP BY Year, leading_cause;
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200


@app.route('/cause-common', methods=['GET']) # path of the request
def cause_common():
    query = """
    SELECT leading_cause, COUNT(*) AS death_count 
    FROM nyc_mortality
    GROUP BY leading_cause
    ORDER BY death_count DESC;
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200


@app.route('/death', methods=['GET']) # path of the request
def death(): #highest number of deaths in a year
    query = """
    SELECT Year, SUM(Deaths) AS Total_Deaths
    FROM nyc_mortality
    GROUP BY Year
    ORDER BY Total_Deaths DESC
    LIMIT 1;
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500
    
@app.route('/death-eth', methods=['GET']) # path of the request
def death_eth(): #ethnicity with most deaths
    query = """
    SSELECT "Race Ethnicity", SUM(Deaths) AS Total_Deaths
    FROM nyc_mortality
    GROUP BY "Race Ethnicity"
    ORDER BY Total_Deaths DESC
    LIMIT 1;   
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/high-death', methods=['GET']) # path of the request
def high_death(): #leading cause of death with most deaths
    query = """
    SELECT "Leading Cause", SUM(Deaths) AS Total_Deaths
    FROM ynyc_mortality
    GROUP BY "Leading Cause"
    ORDER BY Total_Deaths DESC
    LIMIT 1;   
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/avg-death', methods=['GET']) # path of the request
def avg_death(): #leading cause of death with most deaths
    query = """
    SELECT Year, AVG("Death Rate") AS Average_Death_Rate
    FROM nyc_mortality
    GROUP BY Year
    ORDER BY Year; 
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200
if __name__ == '__main__':
    app.run(host=Config.get('HOST'), port=Config.get('PORT'), debug=True) #the base path is "localhost:5000"

