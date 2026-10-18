import tkinter as tk
from tkinter import ttk
from tkinter.font import nametofont
from queue import Empty, Queue
from threading import Thread
import logging
from data import data as fetch_quote

class Dashboard(ttk.Frame):
    def __init__(self, container):
        # Our container is a parent that as the other widgets inside it
        super().__init__(container, padding=24)
        self.loading = False
        self.responses = Queue()
        self.poll_id = None

        self.symbol = tk.StringVar()

        self.configure_styles()
        self.build_layout()
    def configure_styles(self):
        #Default OS Font
        font_family = nametofont("TkDefaultFont").actual("family")
        style = ttk.Style(self)
        
        # Modifies the visual appaerence of the themed widgets
        style.configure("Title.TLabel", font=(font_family, 22, "bold"), )
        style.configure("Price.TLabel", font=(font_family, 28, "bold"), )
        style.configure("Muted.TLabel")
        style.configure("Error.TLabel", foreground='red')
        
        style.configure("TButton", padding=(12, 6))

    def build_layout(self):
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Portfolio Tracker", style='Title.TLabel').grid(row=0, column=0, sticky="w", pady=(0, 20))
        self.build_search_bar()
        self.build_results()

    def build_search_bar(self):
        search_frame = ttk.Frame(self)
        search_frame.grid(row=1, column=0, sticky="ew")
        search_frame.columnconfigure(0, weight=1)

        ttk.Label(search_frame, text="Symbol (e.g. BTC)",).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol,)
        self.symbol_entry.grid(row=1, column=0, sticky="ew")
        self.symbol_entry.bind("<Return>", self.search)
        self.symbol_entry.focus_set()

        self.search_button = ttk.Button(search_frame,text="Search",command=self.search,)
        self.search_button.grid(row=1, column=1, padx=(10, 0))

    def build_results(self):
        result_frame = ttk.Frame(self)
        result_frame.grid(row=2,column=0,sticky="ew",pady=(24, 0),)
        result_frame.columnconfigure(0, weight=1)

        self.symbol_label = ttk.Label(result_frame,text="Search for a cryptocurrency.",style="Muted.TLabel",wraplength=400,)
        self.symbol_label.grid(row=0, column=0, sticky="w")

        self.price_label = ttk.Label(result_frame,text="",style="Price.TLabel",)
        self.price_label.grid(row=1,column=0,sticky="w",pady=(8, 6),)

        self.updated_label = ttk.Label(result_frame,text="",style="Muted.TLabel",wraplength=400,)
        self.updated_label.grid(row=2, column=0, sticky="w")

    def search(self, event=None):
        if self.loading:
            return

        symbol = self.symbol.get().strip().upper()
        
        if not symbol:
            self.show_error("Enter a symbol")
            return

        self.symbol.set(symbol)
        self.set_loading(True)

        self.symbol_label.config(text=f"Searching for {symbol}…",style="Muted.TLabel",)
        self.price_label.config(text="")
        self.updated_label.config(text="")

        Thread(target=self.fetch_in_background,args=(symbol,),daemon=True,).start()

        self.poll_id = self.after(100, self.check_response)
    
    def fetch_in_background(self, symbol):
        try:
            coin = fetch_quote(symbol)
        except Exception:
            logging.exception("Could not fetch quote for %s", symbol)
            coin = None

        self.responses.put((symbol, coin))

    def check_response(self):
        self.poll_id = None

        try:
            symbol, coin = self.responses.get_nowait()
        except Empty:
            self.poll_id = self.after(100, self.check_response)
            return

        self.set_loading(False)

        if coin is None:
            self.show_error(f"Could not fetch {symbol}. Please try again.")
            return

        self.show_quote(symbol, coin)

    def set_loading(self, loading):
        self.loading = loading

        self.search_button.config(text="Searching…" if loading else "Search",state="disabled" if loading else "normal",)
        self.symbol_entry.config(state="disabled" if loading else "normal",)

    def show_quote(self, symbol, coin):
        price = coin.get("Price")

        if price is None:
            self.show_error(f"No price available for {symbol}.")
            return

        updated = coin.get("Time") or "Unavailable"

        self.symbol_label.config(text=f"Symbol: {symbol}",style="Muted.TLabel",)
        self.price_label.config(text=f"Price: {price}")
        self.updated_label.config(text=f"Last updated: {updated}")

    def show_error(self, message):
        self.symbol_label.config(text=message,style="Error.TLabel",)
        self.price_label.config(text="")
        self.updated_label.config(text="")

    def destroy(self):
        if self.poll_id is not None:
            self.after_cancel(self.poll_id)
            self.poll_id = None

        super().destroy()

def main():
    root = tk.Tk()
    root.title("Portfolio Tracker")
    root.minsize(460, 320)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    dashboard = Dashboard(root)
    dashboard.grid(row=0, column=0, sticky="nsew")

    root.mainloop()


if __name__ == "__main__":
    main()
