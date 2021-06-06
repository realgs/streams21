const API = "https://api.bitbay.net/rest/trading/ticker/";
// const axios = require("axios");
let currency = "pln";
let cryptocurrencies = ["bsv", "btc", "dash"];
let bsv = [, ,];
let btc = [, ,];
let dash = [, ,];
let bsvProf = 0;
let btcProf = 0;
let dashProf = 0;
let actualVolume = [0, 0, 0];
let previousVolume = [0, 0, 0];
let volume = [0, 0, 0];
let u = [];
let d = [];
let lastAverage = 0;
let names = [,];
let RSI = 0;
const buyForm = document.querySelector("#buy-form");
const sellForm = document.querySelector("#sell-form");

const buyStocks = async (e) => {
    e.preventDefault();
    let price;

    switch (buyForm.currencyNameBuy.value.toUpperCase()) {
        case "BSV":
            price = bsv[0];
            break;
        case "BTC":
            price = btc[0];
            break;
        case "DASH":
            price = dash[0];
            break;
        default:
            break;
    }

    const doc = {
        currency: buyForm.currencyNameBuy.value.toUpperCase(),
        numberOfStocks: buyForm.numberOfBuyStock.value * 1,
        totalSpend: buyForm.numberOfBuyStock.value * price,
        pricePerstock: price * 1,
    };

    await fetch("http://localhost:3000/stocks", {
        method: "POST",
        body: JSON.stringify(doc),
        headers: { "Content-Type": "application/json" },
    });
};

const countBuyAverage = async (crypto) => {
    const res = await fetch(`http://localhost:3000/stocks?currency=${crypto}`);
    const dataFromDb = await res.json();

    let sumOfBuyStock = 0;
    let sumTotalSpend = 0;

    dataFromDb.forEach((data) => {
        sumOfBuyStock += data.numberOfStocks;
        sumTotalSpend += data.totalSpend;
    });

    switch (crypto.toString()) {
        case "BSV":
            bsv[3] = ((sumTotalSpend * 1) / sumOfBuyStock) * 1;
            break;
        case "BTC":
            btc[3] = ((sumTotalSpend * 1) / sumOfBuyStock) * 1;
            break;
        case "DASH":
            dash[3] = ((sumTotalSpend * 1) / sumOfBuyStock) * 1;
            break;
        default:
            break;
    }
};

const handleSell = async (e) => {
    e.preventDefault();

    let sellCrypto = sellForm.currencyNameSell.value.toUpperCase();
    const res = await fetch(`http://localhost:3000/stocks?currency=${sellCrypto}`);
    const dataFromDb = await res.json();
    let sellPrice;

    switch (sellForm.currencyNameSell.value.toUpperCase()) {
        case "BSV":
            sellPrice = bsv[0];
            break;
        case "BTC":
            sellPrice = btc[0];
            break;
        case "DASH":
            sellPrice = dash[0];
            break;
        default:
            break;
    }

    let numberOfSellStocks = sellForm.numberOfSellStock.value * 1;
    let profit = 0;

    dataFromDb.forEach((data) => {
        if (data.numberOfStocks <= numberOfSellStocks) {
            profit += data.numberOfStocks * sellPrice - data.totalSpend;
            numberOfSellStocks -= data.numberOfStocks;
            console.log(profit);

            fetch(`http://localhost:3000/stocks/${data.id}`, {
                method: "DELETE",
            });
        } else {
            profit += numberOfSellStocks * (sellPrice - data.pricePerstock);

            const doc = {
                currency: data.currency,
                numberOfStocks: data.numberOfStocks - numberOfSellStocks,
                totalSpend: (data.numberOfStocks - numberOfSellStocks) * data.pricePerstock,
                pricePerstock: data.pricePerstock,
            };

            fetch(`http://localhost:3000/stocks/${data.id}`, {
                method: "PUT",
                body: JSON.stringify(doc),
                headers: { "Content-Type": "application/json" },
            });
            numberOfSellStocks = 0;
        }

        if (numberOfSellStocks === 0) {
            switch (data.currency) {
                case "BSV":
                    bsvProf += profit * 1;
                    break;
                case "BTC":
                    btcProf += profit * 1;
                    break;
                case "DASH":
                    dashProf += profit * 1;
                    break;
                default:
                    break;
            }
        }
    });
};

const fetchVolume = (crypto, i) => {
    fetch(`https://api.bitbay.net/rest/trading/stats/${crypto}-${currency}`)
        .then((res) => res.json())
        .then((data) => {
            if (actualVolume[i] == 0) {
                actualVolume[i] = data.stats.v;
            } else {
                previousVolume[i] = actualVolume[i];
                actualVolume[i] = data.stats.v;
            }

            if (previousVolume[i] != 0 && actualVolume[i] - previousVolume[i] > 0) {
                volume[i] = actualVolume[i] - previousVolume[i];
            } else {
                volume[i] = 0;
            }
        });
};

