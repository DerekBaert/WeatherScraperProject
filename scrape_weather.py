"""
Scrapes data from https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year=2018&Month=3
"""
from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
from datetime import datetime

class WeatherScraper(HTMLParser):
    """
    Setting class variable to check if parser is in body of HTML
    """
    def __init__(self):
        """
        Setting class variable to check if parser is in body of HTML
        """
        HTMLParser.__init__(self)
        self.in_row = False
        self.in_data = False
        self.row_head = False
        self.in_row_date = False
        self.entry_data = 0
        self.daily_temps = {}
        self.count = 0
                

    def handle_starttag(self, tag, attrs):
        """
        Checking if the tag attribute to determine if the parser is in the row.
        """
        try:
            if(tag == "tr"):
                self.in_row = True
            if(self.in_row == True):
                if(tag == "td"):
                    self.in_data = True 
                if(tag == "th"):    
                    self.row_head = True  
                if(tag == "abbr" and self.row_head):
                    self.in_row_date = True 
                    try:
                        date = datetime.strptime(attrs[0][1],'%B %d, %Y').strftime('%Y-%m-%d')
                        print(date) 
                    except Exception:
                        pass
        except Exception as error:
            print("Error checking start tag", error)
            
    def handle_endtag(self, tag):
        """
        Checks end tags, and sets body flag to false when body end tag is found.
        """
        try:
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
        valid = True 
        try:
            if(self.in_data and self.count < 3):
                try:
                    self.parsed_data = float(data)
                except Exception:
                    valid = False
                if(valid):    
                    print(self.parsed_data)
                    self.count = self.count + 1            
        except Exception as error:
            print("Error checking or printing data", error)
        

myscraper = WeatherScraper()
try:
    with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year=2018&Month=3') as response:
        html = str(response.read())
    myscraper.feed(html)
    input("")
except Exception as error:
    print("Error parsing HTML", error)