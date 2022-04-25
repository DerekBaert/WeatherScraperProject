"""
Scrapes data from Climate website based on today's date.
"""
import logging
from html.parser import HTMLParser
from datetime import datetime

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
            logging.warning("Error: Init: Initialize variables: %s", error)
    def handle_starttag(self, tag, attrs):
        """
        Checking if the tag attribute to determine if the parser is in the row.
        """
        try:
            if not self.stop:
                if tag == "tbody":
                    self.in_body = True
                if self.in_body:
                    if tag == "tr":
                        self.in_row = True
                    if tag == "td":
                        self.in_data = True
                    if tag == "th":
                        self.row_head = True
                    if tag == "abbr" and self.row_head:
                        self.in_row_date = True
                        try:
                            self.entry_date = datetime.strptime(attrs[0][1],'%B %d, %Y')
                        except Exception as error:
                            logging.warning("Error: handle_starttag: Parsing date %s", error)
        except Exception as error:
            logging.warning("Error: handle_starttag: Checking start tag: %s", error)
    def handle_endtag(self, tag):
        """
        Checks end tags, and sets body flag to false when body end tag is found.
        """
        try:
            if self.in_body:
                if tag == "tr":
                    self.in_row = False
                    self.count = 0
                if tag == "td":
                    self.in_data = False
        except Exception as error:
            logging.warning("Error: handle_endtag: Checking end tag: %s", error)
    def handle_data(self, data):
        """
        Adds the name of the colour and the hex code
        to the dictionary and sets the colour flag back to false.
        """
        try:
            if not self.stop :
                if self.in_body:
                    if data == 'Sum':
                        self.stop = True
                    if self.entry_date:
                        if self.entry_date.strftime('%Y-%m-%d') not in self.weather:
                            if self.in_data and self.count < 3:
                                data = data.strip()
                                if data in ('M', ''):
                                    try:
                                        self.add_to_dictionary(None)
                                        self.count = self.count + 1
                                        logging.warning("handle_data: Found empty/missing data: %s", data)
                                    except Exception as error:
                                        message = "handle_data: Handling missing data: %s", error
                                        logging.warning(message)
                                elif data in ('LegendM', 'LegendE', 'E'):
                                    logging.warning("handle_data: Found exception in data: %s", data)
                                    pass
                                else:
                                    try:
                                        self.add_to_dictionary(data)
                                        self.count = self.count + 1
                                    except Exception as error:
                                        message = "handle_data: Handling existing data: %s", error
                                        logging.warning(message)
                            elif self.count == 3 and self.daily_temps:
                                try:
                                    date = self.entry_date.strftime('%Y-%m-%d')
                                    self.weather[date] = self.daily_temps
                                    self.daily_temps = {}
                                except Exception as error:
                                    message = "handle_data: Adding data to dictionary: %s",error
                                    logging.warning(message)
        except Exception as error:
            logging.warning("Error checking or printing data %s", error)
    def add_to_dictionary(self, data):
        """Add data to weather dictionary based on count."""
        try:
            match self.count:
                case 0:
                    try:
                        self.daily_temps['Max'] = data
                    except Exception as error:
                        logging.warning("Error: add_to_dictionary: Adding max: %s", error)
                case 1:
                    try:
                        self.daily_temps['Min'] = data
                    except Exception as error:
                        logging.warning("Error: add_to_dictionary: Adding min: %s", error)
                case 2:
                    try:
                        self.daily_temps['Mean'] = data
                    except Exception as error:
                        logging.warning("Error: add_to_dictionary: Adding mean: %s", error)
        except Exception as error:
            logging.warning("Error: add_to_dictionary: Matching count: %s", error)
    def compare_url(self, url_month, url_year):
        """Compare the url month to the month in the
        attribute tag to determine when to stop scraping."""
        match = False
        try:
            if self.entry_date:
                try:
                    if url_month == self.entry_date.month and url_year == self.entry_date.year:
                        match = True
                except Exception as error:
                    logging.warning("Error: compare_url: Checking if months are the same: %s", error)
        except Exception as error:
            logging.warning("Error: compare_url: Checking if entry_date exists: %s", error)
        return match
