"""Module level docstring"""

import sqlite3
from dbcm import DBCM

class DBOperations():
    """Class level docstring"""

    def initialize_db(self):
        """Function level docstring"""
        with DBCM("weather.sqlite") as curs:
            curs.execute("""create table if not exists sample_data
                    (id integer primary key autoincrement not null,
                    sample_date text not null,
                    location text not null,                   
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);""")
    def save_data(self, sample_data):
        sql = """insert into sample_data (sample_date, location, min_temp, max_temp, avg_temp)
                values (?, ?, ?, ?, ?)"""
        location = "Winnipeg, MB"
        for date, temps in sample_data.items():
            data = []
            data.append(date)
            data.append(location)
            for key in temps:
                data.append(temps[key])
            with DBCM("weather.sqlite") as curs:
                curs.execute(sql, data)
    def purge_data(self):
        with DBCM("weather.sqlite") as curs:
            sql = """delete from sample_data"""
            curs.execute(sql)
    def fetch_data(self):
        with DBCM("weather.sqlite") as curs:
            sql = """select * from sample_data"""
            for row in curs.execute(sql):
                print(row)
