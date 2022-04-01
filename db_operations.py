"""Module level docstring"""

import sqlite3
import dbcm

class DBOperations():
    """Class level docstring"""

    def initialize_db(self):
        """Function level docstring"""
        with dbcm.DBCM("weather.sqlite") as curs:
            curs.execute("""create table sample_data
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
            with dbcm.DBCM("weather.sqlite") as curs:
                curs.execute(sql, data)
    def purge_data(self):
        with dbcm.DBCM("weather.sqlite") as curs:
            sql = """delete from sample_data"""
            curs.execute(sql)
    def fetch_data(self):
        with dbcm.DBCM("weather.sqlite") as curs:
            sql = """select * from sample_data"""
            for row in curs.execute(sql):
                print(row)

weather_dictionary = {"2018-06-01": {"Max": 12.0, "Min": 5.6, "Mean": 7.1},
                        "2018-06-02": {"Max": 22.2, "Min": 11.1, "Mean": 15.5},
                        "2018-06-03": {"Max": 31.3, "Min": 29.9, "Mean": 30.0},
                        "2018-06-04": {"Max": 1.3, "Min": 2.9, "Mean": 3.0}}

db = DBOperations()
db.initialize_db()
db.save_data(weather_dictionary)
db.fetch_data()
db.purge_data()
db.fetch_data()