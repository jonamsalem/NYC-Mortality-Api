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


## Contributors
   Ruby Ssk
   
   Ezeddin Fadel
   
   Jonathan Amsalem
