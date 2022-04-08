"""
Scrapes data from Climate website based on today's date.
"""
from html.parser import HTMLParser
from html.entities import name2codepoint
from importlib.metadata import entry_points
import urllib.request
from datetime import datetime
import pprint
import dbcm
from db_operations import DBOperations

class WeatherScraper(HTMLParser):
    """
    Class scrapes the weather data only from the passed url.
    """
    def __init__(self):
        """
        Setting class variable to check if parser is in body of HTML
        """
        try:
            HTMLParser.__init__(self)
            self.in_row = False
            self.in_data = False
            self.row_head = False
            self.in_row_date = False
            self.stop = False
            self.in_body = False
            self.entry_date = ""
            self.daily_temps = {}
            self.weather = {}
            self.count = 0
        except Exception as error:
            print("Error: Init: Initialize variables: ", error)
    def handle_starttag(self, tag, attrs):
        """
        Checking if the tag attribute to determine if the parser is in the row.
        """
        try:
            if(not self.stop):
                if(tag == "tbody"):
                    self.in_body = True
                if(self.in_body):
                    if(tag == "tr"):
                        self.in_row = True
                    if(tag == "td"):
                        self.in_data = True
                    if(tag == "th"):    
                        self.row_head = True
                    if(tag == "abbr" and self.row_head):
                        self.in_row_date = True                                        
                        try:                                
                            self.entry_date = datetime.strptime(attrs[0][1],'%B %d, %Y')
                        except Exception as e:
                            print("Error parsing date", e)                      
        except Exception as error:
            print("Error checking start tag", error)
            
    def handle_endtag(self, tag):
        """
        Checks end tags, and sets body flag to false when body end tag is found.
        """
        try:
            if(self.in_body):
                if(tag == "tr"):
                    self.in_row = False
                    self.count = 0
                if(tag == "td"):
                    self.in_data = False
        except Exception as error:
            print("Error checking end tag", error)
                
    def handle_data(self, data):
        """
        Adds the name of the colour and the hex code to the dictionary and sets the colour flag back to false.
        """
        try:  
            if(not self.stop):
                    if(self.in_body):
                        if(data == 'Sum'):
                            self.stop = True
                        if (self.entry_date):
                            if self.entry_date.strftime('%Y-%m-%d') not in self.weather:
                                if(self.in_data and self.count < 3):
                                    data = data.strip()
                                    if(data == "M" or data == ""):
                                        try:
                                            self.add_to_dictionary("M")
                                            self.missing = False
                                            self.count = self.count + 1
                                        except Exception as error:
                                            print("Error: handle_data: Handling missing data: ", error)
                                    elif(data == "LegendM" or data == "LegendE" or data == "E"):
                                        pass
                                    else:
                                        try:
                                            self.add_to_dictionary(data)
                                            self.count = self.count + 1
                                        except Exception as error:
                                            print("Error: handle_data: Handling existing data: ", error)
                                elif(self.count == 3 and self.daily_temps):
                                    try:
                                        self.weather[self.entry_date.strftime('%Y-%m-%d')] = self.daily_temps
                                        self.daily_temps = {}
                                    except Exception as error:
                                        print("Error: handle_data: Adding data to weather dictionary: ", error)
        except Exception as error:
            print("Error checking or printing data", error)
    def add_to_dictionary(self, data):
        """Add data to weather dictionary based on count."""
        try:
            match self.count:
                case 0:
                    try:
                        self.daily_temps['Max'] = data
                    except Exception as error:
                        print("Error: add_to_dictionary: Adding max: ", error)
                case 1:
                    try:
                        self.daily_temps['Min'] = data
                    except Exception as error:
                        print("Error: add_to_dictionary: Adding min: ", error)
                case 2:
                    try:
                        self.daily_temps['Mean'] = data
                    except Exception as error:
                        print("Error: add_to_dictionary: Adding mean: ", error)
        except Exception as error:
            print("Error: add_to_dictionary: Matching count: ", error)
    def compare_url(self, url_month):
        """Compare the url month to the month in the attribute tag to determine when to stop scraping."""
        try:
            if self.entry_date:
                try:
                    if url_month != self.entry_date.month:
                        return False
                    else:
                        return True
                except Exception as error:
                    print("Error: compare_url: Checking if months are the same: ", error)
        except Exception as error:
            print("Error: compare_url: Checking if entry_date exists: ", error)

try:
    today = datetime.today()
    year = today.year
    month = today.month
    end_check = True
    weather = {}
except Exception as error:
    print("Error: main: Initializing variables: ", error)

try:
    while end_check:
        print(f"Year: {year} Month: {month}")
        myscraper = WeatherScraper()
        try:
            with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                html = str(response.read())
            myscraper.feed(html)
            weather = weather | myscraper.weather
            if myscraper.weather:
                end_check = myscraper.compare_url(month)
            if (month == 1):
                year = year - 1
                month = 12
            else:
                month = month - 1
                    
        except Exception as error:
            print("Error parsing HTML", error)
except Exception as error:
    print("Error: main: Checking while loop: ", error)

try:
    db = DBOperations()
    db.initialize_db()
    db.save_data(weather)
    db.fetch_data()
except Exception as error:
    print("Error: main: Database calls: ", error)
