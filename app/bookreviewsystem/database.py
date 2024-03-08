from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the directory of the current Python file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the database file
database_filename = "app.db"
database_path = os.path.join(current_dir, "..", database_filename)

## Sqllite local database
SQLALCHEMY_DATABASE_URI = f"sqlite:///{database_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread' : False})


session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()