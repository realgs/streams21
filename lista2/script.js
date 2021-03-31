const API = 'https://api.cryptonator.com/api/full/';
let cryptocurrencies = ['btc', 'bch', 'btg']

const calcDifference = (markets) => {   
    difference = (1 - (markets[1].price - markets[2].price) / markets[2].price)
    console.log(`The price difference between "${markets[1].market}" and "${markets[2].market}" is ${difference.toFixed(5)}%`)
}

const showStats = ({base, price, markets}) => {
    console.log(`1 ${base} is worth $${price}`);
    calcDifference(markets);
    console.log()

}

const fetchFromApi = (crypto) => {
    fetch(API + crypto + '-usd/')
        .then(res => res.json())
        .then(data => showStats(data.ticker))
        .catch(res => console.log(res))
}
  
setInterval(() => {
    console.clear()
    cryptocurrencies.map(crypto => fetchFromApi(crypto))    
}, 5000);