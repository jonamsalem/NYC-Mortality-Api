# NYC Mortality API

## Overview

The NYC Mortality API is a web service designed to analyze and provide insights into mortality rates in New York City. This project leverages PostgreSQL as the database to store mortality data, Python (with Flask) as the backend framework, and React for the frontend user interface (TODO).

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#Setup)
- [Contributing](#contributing)

## Features

- Retrieve the version of the PostgreSQL database.
- Analyze mortality data based on various parameters (e.g., demographics, causes of death).
- Flexible and reusable query execution with connection pooling for efficient database access.

## Technologies

- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Frontend**: React
- **Database Driver**: psycopg2 for PostgreSQL interaction

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/NYC-Mortality-Api.git
   cd NYC-Mortality-Api
   ```

   Install dependencies:
   ```bash
    pip install -r requirements.txt
    ```

   Create a `.env` file in the root directory and populate with secrets. DO NOT store secrets in `example.env`.

2.  DO NOT write code in main

  code in a different branch that is not main
   example ```git checkout -b"update-readme"```  on terminal

3. Always pull main before creating new code
example ``` git pull origin main ``` on terminal

4. Unzip the random_search_model.pkl.zip file


5. Run server

   ```bash 
   python3 app.py
   ```

6. Before writing code:
     ```bash 
   git pull origin main
   ```

 
7. When done writing code:
      ```bash 
   git add . 
   ```
      ```bash 
   git commit -m "message"
   ```

      ```bash 
   git push origin main
   ```


## To run the prediction endpoint follow this format: 

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "Sex": ["Male"],
  "Race Ethnicity": ["Hispanic"],
  "Death Rate": [15.4],
  "Age Adjusted Death Rate": [22.8]
}'
{
  "predicted_leading_cause": "Meningitis (G00, G03)"
}



```
## Contributors
   Ruby Ssk
   
   Ezeddin Fadel
   
   Jonathan Amsalem


3. Unzip the random_search_model.pkl.zip file
