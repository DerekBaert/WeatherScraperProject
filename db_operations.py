"""Handles all database queries for the weather database."""

import sqlite3
from datetime import datetime
from dbcm import DBCM

class DBOperations():
    """Class for creating, updating, deleting from the database."""

    def initialize_db(self):
        """Initialize the database."""
        try:
            with DBCM("weather.sqlite") as curs:
                curs.execute("""create table if not exists sample_data
                        (id integer primary key autoincrement not null,
                        sample_date text not null,
                        location text not null,                   
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);""")
        except Exception as error:
            print("Error: initailize_db: Create database if doesn't exist: ", error)
    def save_data(self, sample_data):
        """Adds unique weather data to the database."""
        try:
            sql = """insert into sample_data (sample_date, location, min_temp, max_temp, avg_temp)
                    values (?, ?, ?, ?, ?)"""
            location = "Winnipeg, MB"
            date_check_sql = "select max(sample_date) from sample_data"
        except Exception as error:
            print("Error: save_data: Initalize sql statements: ", error)
        try:
            with DBCM("weather.sqlite") as curs:
                for row in curs.execute(date_check_sql):
                    try:
                        last_date = datetime.strptime(str(row).strip("(),'"), "%Y-%m-%d")
                    except:
                        last_date = "None"
        except Exception as error:
            print("Error: save_data: Accessing max date: ", error)
        try:
            for date, temps in sample_data.items():
                try:
                    if last_date == "None" or last_date < datetime.strptime(str(date).strip("'"), "%Y-%m-%d"):
                        data = []
                        try:
                            data.append(date)
                            data.append(location)  
                            try:                      
                                for key in temps:
                                    data.append(temps[key])
                            except Exception as error:
                                print("Error: save_data: Looping through keys: ", error)
                        except Exception as error:
                            print("Error: save_data: Adding to database: ", error)
                        try:
                            with DBCM("weather.sqlite") as curs:
                                curs.execute(sql, data)
                        except Exception as error:
                            print("Error: save_data: Executing sql to database: ", error)
                except Exception as error:
                    print("Error: save_data: Comparing for existing data: ", error)
        except Exception as error:
            print("Error: save_data: Looping through data: ", error)
    def purge_data(self):
        """Deletes all data in the database."""
        try:
            with DBCM("weather.sqlite") as curs:
                sql = """delete from sample_data"""
                try:
                    curs.execute(sql)
                except Exception as error:
                    print("Error: purge_data: Executing sql: ", error)
        except Exception as error:
            print("Error: purge_data: Accessing database: ", error)
    def fetch_data(self):
        """Prints each row of the database."""
        try:
            with DBCM("weather.sqlite") as curs:
                sql = """select * from sample_data"""
                try:
                    for row in curs.execute(sql):
                        print(row)
                except Exception as error:
                    print("Error: fetch_data: Looping through database: ", error)
        except Exception as error:
            print("Error: fetch_data: Accessing database: ", error)
