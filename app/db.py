import databases

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime

DATABASE_URL = "postgresql://postgres:password@localhost/postgres"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

def create_table(db_url, metadata):
    engine = create_engine(db_url)
    metadata.create_all(engine)


employees = Table(
    'employees',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String(30), nullable=False),
    Column('lastname', String(30), nullable=False),
    Column('date_of_birth', DateTime, nullable=False),
    Column('position', String(30), nullable=False)
)


if __name__ == '__main__':
    create_table(DATABASE_URL, metadata)
