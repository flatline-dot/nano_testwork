import databases

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date

DATABASE_URL = "postgresql://postgres:123@localhost:5432/postgres"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

def create_table(db_url, metadata):
    engine = create_engine(db_url)
    metadata.create_all(engine)


employees = Table(
    'employees',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String(30)),
    Column('lastname', String(30)),
    Column('date_of_birth', Date),
    Column('email', String(30),unique=True),
    Column('position', String(30))
)


if __name__ == '__main__':
    create_table(DATABASE_URL, metadata)
