from tkinter import *
from datetime import datetime
from cost_functions import user_average, showSettings

window = Tk()

wybór = IntVar()
wybórs = IntVar()

def calculator():
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")

    value = wybór.get()
    values = wybórs.get()

    ile_jednostek = int(entry1.get())
    za_ile = float(entry2.get())

    if value == 1:
        if values == 1:
            listbox.insert(END,f'{dt_string} -- Kupiono {ile_jednostek} BTC za {za_ile} PLN')
            to_do = 'buy'
            current = 'btc'

        if values == 2:
            listbox.insert(END,f'{dt_string} -- Sprzedano {ile_jednostek} BTC {za_ile} PLN')
            to_do = 'sell'
            current = 'btc'

    elif value == 2:
        if values == 1:
            listbox.insert(END,f'{dt_string} -- Kupiono {ile_jednostek} BAT {za_ile} PLN')
            to_do = 'buy'
            current = 'bat'

        if values == 2:
            listbox.insert(END,f'{dt_string} -- Sprzedano {ile_jednostek} BAT {za_ile} PLN')
            to_do = 'sell'
            current = 'bat'

    elif value == 3:
        if values == 1:
            listbox.insert(END,f'{dt_string} -- Kupiono {ile_jednostek} ZRX {za_ile} PLN')
            to_do = 'buy'
            current = 'zrx'

        if values == 2:
            listbox.insert(END,f'{dt_string} -- Sprzedano {ile_jednostek} ZRX {za_ile} PLN')
            to_do = 'sell'
            current = 'zrx'
    print(f'{to_do},,,,, {current},,,,,, {ile_jednostek},,,,, {za_ile}')
    user_average(to_do, current, ile_jednostek, za_ile)
    print(showSettings())
    # return to_do, current, ile_jednostek, za_ile




start_label = Label(window, text="Co chciałbyś uczynić młody przedsiębiorco?", font=("arial bold", 14))
start1_label = Label(window, text = "buy / sell", font=("arial bold", 14))
start2_label = Label(window, text = "Which Crypto?", font=("arial bold", 14))
start3_label = Label(window, text = "Za ile?", font=("arial bold", 14))
start4_label = Label(window, text = "Ile jednostek?", font=("arial bold", 14))

entry1 = Entry(window)
entry2 = Entry(window)

rad1 = Radiobutton(window, text="BTC", value = 1, variable=wybór)
rad2 = Radiobutton(window, text="BAT", value = 2, variable=wybór)
rad3 = Radiobutton(window, text="ZRX", value = 3, variable=wybór)

rad4 = Radiobutton(window, text="Buy", value = 1, variable=wybórs)
rad5 = Radiobutton(window, text="Sell", value = 2, variable=wybórs)

button1 = Button(window, text="Akceptuj", command= calculator, bg="green")
button2 = Button(window, text="Wyjście", command= exit, bg="red")
listbox = Listbox(window)

start_label.pack()
start1_label.pack()
rad4.pack()
rad5.pack()
start2_label.pack()
rad1.pack()
rad2.pack()
rad3.pack()

start4_label.pack()
entry1.pack()
start3_label.pack()
entry2.pack()

button1.pack(fill=X)
button2.pack(fill=X)
listbox.pack(fill=X)

window.mainloop()





