from tkinter.constants import BOTH, BOTTOM
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import Label, Widget, ttk
from tkinter import messagebox
from L5 import dataFrame, getPath, getOffers, getData, getTransa, plotData, read_from_js, save_to_jsn, volatile_asset, liquid_asset, calculate_mean
import json

matplotlib.use("TkAgg")

LARGE_FONT= ("Verdana", 12)
CURRIENCES = ['LTCPLN', 'ETHPLN', 'XRPPLN']
SLEEP_TIME = 4
URL_BEG = 'https://bitbay.net/API/Public/'
URL_END = '/ticker.json'
URL_TRAN = 'https://api.bitbay.net/rest/trading/transactions/'
MEAN_PEROID = 3
RSI_PEROID = 6
RSI_GRAPH = 6
GRAPH_SIZE = 6
FILENAME = 'user_data.json'
VOLATILE_MIN = 0
VOLATILE_MAX = 10
ANNOTATE_X = 1.06


class CryptoApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.geometry(self, newGeometry='2200x1200')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def load_data(x,name):
        user_buy_data, res = read_from_js(name)
    
        if res == 1:
            for cur in CURRIENCES:
                prices[cur]['mean_buy_price'], prices[cur]['wallet_amount'] = calculate_mean(user_buy_data[cur], True)
        messagebox.showinfo('OK','Dane zostały załadowane pomyślnie!')

    def zrobto(self, data):
        cur = data['cur']
        amount = float(data['amount'])
        price = float(data['price'])
        type = data['type']

        if type == 'buy':
            user_buy_data[cur].append([amount, price])
            b_op = int(prices[cur]['wallet_amount'])
            b_pr = float(prices[cur]['mean_buy_price'])
            sr = ((b_op * b_pr) + (amount * price)) / (b_op + amount)

            prices[cur]['mean_buy_price'] = sr
            prices[cur]['wallet_amount'] = b_op + amount
            messagebox.showinfo('Transakcja została dodana do twojej histori!', f'Ilość {cur[:3]} w portfelu: {prices[cur]["wallet_amount"]}')
            
        if type == 'sell':
            wallet_amount = prices[cur]['wallet_amount']
            if amount > wallet_amount:
                messagebox.showwarning('Error', f"Nie masz wystarczająco {cur[:3]} do wykonania operacji")
                return

            prices[cur]['wallet_amount'] = wallet_amount - amount
            wallet = user_buy_data[cur]
            paid = 0
            sold = amount * price

            while amount > 0:
                trans = wallet[0]

                if trans[0] - amount <= 0:
                    paid += amount * trans[1]
                    amount -= trans[0]
                    
                    del wallet[0]

                else:
                    paid += amount * trans[1]
                    trans[0] -= amount
                    amount = 0

            print(wallet)
            user_buy_data[cur] = wallet
            prices[cur]['mean_buy_price'] = calculate_mean(user_buy_data[cur])
            messagebox.showinfo('Transakcja została dodana do twojej histori!', f'Ilość {cur[:3]} w portfelu: {prices[cur]["wallet_amount"]}\nŚrednia cena: {prices[cur]["mean_buy_price"]}\nZysk z transakcji: {sold-paid}')
        
        save_to_jsn(user_buy_data)
        print(user_buy_data[cur])
        


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        frame1 = tk.Frame(self)
        frame1.pack(fill=BOTH)
        button = ttk.Button(frame1, text="Zobacz wykresy", command=lambda: controller.show_frame(GraphPage), width=42)
        button.pack(side=tk.LEFT, anchor=tk.N, padx=20,pady=20)

        frame2 = tk.Frame(self)
        frame2.pack(fill=BOTH)
        label = tk.Label(frame2, text="Dodaj transakcje: ", width = 40)
        label.config(font=("Courier", 10))
        label.pack(side=tk.LEFT, padx=0, pady=0)

        frame3 = tk.Frame(self)
        frame3.pack(fill=BOTH)
        cb_value = tk.StringVar()
        curbox = ttk.Combobox(frame3, textvariable = cb_value, width=40)
        curbox['values'] = ('LTCPLN', 'ETHPLN', 'XRPPLN')
        curbox.current(0)
        curbox.pack(side=tk.LEFT, padx=20,pady=5)

        frame4 = tk.Frame(self)
        frame4.pack(fill=BOTH)
        label = tk.Label(frame4, text="Ilość:", width = 10)
        label.config(font=("Courier", 10))
        label.pack(side=tk.LEFT, padx=0, pady=0)
        entry_ile = ttk.Entry(frame4, width = 28)
        entry_ile.pack(side=tk.LEFT, anchor=tk.N, padx=20,pady=20)

        frame5 = tk.Frame(self)
        frame5.pack(fill=BOTH)
        label = tk.Label(frame5, text="Cena za sztukę:", padx=18)
        label.config(font=("Courier", 10))
        label.pack(side=tk.LEFT)
        entry_cena = ttk.Entry(frame5, width=19)
        entry_cena.pack(side=tk.LEFT)

        frame6 = tk.Frame(self)
        frame6.pack(fill=BOTH)
        button_buy = ttk.Button(frame6, text="Dodaj do kupionych", command=lambda: controller.zrobto({'cur':cb_value.get(), 'amount':entry_ile.get(), 'price':entry_cena.get(), 'type':'buy'}))
        button_buy.pack(side=tk.LEFT, padx=20, pady=15)

        button_sell = ttk.Button(frame6, text="Dodaj do sprzedanych", command=lambda: controller.zrobto({'cur':cb_value.get(), 'amount':entry_ile.get(), 'price':entry_cena.get(), 'type':'sell'}))
        button_sell.pack(side=tk.LEFT)

        frame2 = tk.Frame(self)
        frame2.pack(fill=BOTH)
        label = tk.Label(frame2, text="Wczytaj dane z pliku: ", width = 40)
        label.config(font=("Courier", 10))
        label.pack(side=tk.LEFT, padx=0, pady=0)

        frame5 = tk.Frame(self)
        frame5.pack(fill=BOTH)
        label = tk.Label(frame5, text="Nazwa pliku:", padx=18)
        label.config(font=("Courier", 10))
        label.pack(side=tk.LEFT,pady=10)
        entry_name = ttk.Entry(frame5, width=24)
        entry_name.pack(side=tk.LEFT)

        frame10 = tk.Frame(self)
        frame10.pack(fill=BOTH)
        button = ttk.Button(frame10, text="Wczytaj dane", command=lambda: controller.load_data(entry_name.get()), width=42)
        button.pack(side=tk.LEFT, anchor=tk.N, padx=20,pady=10)
    

