import databases

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date

DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"

database = databases.Database(DATABASE_URL)

metadata = MetaData()


engine = create_engine(DATABASE_URL)

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
    metadata.create_all(engine)
