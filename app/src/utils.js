export async function fetchOffers(currency, endpoint) {
  try {
    const res = await fetch(`/bitbay/${endpoint}/${currency}`)
    const json = await res.json()
    return json
  } catch (e) {
    console.log('Error: Connection failed')
    console.error(e);
    error = e
  }
}

export function normalizeArray(array) {
  let max = Math.max(...array)
  let min = Math.min(...array)
  return array.map(el => {
    return el - min
  }).map(el => {
    if (el == 0) return el
    return el / (max-min)
  })
}
