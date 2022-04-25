"""
Handles the creation of the box and line plots.
"""
import logging
import matplotlib.pyplot as plt

class PlotOperations():
    """Class for receiving weather data"""

    def initialize(self):
        """Initialize the class instance"""

    def box_plot(self, weather_data):
        """
        Takes in a dictionary of lists containing average
        temps for each month over a range of years and plots them on a box plot.
        """
        try:
            data = []
        except Exception as error:
            logging.warning("Error: box_plot: Initiliazing variables: %s", error)

        try:
            for month in weather_data:
                data.append(weather_data[month])
        except Exception as error:
            logging.warning("Error: box_plot: Organizing data for plot: %s", error)

        if not data:
            logging.warning("box_plot: Empty data set")

        try:
            plt.boxplot(data)
            plt.ylabel('Average Temperature')
            plt.xlabel('Month')
            plt.show()
        except Exception as error:
            logging.warning("Error: box_plot: Creating plot: %s", error)

    def line_plot(self, weather_data):
        """
        Takes in a dictionary of daily average
        temperatures for a month and plots them on a line plot.
        """
        try:
            data = []
            dates = []
        except Exception as error:
            logging.warning("Error: line_plot: Initiliazing variables: %s", error)
        try:
            for day in weather_data:
                dates.append(day)
                data.append(weather_data[day])
        except Exception as error:
            logging.warning("Error: line_plot: Organizing data for plot: %s", error)

        if not data:
            logging.warning("line_plot: Empty data set")

        try:
            plt.plot(dates, data)
            plt.title('Daily Average Temperatures')
            plt.ylabel('Average Temperature')
            plt.xlabel('Day')
            plt.xticks(rotation='vertical')
            plt.show()
        except Exception as error:
            logging.warning("Error: line_plot: Creating plot: %s", error)
