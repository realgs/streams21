import axios from './axiosInstance'

const API_URL = 'https://api-pub.bitfinex.com/v2/'

const getTickerData = async (cryptoCurrencyCode, currencyCode) => {
  const path = 'ticker/'
  const param = `t${cryptoCurrencyCode}${currencyCode}`

  const response = await axios
    .get(`${API_URL}${path}${param}`)
    .then((response) => response)
    .catch((err) => err)

  return {
    currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
    response: response.data,
  }
}

const getTransactionsData = async (cryptoCurrencyCode, currencyCode) => {
  const path = 'candles/'
  const param = `trade:1m:t${cryptoCurrencyCode}${currencyCode}/last`

  const response = await axios
    .get(`${API_URL}${path}${param}`)
    .then((response) => response)
    .catch((err) => err)

  return {
    currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
    response: response.data,
  }
}

export const handleData = async (cryptoCurrencyCode, currencyCode) => {
  const tickerData = await getTickerData(cryptoCurrencyCode, currencyCode)
  const transactionData = await getTransactionsData(
    cryptoCurrencyCode,
    currencyCode
  )

  if (!tickerData.response || !transactionData.response) {
    console.error(
      `[${cryptoCurrencyCode}] Something went wrong, please check your API.`
    )
    return
  }

  const bid = tickerData.response[0]
  const ask = tickerData.response[2]

  const difference = +(((ask - bid) / bid) * 100).toFixed(4)

  const open = transactionData.response[1]
  const close = transactionData.response[2]
  const volume = transactionData.response[5]

  const parsedTickerData = { ask, bid, difference, volume }
  const parsedTransactionData = { open, close, volume }

  return [parsedTickerData, parsedTransactionData]
}
