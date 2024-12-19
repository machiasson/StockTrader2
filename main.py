import yfinance as yf
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # For embedding matplotlib in tkinter

# Define the stock symbols and date range
stock_symbols = ['FNGU', 'FNGD']
start_date = '2021-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')  # Today's date


# Adapter Pattern: Data Access Layer
class DataAccessLayer:
    def fetch_data(self, symbol, start, end):
        raise NotImplementedError("This method should be implemented by subclasses")


class YahooFinanceAdapter(DataAccessLayer):
    def fetch_data(self, symbol, start, end):
        return yf.download(symbol, start=start, end=end)


# Decorator Pattern: Add functionalities dynamically
class PlotDecorator:
    def __init__(self, plot_function):
        self.plot_function = plot_function

    def __call__(self, *args, **kwargs):
        fig, ax = self.plot_function(*args, **kwargs)
        self.decorate_plot(ax)
        return fig, ax

    def decorate_plot(self, ax):
        ax.grid(True)
        ax.legend()


# Strategy Pattern: Interchangeable data processing strategies
class DataProcessingStrategy:
    def process(self, data):
        raise NotImplementedError("This method should be implemented by subclasses")


class NoProcessingStrategy(DataProcessingStrategy):
    def process(self, data):
        return data


class SortByVolumeStrategy(DataProcessingStrategy):
    def process(self, data):
        return data.sort_values(by="Volume", ascending=False)


# Main GUI Application
class Window:
    def __init__(self, data_layer):
        # Initialize tkinter
        self.root = tk.Tk()
        self.root.geometry("800x600")  # Adjusted for better display

        self.data_layer = data_layer
        self.processing_strategy = NoProcessingStrategy()  # Default strategy

        # Selection box for symbols
        self.selectionBox = ttk.Combobox(self.root, state="readOnly", values=stock_symbols)
        self.selectionBox.place(x=10, y=50)
        self.selectionBox.bind("<<ComboboxSelected>>", self.plot_stock_data)  # Bind selection to plot function

        # Display start and end dates
        self.start_label = tk.Label(self.root, text="Start Date: " + start_date)
        self.end_label = tk.Label(self.root, text="End date: " + end_date)
        self.start_label.place(x=10, y=10)
        self.end_label.place(x=10, y=30)

        # Placeholder for the plot canvas
        self.canvas = None

        # Dropdown for data processing strategies
        self.strategyBox = ttk.Combobox(
            self.root,
            state="readOnly",
            values=["No Processing", "Sort by Volume"]
        )
        self.strategyBox.place(x=10, y=80)
        self.strategyBox.bind("<<ComboboxSelected>>", self.change_strategy)

        # Loop for tkinter
        self.root.mainloop()

    def change_strategy(self, event):
        strategy = self.strategyBox.get()
        if strategy == "No Processing":
            self.processing_strategy = NoProcessingStrategy()
        elif strategy == "Sort by Volume":
            self.processing_strategy = SortByVolumeStrategy()

    @PlotDecorator
    def plot_stock_data(self, event):
        selected_symbol = self.selectionBox.get()
        raw_data = self.data_layer.fetch_data(selected_symbol, start_date, end_date)

        # Process data using the selected strategy
        historical_data = self.processing_strategy.process(raw_data)

        dates = historical_data.index
        close_prices = historical_data['Close']

        # Create the figure and plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, close_prices, label=selected_symbol)
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price")
        ax.set_title(f"Closing Price of {selected_symbol}")
        return fig, ax

    def render_plot(self, fig):
        # Clear previous plot if it exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Embed the plot in tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=100, y=100)  # Adjust the placement


# Main execution
if __name__ == "__main__":
    data_layer = YahooFinanceAdapter()  # Use Yahoo Finance Adapter
    Window(data_layer)
