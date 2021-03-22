const axios = require('axios')

const getDataFromApi = async (cryptoCurrencyCode, currencyCode) => {
    const response = await axios
        .get(`https://bitbay.net/API/Public/${cryptoCurrencyCode}${currencyCode}/ticker.json`)
        .then(response => response)
        .catch(err => err)

    return {
        currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
        response: response.data
    }
}

const handleData = async (cryptoCurrencyCode, currencyCode) => {
    const data = await getDataFromApi(cryptoCurrencyCode, currencyCode)

    if(!data.response) {
        console.log(`[${cryptoCurrencyCode}] Something went wrong, please check your API.`)
        return
    }
    console.log(data)
    const { ask, bid } = data.response

    const difference = +(((ask - bid) / bid) * 100).toFixed(4)
    // const difference = +(((bid - ask) / ask) * 100).toFixed(4)

    return difference
}

const main = () => {
    cryptoCurrencyCodes = ['BTC', 'ETH', 'XLM']
    currencyCode = 'PLN'

    cryptoCurrencyCodes.forEach(async cryptoCurrencyCode => {
        const difference = await handleData(cryptoCurrencyCode, currencyCode)

        if (!difference) return

        console.log(`[${cryptoCurrencyCode}] Difference between ASK (someone's lowest sell offer) and BID (someone's highest buy offer) is ${difference}%.`)
        // console.log(`[${cryptoCurrencyCode}] Difference between BID (someone's highest buy offer) and ASK (someone's lowest sell offer) is ${difference}%.`)
    })
}

const interval = setInterval(() => {
    main()
}, 5000)
