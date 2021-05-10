const API = "https://api.bitbay.net/rest/trading/ticker/";
let currency = "pln";
let cryptocurrencies = ["bsv", "btc", "dash"];
let bsv;
let xmr;
let dash;
let volume = [, ,];
let u = [];
let d = [];
let lastAverage = 0;

const fetchVolume = (crypto, i) => {
  fetch(`https://api.bitbay.net/rest/trading/stats/${crypto}-${currency}`)
    .then((res) => res.json())
    .then((data) => {
      volume[i] = data.stats.v;
    });
};

const assignStats = ({ lowestAsk, highestBid, market }, crypto) => {
  const average = (lowestAsk * 1 + highestBid * 1) / 2;

  switch (market.first.currency) {
    case "BSV":
      fetchVolume(crypto, 0);
      bsv = [lowestAsk, highestBid, average, volume[0]];
      break;
    case "BTC":
      fetchVolume(crypto, 1);
      btc = [lowestAsk, highestBid, average, volume[1]];
      const diffrence = lastAverage - average;
      if (lastAverage != 0) {
        if (diffrence >= 0) {
          u.push(diffrence);
        } else {
          d.push(diffrence * -1);
        }
      }
      lastAverage = average;
      const reducer = (accumulator, currentValue) => accumulator + currentValue;
      const RSI =
        100 -
        100 / (1 + u.reduce(reducer) / u.length / d.reduce(reducer) / d.length);

      document.querySelector(".rsi").innerHTML = `RSI: ${RSI}`;
      break;
    case "DASH":
      fetchVolume(crypto, 2);
      dash = [lowestAsk, highestBid, average, volume[2]];
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

for (let i = 0; i < 3; i++) {
  Plotly.plot(`chart-${i}`, [
    {
      y: [],
      type: "line",
      line: {
        color: "#80CAF6",
      },
      name: `${cryptocurrencies[i]} - ASK`,
    },
    {
      y: [],
      type: "line",
      line: {
        color: "#90DDF0",
      },
      name: `${cryptocurrencies[i]} - BID`,
    },
    {
      y: [],
      type: "line",
      line: {
        color: "#000000",
      },
      name: `${cryptocurrencies[i]} - AVERAGE`,
    },
    {
      y: [],
      type: "liner",
      line: {
        color: "#123123",
      },
      name: `${cryptocurrencies[i]} - VOLUME`,
    },
  ]);
}

setInterval(() => {
  console.clear();
  cryptocurrencies.map((crypto) => fetchFromApi(crypto, currency));

  Plotly.extendTraces(
    `chart-0`,
    {
      y: [[bsv[0]], [bsv[1]], [bsv[2]]],
    },
    [0, 1, 2]
  );
  Plotly.extendTraces(
    `chart-1`,
    {
      y: [[btc[0]], [btc[1]], [btc[2]]],
    },
    [0, 1, 2]
  );
  Plotly.extendTraces(
    `chart-2`,
    {
      y: [[dash[0]], [dash[1]], [dash[2]]],
    },
    [0, 1, 2]
  );

  document.querySelector(".chart-0").innerHTML = `VOLUME: ${bsv[3]}`;
  document.querySelector(".chart-1").innerHTML = `VOLUME: ${btc[3]}`;
  document.querySelector(".chart-2").innerHTML = `VOLUME: ${dash[3]}`;
}, 2000);
