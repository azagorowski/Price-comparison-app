import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime, timedelta
import pandas as pd

class PriceRatioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gold vs Bitcoin Price Ratio")
        self.root.geometry("600x400")

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create refresh button
        self.refresh_button = ttk.Button(self.main_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.grid(row=0, column=0, pady=10)

        # Create label for last refresh time
        self.refresh_label = ttk.Label(self.main_frame, text="")
        self.refresh_label.grid(row=1, column=0, pady=5)

        # Create treeview for data display
        self.tree = ttk.Treeview(self.main_frame, columns=("Date", "Gold Price (USD)", "Bitcoin Price (USD)", "Gold/BTC Ratio"), show="headings")
        self.tree.grid(row=2, column=0, pady=10)

        # Configure treeview columns
        self.tree.heading("Date", text="Date")
        self.tree.heading("Gold Price (USD)", text="Gold Price (USD)")
        self.tree.heading("Bitcoin Price (USD)", text="Bitcoin Price (USD)")
        self.tree.heading("Gold/BTC Ratio", text="Gold/BTC Ratio")

        # Configure column widths
        self.tree.column("Date", width=100)
        self.tree.column("Gold Price (USD)", width=150)
        self.tree.column("Bitcoin Price (USD)", width=150)
        self.tree.column("Gold/BTC Ratio", width=150)

        # Initial data load
        self.refresh_data()

    def get_gold_prices(self):
        # Using Gold API (you need to replace 'YOUR_API_KEY' with actual API key)
        api_key = 'YOUR_GOLD_API_KEY'
        url = f'https://www.goldapi.io/api/XAU/USD'
        headers = {'x-access-token': api_key}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['price']
            else:
                return None
        except Exception as e:
            print(f"Error fetching gold price: {e}")
            return None

    def get_bitcoin_prices(self):
        # Using CoinGecko API (free, no API key required)
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin']['usd']
            else:
                return None
        except Exception as e:
            print(f"Error fetching bitcoin price: {e}")
            return None

    def refresh_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get current prices
        gold_price = self.get_gold_prices()
        bitcoin_price = self.get_bitcoin_prices()

        if gold_price and bitcoin_price:
            ratio = gold_price / bitcoin_price
            current_date = datetime.now()

            # Insert data into treeview
            self.tree.insert("", "end", values=(
                current_date.strftime("%Y-%m-%d"),
                f"${gold_price:,.2f}",
                f"${bitcoin_price:,.2f}",
                f"{ratio:.6f}"
            ))

            # Update refresh time label
            self.refresh_label.config(text=f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.refresh_label.config(text="Error fetching data. Please try again.")

def main():
    root = tk.Tk()
    app = PriceRatioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
