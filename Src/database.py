import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv('.env')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('DATABASE_NAME')

db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(db_url)
    
local_session = sessionmaker(bind = engine, autoflush = False, autocommit = False)