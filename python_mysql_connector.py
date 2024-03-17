import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

from db_credentials import db_connnection_string


def update_booking_table(date, name):
    engine = create_engine(db_connnection_string)

    with engine.connect() as con:
        sql = text(f"REPLACE into booking_table (date, name) values (:date, :name)")
        params = {'name': name, 'date': date}

        con.execute(sql, parameters=params)

        con.commit()


if __name__ == '__main__':
    """
    engine = create_engine(db_connnection_string)

    with engine.connect() as con:
        sql = text("show tables")
        res = con.execute(sql).fetchall()

    print(res)
    """

    date = datetime(2023, 3, 18).date()
    name = 'Tuan'

    update_booking_table(date, name)