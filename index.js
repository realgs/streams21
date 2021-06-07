const express = require('express')
const fetch = require('node-fetch')
const path = require('path')
const fs = require('fs');

const app = express()
const port = 3000

const STATIC = 'app/public'


app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(STATIC))


app.get('/', (req, res) => {
  res.sendFile( path.join(__dirname+'/app/public/index.html') )
})

app.get('/bitbay/transactions/:currency', async (req, res) => {
  const r = await fetch('https://api.bitbay.net/rest/trading/'
    +`transactions/${req.params['currency']}`)
  const json = await r.json()
  let buy = null
  let sell = null
  try {
    json.items.forEach(item => {
      let value = Number(item.a) * Number(item.r)
      if (item.ty == 'Buy') {
        if (buy == null || buy.rate * buy.amount < value)
          buy = { rate: Number(item.r), amount: Number(item.a) }
      } else if (item.ty == 'Sell') {
        if (sell == null || sell.rate * sell.amount > value)
          sell = { rate: Number(item.r), amount: Number(item.a) }
      }
    })
  } catch(e) {
    console.log(e)
    console.log('Most likely there were no transactions to fetch')
  }
  res.send({
    currency: req.params['currency'],
    buy: buy,
    sell: sell
  })
})

app.get('/bitbay/orderbook-limited/:currency', async (req, res) => {
  const r = await fetch('https://api.bitbay.net/rest/trading/'
    +`orderbook-limited/${req.params['currency']}/10`)
  const json = await r.json()
  let bid = null
  let ask = null
  try {
    bid = { rate: Number(json.sell[0].ra), amount: Number(json.sell[0].ca) }
  } catch {
    console.log(e)
    console.log('Most likely there were no bids to fetch')
  }
  try {
    ask = { rate: Number(json.buy[0].ra), amount: Number(json.buy[0].ca) }
  } catch(e) {
    console.log(e)
    console.log('Most likely there were no asks to fetch')
  }
  res.send({
    currency: req.params['currency'],
    bid: bid,
    ask: ask
  })
})


app.post('/save/:filename', (req, res) => {
  let filename = req.params['filename']
  let json = JSON.stringify(req.body)
  console.log(filename)
  console.log(JSON.stringify(req.body))
  let path = STATIC+'/'+filename+'.json'
  fs.writeFileSync(path, json)
})

app.post('/load/:filename', (req, res) => {
  let filename = req.params['filename']
  console.log(filename)
  let path = STATIC+'/'+filename+'.json'
  let json = JSON.parse(fs.readFileSync(path, 'utf8'))
  res.send(json)
})


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
