export default function CandleChart({ candles }) {
  if (!candles.length) return null

  const width = 800
  const height = 340
  const padding = { top: 20, right: 100, bottom: 40, left: 20 }

  const plotWidth = width - padding.left - padding.right
  const plotHeight = height - padding.top - padding.bottom

  const lowest = Math.min(...candles.map(c => c.low))
  const highest = Math.max(...candles.map(c => c.high))

  const margin = (highest - lowest) * 0.08 ||
    Math.abs(highest) * 0.01 || 1

  const minPrice = lowest - margin
  const maxPrice = highest + margin

  const spacing = plotWidth / candles.length
  const candleWidth = spacing * 0.65

  const priceToY = price =>
    padding.top +
    ((maxPrice - price) / (maxPrice - minPrice)) * plotHeight

  const formatPrice = price =>
    price.toLocaleString('en-US', { maximumSignificantDigits: 6 })

  const formatTime = time =>
    new Date(time * 1000).toLocaleString('en-GB', {
      timeZone: 'UTC',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })

  return (
    <div className="chart-scroll" tabIndex={0} role="region" aria-label="Price chart, scroll horizontally on small screens">
      <svg
        className="candle-chart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Candlestick chart, prices in USDT and times in UTC"
      >
        {Array.from({ length: 5 }, (_, index) => {
          const price = minPrice + ((maxPrice - minPrice) * index) / 4
          const y = priceToY(price)

          return (
            <g key={index}>
              <line
                x1={padding.left}
                x2={width - padding.right}
                y1={y}
                y2={y}
                stroke="#e2e8f0"
              />
              <text
                x={width - padding.right + 10}
                y={y + 4}
                fontSize={12}
                fill="#64748b"
              >
                {formatPrice(price)}
              </text>
            </g>
          )
        })}

        {candles.map((candle, index) => {
          const x = padding.left + spacing * (index + 0.5)
          const openY = priceToY(candle.open)
          const closeY = priceToY(candle.close)
          const color = candle.close >= candle.open ? '#16a34a' : '#dc2626'

          return (
            <g key={candle.time}>
              <title>
                {`${formatTime(candle.time)} UTC
                  Open: ${candle.open}
                  High: ${candle.high}
                  Low: ${candle.low}
                  Close: ${candle.close}`}
              </title>
              <line
                x1={x}
                x2={x}
                y1={priceToY(candle.high)}
                y2={priceToY(candle.low)}
                stroke={color}
                strokeWidth={1.5}
              />
              <rect
                x={x - candleWidth / 2}
                y={Math.min(openY, closeY)}
                width={candleWidth}
                height={Math.max(Math.abs(openY - closeY), 1)}
                fill={color}
              />
            </g>
          )
        })}

        <text
          x={padding.left}
          y={height - 12}
          fontSize={12}
          fill="#64748b"
        >
          {formatTime(candles[0].time)} UTC
        </text>

        <text
          x={width - padding.right}
          y={height - 12}
          textAnchor="end"
          fontSize={12}
          fill="#64748b"
        >
          {formatTime(candles[candles.length - 1].time)} UTC
        </text>
      </svg>
    </div>
  )
}
