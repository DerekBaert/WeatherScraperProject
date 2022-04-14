"""
Handles the creation of the box and line plots.
"""
import matplotlib.pyplot as plt
import numpy as np

class PlotOperations():
    """Class for receiving weather data"""

    def initialize(self):
        """Initialize the class instance"""

    def box_plot(self, weather_data):
        """
        Takes in a dictionary of lists containing average temps for each month over a range of years and plots them on a box plot.
        """
        data = []
        for month in weather_data:
            data.append(weather_data[month])

        plt.boxplot(data)
        plt.ylabel('Average Temperature')
        plt.xlabel('Month')
        plt.show()

    def line_plot(self, weather_data):
        """
        Takes in a dictionary of daily average temperatures for a month and plots them on a line plot.
        """
        data = []
        dates = []
        for day in weather_data:
            dates.append(day)
            data.append(weather_data[day])
        plt.plot(dates, data)
        plt.title('Daily Average Temperatures')
        plt.ylabel('Average Temperature')
        plt.xlabel('Day')
        plt.xticks(rotation='vertical')
        plt.show()
