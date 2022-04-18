"""Handles all database queries for the weather database."""

from re import I
import sqlite3
from datetime import datetime
from dbcm import DBCM
import logging

class DBOperations():
    """Class for creating, updating, deleting from the database."""

    def initialize_db(self):
        """Initialize the database."""
        try:
            with DBCM("weather.sqlite") as curs:
                curs.execute("""create table if not exists sample_data
                        (id integer primary key autoincrement not null,
                        sample_date text not null,
                        location text,                   
                        min_temp real,
                        max_temp real,
                        avg_temp real);""")
        except Exception as error:
            logging.warning("Error: initailize_db: Create database if doesn't exist: ", error)

    def save_data(self, sample_data):
        """Adds unique weather data to the database."""
        try:
            sql = """insert into sample_data (sample_date, location, min_temp, max_temp, avg_temp)
                    values (?, ?, ?, ?, ?)"""
            location = "Winnipeg, MB"
            date_check_sql = "select max(sample_date) from sample_data"
        except Exception as error:
            logging.warning("Error: save_data: Initalize sql statements: ", error)
        try:
            with DBCM("weather.sqlite") as curs:
                for row in curs.execute(date_check_sql):
                    try:
                        last_date = datetime.strptime(str(row).strip("(),'"), "%Y-%m-%d")
                    except:
                        last_date = "None"
        except Exception as error:
            logging.warning("Error: save_data: Accessing max date: ", error)
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
                                logging.warning("Error: save_data: Looping through keys: ", error)
                        except Exception as error:
                            logging.warning("Error: save_data: Adding to database: ", error)
                        try:
                            with DBCM("weather.sqlite") as curs:
                                curs.execute(sql, data)
                        except Exception as error:
                            logging.warning("Error: save_data: Executing sql to database: ", error)
                except Exception as error:
                    logging.warning("Error: save_data: Comparing for existing data: ", error)
        except Exception as error:
            logging.warning("Error: save_data: Looping through data: ", error)

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
            logging.warning("Error: purge_data: Accessing database: ", error)

    def fetch_box_data(self, values):
        """Collects all the data required for the box plot."""
        try:
            box_plot_dictionary = {}
            month_data = []
            values.append("")
        except Exception as error:
            logging.warning("Error: fetch_box_data: Initializing variables: ", error)
        try:
            with DBCM("weather.sqlite") as curs:
                for i in range(1, 13):
                    if i >= 10:
                        values[2] = ("%-" + str(i) + "-%")
                    else:
                        values[2] = ("%-0" + str(i) + "-%")
                    sql = """select sample_date, avg_temp from sample_data where sample_date between ? and ? and sample_date like ?"""
                    for row in curs.execute(sql, values):
                        if (row[1] is not None):
                            month_data.append(row[1])
                    box_plot_dictionary[i] = month_data
                    month_data = []
        except Exception as error:
            logging.warning("Error: fetch_box_data: Collecting data from database: ", error)
        return box_plot_dictionary

    def fetch_line_data(self, date):
        """Collects all the data required for the line plot."""
        try:
            modified_date = []
            line_plot_dictionary = {}
            modified_date.append("%" + date.strftime("%Y") + "-" + date.strftime("%m") + "%")
        except Exception as error:
            logging.warning("Error: fetch_line_data: Initializing variables: ", error)
        try:
            with DBCM("weather.sqlite") as curs:
                sql = """select sample_date, avg_temp from sample_data where sample_date like ?"""
                for row in curs.execute(sql, modified_date):
                    line_plot_dictionary[row[0]] = row[1]
        except Exception as error:
            logging.warning("Error: fetch_line_data: Collecting data from database: ", error)
        return line_plot_dictionary

    def last_day(self):
        """Fetches the last date from the data in the database."""
        try:
            last_date = ""
        except Exception as error:
            logging.warning("Error: last_day: Initialize variables: ", error)
        
        try:
            with DBCM("weather.sqlite") as curs:                
                sql = """select MAX(sample_date) from sample_data"""
                for row in curs.execute(sql):
                    last_date = datetime.strptime(str(row).strip("(),'"), "%Y-%m-%d")
        except Exception as error:
            logging.warning("Error: last_day: Retrieving the earliest date from database: ", error)
        return last_date