const assignStats = ({ lowestAsk, highestBid, market }, crypto) => {
    const average = (lowestAsk * 1 + highestBid * 1) / 2;

    switch (market.first.currency) {
        case "BSV":
            names[0] = market.first.currency;
            fetchVolume(crypto, 0);
            bsv = [lowestAsk, highestBid, volume[0]];
            break;
        case "BTC":
            names[1] = market.first.currency;
            fetchVolume(crypto, 1);
            btc = [lowestAsk, highestBid, volume[1]];
            const diffrence = lastAverage - average;
            if (lastAverage != 0) {
                if (diffrence >= 0) {
                    u.push(diffrence);
                } else {
                    d.push(diffrence * -1);
                }

                const reducer = (accumulator, currentValue) => accumulator + currentValue;
                RSI = 100 - 100 / (1 + u.reduce(reducer) / u.length / d.reduce(reducer) / d.length);
            }
            lastAverage = average;

            break;
        case "DASH":
            names[2] = market.first.currency;
            fetchVolume(crypto, 2);
            dash = [lowestAsk, highestBid, volume[2]];
            break;
        default:
            break;
    }
};

const fetchFromApi = (crypto, currency) => {
    fetch(API + `${crypto}-${currency}`)
        .then((res) => res.json())
        .then((data) => {
            assignStats(data.ticker, crypto);
        })
        .catch((err) => console.log(err));
};

var layout = {
    height: 400,
    xaxis: {
        type: "date",
        domain: [0, 1],
        showticklabels: false,
    },
    yaxis: { domain: [0.6, 1] },
    xaxis2: {
        type: "date",
        anchor: "y2",
        domain: [0, 1],
    },
    yaxis2: {
        anchor: "x2",
        domain: [0, 0.4],
    },
};

for (let i = 0; i < 3; i++) {
    var ask = {
        x: [],
        y: [],
        name: `ASK`,
        mode: "lines",
        line: {
            color: "#80CAF6",
        },
    };

    var bid = {
        x: [],
        y: [],
        name: "BID",
        mode: "lines",
        line: {
            color: "#008000",
        },
    };

    var buyAverage = {
        x: [],
        y: [],
        name: "AVERAGE",
        xaxis: "x2",
        yaxis: "y2",
        mode: "lines",
        line: {
            dash: "dashdot",
            width: 4,
            color: "#000",
        },
    };

    var volumeChart = {
        x: [],
        y: [],
        name: "VOLUME",
        xaxis: "x2",
        yaxis: "y2",
        type: "bar",
        line: { color: "#000" },
    };

    var data = [ask, buyAverage];
    var data2 = [bid, volumeChart];

    Plotly.plot(`chart-${i}`, data, layout);
    Plotly.plot(`chart-${i}_1`, data2, layout);
}

Plotly.plot("rsi", [
    {
        y: [],
        type: "line",
        name: "RSI",
        line: { color: "#80CAF6" },
    },
]);

buyForm.addEventListener("submit", buyStocks);
sellForm.addEventListener("submit", handleSell);

bsv[4] = 0;
btc[4] = 0;
dash[4] = 0;
setInterval(() => {
    console.clear();

    cryptocurrencies.map((crypto) => fetchFromApi(crypto, currency));

    var time = new Date();

    var updateBTC = {
        x: [[time], [time]],
        y: [[btc[0]], [btc[3]]],
    };

    var updateBTC2 = {
        x: [[time], [time]],
        y: [[btc[1]], [btc[2]]],
    };

    var updateDASH = {
        x: [[time], [time]],
        y: [[dash[0]], [dash[3]]],
    };

    var updateDASH2 = {
        x: [[time], [time]],
        y: [[dash[1]], [dash[2]]],
    };

    var updateBSV = {
        x: [[time], [time]],
        y: [[bsv[0]], [bsv[3]]],
    };

    var updateBSV2 = {
        x: [[time], [time]],
        y: [[bsv[1]], [bsv[2]]],
    };

    Plotly.extendTraces("chart-0", updateBSV, [0, 1]);
    Plotly.extendTraces("chart-0_1", updateBSV2, [0, 1]);
    Plotly.extendTraces("chart-1", updateBTC, [0, 1]);
    Plotly.extendTraces("chart-1_1", updateBTC2, [0, 1]);
    Plotly.extendTraces("chart-2", updateDASH, [0, 1]);
    Plotly.extendTraces("chart-2_1", updateDASH2, [0, 1]);

    Plotly.extendTraces(
        "rsi",
        {
            y: [[RSI]],
        },
        [0]
    );

    countBuyAverage("BTC");
    countBuyAverage("BSV");
    countBuyAverage("DASH");

    document.querySelector("#title-0").innerHTML = `${names[0]}`;
    document.querySelector("#title-1").innerHTML = `${names[1]}`;
    document.querySelector("#title-2").innerHTML = `${names[2]}`;

    document.querySelector("#profit-0").innerHTML = `${bsvProf}`;
    document.querySelector("#profit-1").innerHTML = `${btcProf}`;
    document.querySelector("#profit-2").innerHTML = `${dashProf}`;
}, 3000);
