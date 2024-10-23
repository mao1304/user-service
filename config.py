from dotenv import load_dotenv
import os 


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SERVER_NAME = 'localhost:5000'
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'database', 'data.sqlite3')


    