from flask import Flask, jsonify,request
from config import Config
from db import init_db_pool
from queries import execute_query

import pandas as pd
import pickle

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
    return jsonify(results), 200
    
@app.route('/death-eth', methods=['GET']) # path of the request
def death_eth(): #ethnicity with most deaths
    query = """
    SELECT race_ethnicity, SUM(deaths) AS Total_Deaths
    FROM nyc_mortality
    GROUP BY race_ethnicity
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
    SELECT leading_cause, SUM(COALESCE(Deaths, 0)) AS Total_Deaths
    FROM nyc_mortality
    GROUP BY leading_cause
    ORDER BY Total_Deaths DESC
    LIMIT 1;  
        """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200

@app.route('/avg-death', methods=['GET']) # path of the request
def avg_death(): #average death rate for each year
    query = """
    SELECT Year, AVG(death_rate) AS Average_Death_Rate
    FROM nyc_mortality
    GROUP BY Year
    ORDER BY Year; 
    """
    results, error = execute_query(query)
    
    if error:
        return {"error": str(error)}, 500

    return jsonify(results), 200


@app.route('/predict', methods=['POST'])
def predict():
    # Load the saved LabelEncoder, one-hot encoded column names, and scaler
    with open('label_encoder_sex.pkl', 'rb') as f:
        label_encoder = pickle.load(f)

    with open('race_columns.pkl', 'rb') as f:
        race_columns = pickle.load(f)

    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Load the trained model
    with open('random_search_model.pkl', 'rb') as f:
        model = pickle.load(f)


    # Convert new data to DataFrame
    data = request.get_json()
    try:
        new_data_df = pd.DataFrame(data)

        # 1. Handle categorical data (Label Encoding for 'Sex')
        try:
            new_data_df['Sex'] = label_encoder.transform(new_data_df['Sex'])
        except ValueError as e:
            print(f"Error in encoding 'Sex' value: {e}")
            # If an unknown value, we can either set it to a default or skip the input.
            raise ValueError("Unknown 'Sex' value encountered. Please provide a valid label.")
        
        valid_race_categories = ['White Non-Hispanic', 'Black Non-Hispanic', 'Hispanic', 'Asian Non-Hispanic', 'Other']
        input_race = new_data_df['Race Ethnicity'].iloc[0]
        
        if input_race not in valid_race_categories:
            return jsonify({"error": f"Invalid 'Race Ethnicity' value: {input_race}. Please provide one of the following: {', '.join(valid_race_categories)}"}), 400
        # 2. Handle 'Race Ethnicity' with one-hot encoding (matching columns)
        new_data_df = pd.get_dummies(new_data_df, columns=['Race Ethnicity'], drop_first=True)

        # 3. Add missing columns with zero values
        for col in race_columns:
            if col not in new_data_df.columns:
                new_data_df[col] = 0

        # 4. Reorder the new data to match the original feature columns
        new_data_df = new_data_df[race_columns]

        # 5. Scale numerical features using the same scaler as during training
        new_data_df[['Death Rate', 'Age Adjusted Death Rate']] = scaler.transform(new_data_df[['Death Rate', 'Age Adjusted Death Rate']])
        prediction = model.predict(new_data_df)

        return jsonify({"predicted_leading_cause": prediction[0]})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host=Config.get('HOST'), port=Config.get('PORT'), debug=True) #the base path is "localhost:5000"



