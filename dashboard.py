from tkinter import *
from tkinter import ttk
from tkinter.font import nametofont
from data import data

root = Tk()
root.title("Portfolio Tracker")
root.minsize(460, 320)

font_family = nametofont("TkDefaultFont").actual("family")

frm = ttk.Frame(root, padding=10)
frm.grid()

# Main Contender
main = ttk.Frame(root, padding=24)
main.grid(row=0, column=0, sticky="nsew")
main.columnconfigure(0, weight=1)

ttk.Label( main, text="Portfolio Tracker", style="Title.TLabel",).grid(row=0, column=0, sticky="w")
entry1 = ttk.Entry(root)
entry1.grid(row=0, column=1)

result = ttk.Frame(main)
result.grid(row=4, column=0, sticky="ew")
result.columnconfigure(0, weight=1)

symbol_label = ttk.Label(result, text="Symbol", style="Muted.TLabel", wraplength=400)
symbol_label.grid(row=0, column=0, sticky="w")

price_label = ttk.Label(result, text="", style="Price.TLabel")
price_label.grid(row=1, column=0, sticky="w", pady=(6, 4))

updated_label = ttk.Label(result, text="",style="Muted.TLabel",wraplength=400)
updated_label.grid(row=2, column=0, sticky="w")

def show_error(message):
    symbol_label.config(text=message, style="Error.TLabel")
    price_label.config(text="")
    updated_label.config(text="")

def read_text():
    symbol = entry1.get().strip().upper()

    if not symbol:
        show_error("Write a Symbol")
        return

    coin = data(symbol)

    if coin is None:
        show_error("Not possible to consult the data")
        return

    price = coin.get("Price")

    if price is None:
        show_error("No Price available")
        return

    updated = coin.get("Time")
    
    if updated is None:
        show_error("Not possible to consult the data")
        return
    symbol_label.config(text=f"Name: {symbol}", style="Muted.TLabel")
    price_label.config(text=f"Price: {price}")
    updated_label.config(text=f"Last Updated: {updated}")

btn = ttk.Button(root, text="Search", command=read_text) 
btn.grid(row=0, column=3, padx=10, pady=10)
root.mainloop()
