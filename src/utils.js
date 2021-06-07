async function fetchJSONData(url) {
    let response;
    try {
        response = await fetch(url);
    } catch(error) {
        return { 
            success: false,
            data: `Unexpected error occurred during fetching data from ${url}: \n${error}`
        };
    }

    if(!response.ok) {
        return { 
            success: false,
            data: `Got wrong response status (${response.status}) during fetching data from ${url}`
        };
    }

    return {
        success: true,
        data: await response.json()
    };
}

export async function fetchTransactions(currencyPair, fromTime, limit=1) {
    const { success, data: fetchedData } = await fetchJSONData(
        `https://api.bitbay.net/rest/trading/transactions/${currencyPair}?fromTime=${fromTime}&limit=${limit}`
    );

    if (!success)
        return { success, data: fetchedData };

    const transactions = [];
    for (let i = 0; i < fetchedData['items'].length; i++)
        transactions.push({
            rate: parseFloat(fetchedData['items'][i]['r']),
            volume: parseFloat(fetchedData['items'][i]['a'])
        });

    return { 
        success,
        data: {
            time: Date.now(),
            transactions
        }
    };
}

export async function fetchBestOffers(currencyPair) {
    const { success, data: fetchedData } = await fetchJSONData(
        `https://api.bitbay.net/rest/trading/orderbook-limited/${currencyPair}/10`
    );

    if (!success)
        return { success, data: fetchedData };

    return {
        success,
        data: {
            time: Date.now(),
            sell: parseFloat(fetchedData['sell'][0]['ra']),
            buy: parseFloat(fetchedData['buy'][0]['ra'])
        }
    }
}

export function calculateAvgLastTransaction(fetchedData) {
    let rate = 0, volume = 0;

    if (!fetchedData['transactions'].length)
        return { rate, volume }
    
    for (let transaction of fetchedData['transactions']) {
        rate += transaction['rate'] * transaction['volume'];
        volume += transaction['volume'];
    }

    rate /= volume;

    return {rate, volume};
}

export function calculateRSI(transactions, rsiPeriod) {
    if (transactions.length < rsiPeriod)
        return -1;
    
    const transactionsChunk = transactions.slice(-rsiPeriod);
    let upsMean = 0, upsCounter = 0, downsMean = 0, downsCounter = 0 ;

    for (let i = 1; i < transactionsChunk.length; i++) {
        if (transactionsChunk[i-1]['y'] > transactionsChunk[i]['y']) {
            downsMean += transactionsChunk[i-1]['y'] - transactionsChunk[i]['y'];
            downsCounter++;
        } else if (transactionsChunk[i-1]['y'] < transactionsChunk[i]['y']) {
            upsMean += transactionsChunk[i]['y'] - transactionsChunk[i-1]['y'];
            upsCounter++;
        }
    }

    if (!!upsCounter)
        upsMean /= upsCounter;

    if (!!downsCounter)
        downsMean /= downsCounter;
    else
        downsMean = 1

    return 100 - (100 / (1 + (upsMean / downsMean)));
}

export function isLiquidAsset(sellsOffers, buysOffers, S) {
    if (!sellsOffers.length || !buysOffers.length)
        return false;
    
    return (Math.abs(sellsOffers[-1][0] - buysOffers[-1][0]) / sellsOffers[-1][0]) * 100 < S;
}

export function isVolatileAsset(transactions, X, Y) {
    if (transactions.length < Y)
        return false;

    const transactionsChunk = transactions.slice(-Y),
        chunkMin = Math.min(...transactionsChunk), 
        chunkMax = Math.max(...transactionsChunk);

    return ((chunkMax - chunkMin) / chunkMin) * 100 > X;
}

export function getTrendSymbol(rsi, period) {
    if (rsi.length < period)
        return '';
    
    const rsiChunk = rsi.slice(-period),
        rsiMean = rsiChunk.reduce((total, rsi) => { return total+rsi.y }, 0) / rsiChunk.length;

    if (rsiMean > 70)
        return '⬆';
    else if (rsiMean < 30)
        return '⬇';
    else
        return '~'
}

export function downloadJSON(obj, name){
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(obj));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", name + ".json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  }