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
  let [ highestBidRate, highestBidAmount, highestBidValue ] = [null,null,null]
  let [ lowestAskRate, lowestAskAmount, lowestAskValue ] = [null,null,null]
  json.items.forEach(item => {
    let value = Number(item.a) * Number(item.r)
    if (item.ty == 'Buy') {
      if (highestBidValue == null || highestBidValue < value) {
        highestBidRate = Number(item.r)
        highestBidAmount = Number(item.a)
        highestBidValue = value
      }
    } else if (item.ty == 'Sell') {
      if (lowestAskValue == null || lowestAskValue > value) {
        lowestAskRate = Number(item.r)
        lowestAskAmount = Number(item.a)
        lowestAskValue = value
      }
    }
  });
  res.send({
    currency: req.params['currency'],
    bid: { rate: highestBidRate, amount: highestBidAmount },
    ask: { rate: lowestAskRate,  amount: lowestAskAmount  }
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
