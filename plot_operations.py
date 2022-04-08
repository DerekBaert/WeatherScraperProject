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
        plt.show()

# Test Data
box_data = {1: [1.1, 5.5, 6.2, 7.1], 2: [8.1, 5.4, 9.6, 4.7]}
line_data = {"2020-04-01": 1.5, "2020-04-02": 5.4, "2020-04-03": 3.5, "2020-04-04": 7.7, "2020-04-05": 6.0}

box = PlotOperations()
line = PlotOperations()

box.box_plot(box_data)
line.line_plot(line_data)
