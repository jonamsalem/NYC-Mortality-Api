import os
from dotenv import load_dotenv

load_dotenv()

#parse the .env file and return it using the get method
class Config:
    config = {
        "DB_HOST": os.getenv('DB_HOST'),
        "DB_PORT": 5432,
        "DB_NAME": os.getenv('DB_NAME'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "DB_USER": os.getenv('DB_USER'),
        "PORT": os.getenv('PORT'),
        "HOST": os.getenv('HOST')
    }

    @classmethod #allows us to avoid creating an instance of the class to use the get method
    def get(cls, name):
        return cls.config.get(name)

