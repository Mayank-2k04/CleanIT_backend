from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# make the database connection ---comments by MAYANK
sql_filename = "./testdb.db"
SQL_DATABASE_URL = f'sqlite:///{sql_filename}'
connect_args = {"check_same_thread":False}
engine = create_engine(SQL_DATABASE_URL,connect_args=connect_args)

local_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

base = declarative_base()