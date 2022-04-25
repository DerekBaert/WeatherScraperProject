"""UI for the weather processor project"""
from datetime import datetime
import time
import logging
import urllib.request
import db_operations
import scrape_weather
import plot_operations
from frmMain import fraMain

class UI(fraMain):
    """Class level docstring"""
    plot = plot_operations.PlotOperations()
    db = db_operations.DBOperations()

    def __init__(self):
        """
        Initializes variables based on if database is populated or not.
        """
        try:
            super().__init__(None)
            self.db.initialize_db()
            if self.db.count() == 0:
                self.disable_controls()
            else:
                self.set_dropdowns()
                self.enable_controls()
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("__init__: Initiliazing variables: %s", error)

    def disable_controls(self):
        """
        Disables all dropdowns and buttons other than the download button.
        """
        try:
            self.drp_StartYear.Disable()
            self.drp_EndYear.Disable()
            self.drp_Year.Disable()
            self.drp_Month.Disable()
            self.btnBox.Disable()
            self.btnUpdate.Disable()
            self.btnLine.Disable()
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("disable_controls: Error disabling controls %s", error)

    def enable_controls(self):
        """
        Enables all dropdowns and buttons other than the download button.
        """
        try:
            self.drp_StartYear.Enable()
            self.drp_EndYear.Enable()
            self.drp_Year.Enable()
            self.drp_Month.Enable()
            self.btnBox.Enable()
            self.btnUpdate.Enable()
            self.btnLine.Enable()
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("enable_controls: Error enabling controls %s", error)

    def set_dropdowns(self):
        """
        Sets years in the drop down fields.
        """
        try:
            self.first = self.db.first_day()
            self.first_year = int(self.first.year)
            self.last = self.db.last_day()
            self.last_year = int(self.last.year)
            years = []
            for year in range(self.first_year, self.last_year+1):
                years.append(str(year))
            self.drp_StartYear.SetItems(years)
            self.drp_StartYear.SetSelection(0)
            self.drp_EndYear.SetItems(years)
            self.drp_EndYear.SetSelection(0)
            self.drp_Year.SetItems(years)
            self.drp_Year.SetSelection(0)
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("set_dropdowns: Error populating dropdowns %s", error)

    def btnUpdate_Click( self, event ):
        """
        Updates the database with any missing dates from the website.
        """
        try:
            today = datetime.today()
            year = today.year
            month = today.month
            last_day = self.db.last_day()
            end_check = True
            weather = {}
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: update_weather: Initiliazing variables: %s", error)
        try:
            while end_check:
                self.status_bar.SetStatusText(f"Year: {year} Month: {month}")
                try:
                    self.status_bar.SetStatusText("Scraping Weather...")
                    scraper = scrape_weather.WeatherScraper()
                    with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                        html = str(response.read())
                    scraper.feed(html)
                    weather = weather | scraper.weather
                except Exception as error:
                    self.status_bar.SetStatusText("Error, see log for details.", 1)
                    logging.warning("update_weather: Adding data to weather dictionary: %s", error)
                if month == 1:
                    year = year - 1
                    month = 12
                else:
                    month = month - 1
                if scraper.compare_url(last_day.month, last_day.year):
                    end_check = False
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: update_weather: Looping through scraper: %s", error)
        self.status_bar.SetStatusText("Scrape complete, saving to database...")
        try:
            self.db.save_data(weather)
            self.status_bar.SetStatusText("Up to date.")
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: update_weather: Saving weather to database: %s", error)
        self.status_bar.SetStatusText("Saved to database.")
        time.sleep(1)
        self.status_bar.SetStatusText("")
        self.set_dropdowns()
        self.enable_controls()
        self.Update()

    def btnDownload_Click( self, event ):
        """
        Purges database and repopulates with data from site.
        """
        try:
            self.db.purge_data()
            today = datetime.today()
            year = today.year
            month = today.month
            end_check = True
            weather = {}
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: download_weather: Initializing variables: %s", error)
        try:
            while end_check:
                self.status_bar.SetStatusText(f"Year: {year} Month: {month}")
                try:
                    scraper = scrape_weather.WeatherScraper()
                    with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}') as response:
                        html = str(response.read())
                    scraper.feed(html)
                    weather = weather | scraper.weather
                except Exception as error:
                    self.status_bar.SetStatusText("Error, see log for details.", 1)
                    message = "download_weather: Adding data to weather dictionary: %s", error
                    logging.warning(message)
                if scraper.weather:
                    end_check = scraper.compare_url(month, year)
                if month == 1:
                    year = year - 1
                    month = 12
                else:
                    month = month - 1
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: download_weather: Looping through scraper: %s", error)
        self.status_bar.SetStatusText("Scrape complete, saving to database...")
        try:
            self.db.save_data(weather)
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error: download_weather: Saving weather to database: %s", error)
        self.status_bar.SetStatusText("Saved to database.")
        time.sleep(1)
        self.status_bar.SetStatusText("")
        self.set_dropdowns()
        self.enable_controls()
        self.Update()

    def btnBox_Click( self, event ):
        """
        Handles the click event of the "Generate Box Plot" button.
        """
        try:
            self.status_bar.SetStatusText("")
            self.status_bar.SetStatusText("",1)
            start_index = self.drp_StartYear.GetCurrentSelection()
            end_index = self.drp_EndYear.GetCurrentSelection()
            start = int(self.drp_StartYear.GetString(start_index))
            end = int(self.drp_EndYear.GetString(end_index))
            if start < end:
                year_range = []
                year_range.append(start)
                year_range.append(end)
                data = self.db.fetch_box_data(year_range)
                self.plot.box_plot(data)
            else:
                self.status_bar.SetStatusText("Starting Year must be before Ending Year",1)
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error generating box plot: %s", error)

    def btnLine_Click( self, event ):
        """
        Handles the click event of the "Generate Line Plot" button.
        """
        try:
            year_index = self.drp_Year.GetCurrentSelection()
            year = int(self.drp_Year.GetString(year_index))
            month_index = self.drp_Month.CurrentSelection
            month = datetime.strptime(self.drp_Month.GetString(month_index), "%B").month
            date = datetime(year, month, 1)
            data = self.db.fetch_line_data(date)
            self.plot.line_plot(data)
        except Exception as error:
            self.status_bar.SetStatusText("Error, see log for details.", 1)
            logging.warning("Error generating line plot: %s", error)
