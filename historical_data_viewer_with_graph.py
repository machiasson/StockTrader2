import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt


# Function to load and filter the data from JSON
def load_data(symbol, start_date, end_date):
    try:
        # Load the data from the respective JSON file
        file_name = f'{symbol}_historical_data.json'
        with open(file_name, 'r') as f:
            data = json.load(f)
        
        # Filter the data based on the date range
        filtered_data = [
            entry for entry in data 
            if start_date <= entry['Date'] <= end_date
        ]
        
        if not filtered_data:
            messagebox.showerror("No Data", "No data available for the selected date range.")
            return None
        
        return filtered_data

    except FileNotFoundError:
        messagebox.showerror("File Error", f"Data file for {symbol} not found.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None


# Function to plot the data using Matplotlib
def plot_graph(data, symbol, start_date, end_date):
    dates = [entry['Date'] for entry in data]
    close_prices = [entry['Close'] for entry in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label=f'{symbol} Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.title(f'{symbol} Historical Data ({start_date} to {end_date})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()


# Function to handle the 'Submit' button
def submit():
    symbol = symbol_entry.get().upper()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Validate the symbol
    if symbol not in ['FNGU', 'FNGD']:
        messagebox.showerror("Invalid Symbol", "Please enter a valid symbol (FNGU or FNGD).")
        return

    # Validate the date format
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter dates in the format YYYY-MM-DD.")
        return

    # Load the data based on user inputs
    filtered_data = load_data(symbol, start_date, end_date)
    
    if filtered_data:
        # Plot the graph using Matplotlib
        plot_graph(filtered_data, symbol, start_date, end_date)
        messagebox.showinfo("Success", "Data loaded and graph plotted successfully!")


# Set up the GUI using Tkinter
root = tk.Tk()
root.title("Historical Data Viewer")

# Create the input fields
tk.Label(root, text="Symbol (FNGU/FNGD):").grid(row=0, column=0, padx=10, pady=10)
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
start_date_entry = tk.Entry(root)
start_date_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
end_date_entry = tk.Entry(root)
end_date_entry.grid(row=2, column=1, padx=10, pady=10)

# Create the Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
