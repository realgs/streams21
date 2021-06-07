export class Transaction {
    constructor(type, currencyPair, volume, price, rate=null) {
        this.type = type;
        this.currencyPair = currencyPair;
        this.volume = volume;
        this.price = price;

        if(!rate)
            this.rate = +(price/volume).toFixed(2);
        else
            this.rate = rate;
    }

    get volumeCurrency() {
        return this.currencyPair.split("-")[0];
    }

    get priceCurrency() {
        return this.currencyPair.split("-")[1];
    }

    clone() {
        return new Transaction(this.type, this.currencyPair, this.volume, this.price, this.rate);
    }
}

export function calculateProfit(currencyPair, transactions) {
    let profit = 0, sells = [], buys = [];

    for (let transaction of transactions) {
        if(transaction.currencyPair != currencyPair) 
            continue;
        
        if (transaction.type == 'Sell') {
            sells.push(transaction.clone());
        } else if(transaction.type == 'Buy')
            buys.push(transaction.clone())

        
    }

    let sIndex = 0, bIndex = 0;
        
    while(sIndex != sells.length) {
        if (sells[sIndex]['volume'] == buys[bIndex]['volume']) {
            profit += sells[sIndex]['volume'] * sells[sIndex]['rate'] - buys[bIndex]['volume'] * buys[bIndex]['rate'];
            sIndex++;
            bIndex++;
        } else if (sells[sIndex]['volume'] > buys[bIndex]['volume']) {
            sells[sIndex]['volume'] -= buys[bIndex]['volume'];
            profit += buys[bIndex]['volume'] * sells[sIndex]['rate'] - buys[bIndex]['price'];
            bIndex++;
        } else { // sells[sIndex]['volume'] < buys[bIndex]['volume']
            profit += sells[sIndex]['volume'] * sells[sIndex]['rate']-sells[sIndex]['volume'] * buys[bIndex]['rate'];
            sIndex++;
        }
    }

    return +profit.toFixed(2) ;
}

export function sumVolume(currencyPair, transactions) {
    let volume = 0;
    for (let transacton of transactions) {
        if (transacton.currencyPair !== currencyPair)
            continue;
        
        let type = transacton.type;
        if(type == 'Buy') {
            volume += transacton.volume;
        } else if (type == 'Sell') {
            volume -= transacton.volume;
        }
    }

    return volume;
}

export function avgBuyRate(currencyPair, transactions) {
    let sells = [], buys = [];

    for (let transaction of transactions) {
        if(transaction.currencyPair != currencyPair) 
            continue;
        
        if (transaction.type == 'Sell') {
            sells.push(transaction.clone());
        } else if(transaction.type == 'Buy')
            buys.push(transaction.clone())
    }

    let sIndex = 0, bIndex = 0;
    
    while(sIndex != sells.length) {
        if (sells[sIndex]['volume'] == buys[bIndex]['volume']) {
            sIndex++;
            bIndex++;
        } else if (sells[sIndex]['volume'] > buys[bIndex]['volume']) {
            sells[sIndex]['volume'] -= buys[bIndex]['volume'];
            bIndex++;
        } else { // sells[sIndex]['volume'] < buys[bIndex]['volume']
            sIndex++;
        }
    }

    let avgRate = 0, volumes = 0;
    for (let i = bIndex; i < buys.length; i++) {
        avgRate += buys[i].volume * buys[i].rate;
        volumes += buys[i].volume;
    }

    avgRate /=volumes;

    return +avgRate.toFixed(2);
}