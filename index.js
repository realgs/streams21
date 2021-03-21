const axios = require('axios')

const getDataFromApi = async (cryptoCurrencyCode, currencyCode) => {
    const response = await axios.get(`https://bitbay.net/API/Public/${cryptoCurrencyCode}${currencyCode}/ticker.json`)

    return {
        currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
        response: response.data
    }
}

