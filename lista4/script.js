const API = "https://api.bitbay.net/rest/trading/ticker/";
let currency = "pln";
let cryptocurrencies = ["bsv", "btc", "dash"];
let bsv;
let xmr;
let dash;
let actualVolume = [0, 0, 0];
let previousVolume = [0, 0, 0];
let volume = [0, 0, 0];
let u = [];
let d = [];
let lastAverage = 0;
let names = [,];
let RSI = 0;

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
      bsv = [lowestAsk, highestBid, average, volume[0]];
      break;
    case "BTC":
      names[1] = market.first.currency;
      fetchVolume(crypto, 1);
      btc = [lowestAsk, highestBid, average, volume[1]];
      const diffrence = lastAverage - average;
      if (lastAverage != 0) {
        if (diffrence >= 0) {
          u.push(diffrence);
        } else {
          d.push(diffrence * -1);
        }

        const reducer = (accumulator, currentValue) =>
          accumulator + currentValue;
        RSI =
          100 -
          100 /
            (1 + u.reduce(reducer) / u.length / d.reduce(reducer) / d.length);
      }
      lastAverage = average;

      break;
    case "DASH":
      names[2] = market.first.currency;
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

  var average = {
    x: [],
    y: [],
    name: "AVERAGE",
    xaxis: "x2",
    yaxis: "y2",
    mode: "lines",
    line: { color: "#000" },
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

  var data = [ask, average];
  var data2 = [bid, volumeChart];

  Plotly.plot(`chart-${i}`, data, layout);
  Plotly.plot(`chart-${i}_1`, data2, layout);
}

function rand() {
  return Math.random();
}

Plotly.plot("rsi", [
  {
    y: [],
    type: "line",
    name: "RSI",
    line: { color: "#80CAF6" },
  },
]);

setInterval(() => {
  console.clear();
  cryptocurrencies.map((crypto) => fetchFromApi(crypto, currency));

  var time = new Date();

  var updateBTC = {
    x: [[time], [time]],
    y: [[btc[0]], [btc[2]]],
  };

  var updateBTC2 = {
    x: [[time], [time]],
    y: [[btc[1]], [btc[3]]],
  };

  var updateDASH = {
    x: [[time], [time]],
    y: [[dash[0]], [dash[2]]],
  };

  var updateDASH2 = {
    x: [[time], [time]],
    y: [[dash[1]], [dash[3]]],
  };

  var updateBSV = {
    x: [[time], [time]],
    y: [[bsv[0]], [bsv[2]]],
  };

  var updateBSV2 = {
    x: [[time], [time]],
    y: [[bsv[1]], [bsv[3]]],
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

  document.querySelector("#title-0").innerHTML = `${names[0]}`;
  document.querySelector("#title-1").innerHTML = `${names[1]}`;
  document.querySelector("#title-2").innerHTML = `${names[2]}`;
}, 2000);
