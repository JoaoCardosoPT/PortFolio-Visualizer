from tkinter import *
from tkinter import ttk
from data import data

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

root.title("Portfolio Tracker")
ttk.Label(root, text="Symbol", font=("Arial", 12)).grid(row=0, column=0)

entry1 = ttk.Entry(root)
entry1.grid(row=0, column=1)

result = ttk.Label(root, text="", font=("Arial", 10), justify="left", padding=15)
result.grid(row=1, column=0, columnspan=3, pady=10)

def read_text():
    symbol = entry1.get().strip().upper()

    if not symbol:
        result.config(text="Write a Symbol")
        return

    coin = data(symbol)

    if coin is None:
        result.config(text="Not possible to consult the data")
        return

    price = coin.get("Price")

    if price is None:
        result.config(text="No Price available")
        return

    updated = coin.get("Time")
    
    if updated is None:
        result.config(text="Not possible to consult the data")
        return
    result.config(text=f"Name: {symbol}\n" f"Price: {price}\n" f"Last Updated: {updated}")

def use_enter(event=None):
    read_text()

entry1.bind("<Return>", use_enter)

btn = ttk.Button(root, text="Search", command=read_text) 
btn.grid(row=0, column=3, padx=10, pady=10)
root.mainloop()