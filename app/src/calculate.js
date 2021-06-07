function sliceValues(values, x) {
  // Slice an array of values if possible
  if (x > values.length) x = values.length
  return values.slice(values.length-x)
}

export function getSum(values, x) {
  // Calculate a sum from x last values
  return sliceValues(values, x).reduce((a,b) => a+b, 0)
}

export function getAvg(values, x) {
  // Calculate an average from x last values
  values = sliceValues(values, x)
  if (x > values.length) x = values.length
  return getSum(values, x) / x
}

export function calculateRSI(values, x) {
  // Calculate RSI from the last x values gains and losses
  values = sliceValues(values, x)
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

export function checkVolatile(buys, x, percent, log=false) {
  // Check if the resource is volatile based on last x buy values
  buys = sliceValues(buys, x)
  let mean = getAvg(buys, x)
  if (log) {
    console.log('%cVOLATILE', 'font-size: large')
    console.log(`buys: ${buys}\nmean: ${mean}`)
    console.log(`samples: ${x}\npercent: ${percent}`)
  }
  let logger = []
  for (const buy of buys) {
    let change = Math.abs(mean - buy)
    let current = (change/mean)*100
    logger.push({ buy: buy, change: change, percent: current })
    if (current >= percent) {
      if (log) console.table(logger)
      return true
    }
  }
  if (log) console.table(logger)
  return false
}

export function checkLiquid(bids, asks, x, percent, log=false) {
  // Check if the resource is liquid based on last x values
  bids = sliceValues(bids, x)
  asks = sliceValues(asks, x)
  if (log) {
    console.log('%cLIQUID', 'font-size: large')
    console.log(`bids: ${bids}\asks: ${asks}`)
    console.log(`samples: ${x}\npercent: ${percent}`)
  }
  let logger = []
  for (const i in bids) {
    let change = Math.abs(bids[i] - asks[i])
    let max = Math.max(bids[i], asks[i])
    let current = (change/max)*100
    logger.push({ bid: bids[i], ask: asks[i],
      change: change, max: max, percent: current })
    if (current < percent) {
      if (log) console.table(logger)
      return true
    }
  }
  if (log) console.table(logger)
  return false
}
