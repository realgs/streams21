// import axios from 'axios'

const getDataFromApi = async (cryptoCurrencyCode, currencyCode) => {
    // const response = await axios
    //     .get(`https://bitbay.net/API/Public/${cryptoCurrencyCode}${currencyCode}/ticker.json`)
    //     .then(response => response)
    //     .catch(err => err)

    const response = await fetch(`https://bitbay.net/API/Public/${cryptoCurrencyCode}${currencyCode}/ticker.json`)
                        .then(response => response)
                        .catch(error => error)

    return {
        currencies: `${cryptoCurrencyCode} -> ${currencyCode}`,
        response: await response.json()
    }
}

export const handleData = async (cryptoCurrencyCode, currencyCode) => {
    const data = await getDataFromApi(cryptoCurrencyCode, currencyCode)

    if(!data.response) {
        return { error: true, message: `[${cryptoCurrencyCode}] Something went wrong, please check your API.` }
    }

    const { ask, bid } = data.response

    const difference = +(((ask - bid) / bid) * 100).toFixed(4)
    // const difference = +(((bid - ask) / ask) * 100).toFixed(4)

    return { ask, bid, difference }
}