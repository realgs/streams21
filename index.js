const axios = require('axios')

const getDataFromApi = async (cryptoCurrencyCode, currencyCode) => {
    const response = await axios.get(`https://bitbay.net/API/Public/${cryptoCurrencyCode}${currencyCode}/ticker.json`)

    return {
        currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
        response: response.data
    }
}

const handleData = async (cryptoCurrencyCode, currencyCode) => {
    const data = await getDataFromApi(cryptoCurrencyCode, currencyCode)
    console.log(data)

    const { ask, bid } = data.response

    const difference = +(((ask - bid) / bid) * 100).toFixed(4)
    // const difference = +(((bid - ask) / ask) * 100).toFixed(4)

    return difference
}