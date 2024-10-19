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
 ##! Write your queries and then just copy and paste the rest
@app.route('/db_version', methods=['GET']) # path of the request
def db_version():
    query = "SELECT version();"
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200



if __name__ == '__main__':
    app.run(host=Config.get('HOST'), port=Config.get('PORT'), debug=True) #the base path is "localhost:5000"