class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Wróć na stronę główną", command=lambda: controller.show_frame(StartPage), width=40)
        button1.pack()
    

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def plotLoop(i):

    time_data_p, prices_p = plotData(time_data, prices)
    time_data_p = time_data_p[-GRAPH_SIZE:]
    for i, graph in enumerate(graphs):
        cur = CURRIENCES[i]
        graph.clear()
        graphs_twinx_mean[i].clear()
        graph.plot(time_data_p, prices[cur]['buy'][-GRAPH_SIZE:], label=f'Buy')
        graph.plot(time_data_p, prices[cur]['sell'][-GRAPH_SIZE:], label=f'Sell')
        graph.set_ylabel('Price')
        graph.set_title(cur)
        srednia = float(prices[cur]['mean_buy_price']) 
        if srednia > 0:
            graphs_twinx_mean[i].plot(time_data_p, [srednia for x in range(len(time_data_p))], color='k', linestyle='dashed', linewidth=1, label=f'Buy mean')
            
        graph.legend(bbox_to_anchor=(ANNOTATE_X, 1), loc='upper left', borderaxespad=0.)
        graph.set_xticks(time_data_p)
        graph.set_xmargin(-0.1)
    
        volume = prices[cur]['volume'][-1]
        tekst = f'Wolumen:{round(volume,2)}'
        graph.annotate(tekst, xy=(ANNOTATE_X, 0.5), xycoords='axes fraction')
        rsi = prices[cur]['rsi']
        tekst = f'Rsi:{round(rsi[-1],2)}'
        graph.annotate(tekst, xy=(ANNOTATE_X, 0.6), xycoords='axes fraction')

        
        

        if rsi[-1] != 0:
            trend = prices[cur]['trend'][1]
            tekst = f'Trend: {trend}'
            graph.annotate(tekst, xy=(ANNOTATE_X, 0.4), xycoords='axes fraction')
        
        else:
            trend = prices[cur]['trend'][1]
            tekst = f'Trend:'
            graph.annotate(tekst, xy=(ANNOTATE_X, 0.4), xycoords='axes fraction')

        if prices[cur]['candidate'] == 1:
            tekst = '<- Kandydat'
            graph.annotate(tekst, xy=(ANNOTATE_X, 0.3), xycoords='axes fraction')
            volatile = volatile_asset(cur, VOLATILE_MIN, VOLATILE_MAX)
            graph.annotate(volatile, xy=(ANNOTATE_X, 0.2), xycoords='axes fraction')
            liquid = liquid_asset(cur, 50)
            graph.annotate(liquid, xy=(ANNOTATE_X, 0.1), xycoords='axes fraction')

    for i, graph in enumerate(graphs_rsi):
        cur = CURRIENCES[i]
        graph.clear()
        graphs_twinx[i].clear()
        graph.set_title(cur + ' RSI')
        graph.plot(time_data_p, prices[cur]['rsi'][-RSI_GRAPH:], linestyle='dashed', label=f'{cur} RSI')
        graph.set_xticks(time_data_p)
        graph.set_xmargin(-0.1)
        graphs_twinx[i].bar(time_data_p, prices[cur]['volume'][-RSI_GRAPH:], alpha = 0.2, color='white', edgecolor='blue', label = 'Volume' )
        graph.legend(bbox_to_anchor=(0.8, 0.95), loc='upper left', borderaxespad=0.)
        graphs_twinx[i].legend(bbox_to_anchor=(0.8, 0.8), loc='upper left', borderaxespad=0.)
        graphs_twinx[i].set_ylim(bottom=0)
        graphs_twinx[i].set_xmargin(-0.1)



if __name__ == '__main__':
    f = Figure(figsize=(5,5), dpi=100)
    f.subplots_adjust(hspace=0.3, wspace=0.3)

    graph1 = f.add_subplot(321)
    graph1_rsi = f.add_subplot(322)
    graph2 = f.add_subplot(323)
    graph2_rsi = f.add_subplot(324)
    graph3 = f.add_subplot(325)
    graph3_rsi = f.add_subplot(326)

    graphs_rsi = [graph1_rsi, graph2_rsi, graph3_rsi]
    graphs_twinx = [x.twinx() for x in graphs_rsi]
    graphs = [graph1, graph2, graph3]
    graphs_twinx_mean = [x.twinx() for x in graphs]
    


    time_data = []
    prices = dataFrame()
    user_buy_data, res = read_from_js(FILENAME)
    
    if res == 1:
        for cur in CURRIENCES:
            prices[cur]['mean_buy_price'], prices[cur]['wallet_amount'] = calculate_mean(user_buy_data[cur], True)


    app = CryptoApp()
    ani = animation.FuncAnimation(f, plotLoop, interval=1000*SLEEP_TIME)
    plt.show()
    app.mainloop()