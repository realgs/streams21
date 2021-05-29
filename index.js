const express = require('express')
const fetch = require('node-fetch');
const path = require('path')
const app = express()
const port = 3000


app.use(express.static('app/public'))

app.get('/', (req, res) => {
  res.sendFile( path.join(__dirname+'/app/public/index.html') )
})

app.get('/bitbay/transactions/:currency', async (req, res) => {
  const r = await fetch('https://api.bitbay.net/rest/trading/'
    +`transactions/${req.params['currency']}`)
  const json = await r.json()
  let [ highestBuyRate, highestBuyAmount, highestBuyValue ] = [null,null,null]
  let [ lowestSellRate, lowestSellAmount, lowestSellValue ] = [null,null,null]
  json.items.forEach(item => {
    let value = Number(item.a) * Number(item.r)
    if (item.ty == 'Buy') {
      if (highestBuyValue == null || highestBuyValue < value) {
        highestBuyRate = Number(item.r)
        highestBuyAmount = Number(item.a)
        highestBuyValue = value
      }
    } else if (item.ty == 'Sell') {
      if (lowestSellValue == null || lowestSellValue > value) {
        lowestSellRate = Number(item.r)
        lowestSellAmount = Number(item.a)
        lowestSellValue = value
      }
    }
  });
  res.send({
    currency: req.params['currency'],
    buy:  { rate: highestBuyRate, amount: highestBuyAmount },
    sell: { rate: lowestSellRate, amount: lowestSellAmount  }
  })
})

app.get('/bitbay/orderbook-limited/:currency', async (req, res) => {
  const r = await fetch('https://api.bitbay.net/rest/trading/'
    +`orderbook-limited/${req.params['currency']}/10`)
  const json = await r.json()
  res.send({
    currency: req.params['currency'],
    bid: { rate: Number(json.sell[0].ra), amount: Number(json.sell[0].ca) },
    ask: { rate: Number(json.buy[0].ra),  amount: Number(json.buy[0].ca)  }
  })
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
