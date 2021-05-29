export function dateToHTML(datetimeJS) {
  // "06.12.2012, 12:06:00" => "2012-12-06, 12:06:00"
  let [ date, time ] = datetimeJS.split(', ')
  date = date.split('.')
  return date[2]+'-'+date[1]+'-'+date[0]+', '+time
}

export function dateToJS(datetimeHTML) {
  // "2012-12-06, 12:06:00" => "06.12.2012, 12:06:00"
  let [ date, time ] = datetimeHTML.split(', ')
  date = date.split('-')
  return date[2]+'.'+date[1]+'.'+date[0]+', '+time
}

export function sliceByDate(data, datetime, timestamps) {
  let rangeIndex = null
  timestamps.forEach((timestamp, i) => {
    if (Date.parse(dateToHTML(timestamp)) >= Date.parse(dateToHTML(datetime)))
      if (rangeIndex == null) rangeIndex = i
  })
  data = data.map(d => d.slice(rangeIndex))
  if (data.length == 1)
    return data[0]
  return data
}
