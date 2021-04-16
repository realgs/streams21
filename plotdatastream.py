import requests
import time

oscillation = 5
cryptos = ["BTC","ETH","TRX"]
currency = "USD"

def sellbuy_difference(sells, buys):
    sa,sp,ba,bp = 0,0,0,0
    for s in sells:
        sa, sp = sa+s[0],sp+s[1]
    for b in buys:
        ba, bp = ba+b[0],bp+b[1]
    sellprice = sp/sa
    buyprice= bp/ba
    return (1 - (sellprice - buyprice) / buyprice)

def handle_exceptions(req):
    try:
        r = req
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

#def graph_gen():



def cryptostream_to_plot(crypto_set, currency, oscillation):
    all_data = []
    while True:
        c_list = []
        for crypto in crypto_set:
            response = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/orderbook.json", timeout=5)
            handle_exceptions(response)
            c_list.append([crypto+"/"+currency,sellbuy_difference(response.json()['asks'], response.json()['bids'])])
        all_data.append(c_list)
        #graph_gen()
        time.sleep(oscillation)

cryptostream_to_plot(cryptos,currency, oscillation)


