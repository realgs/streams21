const API = 'https://api.cryptonator.com/api/full/';
let cryptocurrencies = ['bsv', 'xmr', 'dash'];
let colors = ['#EE82EE', '#FF00FF', '#000000', '#666666', '#32CD32', '#228B22']
let currency = 'usd'
let bsv;
let xmr;
let dash;


const assignStats = ({
    base,
    markets
}) => {
    switch (base) {
        case 'BSV':
            bsv = [markets[1].price, markets[2].price]
            break;
        case 'XMR':
            xmr = [markets[1].price, markets[2].price]
            break;
        case 'DASH':
            dash = [markets[1].price, markets[2].price]
            break;
        default:
            break;
    }
};

const fetchFromApi = (crypto, currency) => {
    fetch(API + crypto + `-${currency}/`)
        .then(res => res.json())
        .then(data => {
            assignStats(data.ticker)
        })
        .catch(err => console.log(err))
}

let i = 0;
let j = 0;
do {
    Plotly.plot('chart', [{
        y: [],
        type: 'line',
        line: {
            color: colors[j++]
        },
        name: `${cryptocurrencies[i]} - Fisrt Market`
    }, {
        y: [],
        type: 'line',
        line: {
            color: colors[j++]
        },
        name: `${cryptocurrencies[i++]} - Second Market`
    }, ])
} while (i < cryptocurrencies.length)

setInterval(() => {
    console.clear()
    cryptocurrencies.map(crypto => fetchFromApi(crypto, currency))
    Plotly.extendTraces('chart', {
        y: [
            [bsv[0]],
            [bsv[1]],
            [xmr[0]],
            [xmr[1]],
            [dash[0]],
            [dash[1]]
        ]
    }, [0, 1, 2, 3, 4, 5])
}, 1000);