const API = 'https://api.cryptonator.com/api/full/';
let cryptocurrency = 'btc';
let currency = 'usd'
let prices;


const assignStats = ({
    markets
}) => {
    prices = [markets[1].price, markets[2].price]
};

const fetchFromApi = (crypto, currency) => {
    fetch(API + crypto + `-${currency}/`)
        .then(res => res.json())
        .then(data => {
            assignStats(data.ticker)
        })
        .catch(err => console.log(err))
}

Plotly.plot('chart', [{
    y: [],
    type: 'line',
    line: {
        color: '#80CAF6'
    },
    name: 'BTC - First Market'
}, {
    y: [],
    type: 'line',
    line: {
        color: '#90DDF0'
    },
    name: 'BTC - Second Market'
}])

setInterval(() => {
    console.clear()

    fetchFromApi(cryptocurrency, currency)
    Plotly.extendTraces('chart', {
        y: [
            [prices[0]],
            [prices[1]]
        ]
    }, [0, 1])
}, 1000);
