import { sliceByDate } from './date.js'


export function calculateAverage(values, x) {
  // Calculate a moving average from the last x values
  if (x > values.length) x = values.length
  values = values.slice(values.length-x)
  return values.reduce((a,b) => a+b, 0) / x
}

export function calculateRSI(values, x) {
  // Calculate RSI from the last x values gains and losses
  if (x > values.length) x = values.length
  values = values.slice(values.length-x)
  let gain = 0
  let loss = 0
  for (let i=0; i < values.length; i++) { // omit the last element
    if (values[i] > values[i+1])
      gain += values[i] - values[i+1]
    else if (values[i] < values[i+1])
      loss += values[i+1] - values[i]
  }
  let a = gain/x
  let b = loss/x
  if (b == 0)
    return 100
  return 100 - 100/(1 + a/b)
}

export function calculateVolume(values, hours, timestamps) {
  // Calculate Volume from a given amount of hours
  let now = new Date
  now.setTime(now.getTime() - (hours*60*60*1000))
  values = sliceByDate([values], now.toLocaleString(), timestamps)
  return values.reduce((a,b) => a+b, 0)
}
